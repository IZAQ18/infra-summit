"""Record an honest scripted cube pick/place attempt, including failed attempts."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mujoco
import numpy as np
from PIL import Image, ImageDraw
from simulation.scene import LocalScene
from simulation.teacher import ScriptedTeacher


def assess(records, initial, final, target_xy, failure=None):
    hold = [r for r in records if r["phase"] == "hold"]
    height_gain = min(r["cube"][2] for r in hold) - initial[2] if hold else None
    contact_hold = bool(hold) and all({"left_gripper", "left_moving_jaw_so101_v1"}.issubset(r["cube_contact_bodies"]) for r in hold)
    transfer = [r for r in records if r["phase"] == "transfer"]
    uninterrupted_carry = bool(transfer) and all(
        r["cube"][2] > initial[2] + .04 and
        {"left_gripper", "left_moving_jaw_so101_v1"}.issubset(r["cube_contact_bodies"])
        for r in transfer)
    lower = [r for r in records if r["phase"] == "lower"]
    supported_lower = bool(lower) and all(
        {"left_gripper", "left_moving_jaw_so101_v1"}.issubset(r["cube_contact_bodies"]) or
        ("world" in r["cube_contact_bodies"] and abs(r["cube"][2] - initial[2]) < .012)
        for r in lower)
    final_distance = float(np.linalg.norm(final[:2] - target_xy))
    released = all(not any(b.startswith("left_") for b in r["cube_contact_bodies"]) for r in records[-20:])
    stable = len(records) >= 20 and float(np.max(np.linalg.norm(np.array([r["cube"] for r in records[-20:]]) - final, axis=1))) < .002
    passed = bool(failure is None and height_gain is not None and height_gain > .04 and contact_hold and uninterrupted_carry and supported_lower and final_distance < .025 and released and stable and abs(final[2] - initial[2]) < .012)
    return {"min_sustained_lift_m": float(height_gain) if height_gain is not None else None,
            "contact_throughout_hold": contact_hold, "uninterrupted_carry": uninterrupted_carry,
            "supported_lower": supported_lower, "scorer_version": 3,
            "final_xy_error_m": final_distance, "released": released, "stable": stable,
            "scripted_pick_place_passed": passed}


def run(output, render=False, height=.047, offset=0., close=-.1, roll=None, grasp_offset=(0., 0., 0.), collision_mode="original", tilt=.74236, destination=(-.075, -.07), seed=None):
    if not np.isfinite(tilt) or not 0 <= tilt <= 1:
        raise ValueError("Expected downward tilt in [0, 1]")
    output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    scene = LocalScene(collision_mode=collision_mode, seed=seed)
    teacher = ScriptedTeacher(scene)
    cube = scene.model.body("cube").id
    cube_geom = scene.model.geom("cube_geom").id
    site = scene.model.site("left_gripperframe").id
    target_xy = np.array(destination, float)
    frames, records, solves = [], [], []
    renderer = mujoco.Renderer(scene.model, height=480, width=720) if render else None
    targets = scene.home.copy()
    targets[5] = .9
    initial = scene.data.xpos[cube].copy()
    failure = None

    def sample(phase, target):
        scene.step(target, epoch=scene.epoch, steps=25)
        contacts = []
        for contact in scene.data.contact:
            if cube_geom in (contact.geom1, contact.geom2):
                other = contact.geom2 if contact.geom1 == cube_geom else contact.geom1
                body = scene.model.body(int(scene.model.geom_bodyid[other])).name
                contacts.append(body or "world")
        records.append({"time": float(scene.data.time), "phase": phase,
                        "cube": scene.data.xpos[cube].tolist(),
                        "tool": scene.data.site_xpos[site].tolist(),
                        "qpos": scene.data.qpos[scene.qpos_ids].tolist(),
                        "action": target.tolist(), "cube_contact_bodies": contacts})
        if renderer and len(records) % 2 == 0:
            im = Image.fromarray(scene.render(renderer))
            ImageDraw.Draw(im).text((12, 12), f"SCRIPTED PHYSICS EXPERIMENT | {phase} | {scene.data.time:.1f}s", fill="white", stroke_width=1, stroke_fill="black")
            frames.append(im)

    def move(phase, end, chunks=30):
        nonlocal targets
        start = targets.copy()
        for index in range(1, chunks + 1):
            fraction = index / chunks
            fraction = fraction * fraction * (3 - 2 * fraction)
            sample(phase, start + (end - start) * fraction)
        targets = end.copy()
        if renderer:
            camera = mujoco.MjvCamera()
            camera.lookat[:] = scene.data.xpos[cube]
            camera.distance = .26
            camera.azimuth = 80
            camera.elevation = -20
            renderer.update_scene(scene.data, camera=camera)
            Image.fromarray(renderer.render()).save(output / f"{phase}-closeup.png")

    def pose(xy, z, seed):
        radial = np.r_[np.asarray(xy) - [-.29, 0], 0.]
        radial /= np.linalg.norm(radial)
        approach = radial * np.sqrt(1 - tilt ** 2) + [0, 0, -tilt]
        position = np.r_[xy, z] + offset * approach
        q, errors = teacher.solve(position, seed=seed, approach=approach, roll=roll, grasp_offset=grasp_offset)
        solves.append({"target": position.tolist(), **errors})
        if errors["position_error_m"] > .004 or errors["approach_error_rad"] > .15:
            raise RuntimeError(f"Unreachable teacher waypoint: {solves[-1]}")
        return q

    try:
        move("settle", targets, 20)
        initial = scene.data.xpos[cube].copy()
        start_xy = initial[:2].copy()
        end = targets.copy()
        end[:5] = pose(start_xy, .13, [.3, -.3, .4, .7, 0.])
        move("approach", end, 40)
        end[:5] = pose(start_xy, height, end[:5])
        move("descend", end, 40)
        end[5] = close
        move("close", end, 30)
        end[:5] = pose(start_xy, .13, end[:5])
        move("lift", end, 40)
        move("hold", end, 20)
        end[:5] = pose(target_xy, .13, end[:5])
        move("transfer", end, 40)
        end[:5] = pose(target_xy, height, end[:5])
        move("lower", end, 40)
        end[5] = .9
        move("release", end, 30)
        end[:5] = pose(target_xy, .13, end[:5])
        move("retreat", end, 40)
        move("verify", end, 40)
    except RuntimeError as error:
        failure = str(error)
    finally:
        if renderer:
            renderer.close()
    final = scene.data.xpos[cube].copy()
    assessment = assess(records, initial, final, target_xy, failure)
    report = {"kind": "SCRIPTED_CONTACT_PROBE_NOT_LEARNED_POLICY", "utc": datetime.now(timezone.utc).isoformat(),
              "mujoco": mujoco.__version__, "configuration": {"height": height, "offset": offset, "close": close, "roll": roll, "grasp_offset": list(grasp_offset), "collision_mode": collision_mode, "tilt": tilt, "seed": seed},
              "randomization": "cube XY +/-5 mm and yaw +/-0.12 rad" if seed is not None else None,
              "initial_cube": initial.tolist(), "final_cube": final.tolist(), "target_xy": target_xy.tolist(),
              **assessment, "sample_period_seconds": .05,
              "hold_contact_requirement": "Both fixed finger and moving jaw in every hold/transfer sample; supported lowering",
              "failure": failure, "full_task_success": None, "learned_policy": None,
              "waypoint_errors": solves, "simulated_seconds": float(scene.data.time), "wall_seconds": time.perf_counter()-started}
    if frames:
        frames[0].save(output / "attempt.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
        frames[-1].save(output / "final.png")
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    (output / "trajectory.json").write_text(json.dumps(records) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("artifacts/contact-probe"))
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--height", type=float, default=.047)
    parser.add_argument("--offset", type=float, default=0.)
    parser.add_argument("--close", type=float, default=-.1)
    parser.add_argument("--roll", type=float)
    parser.add_argument("--grasp-offset", type=float, nargs=3, default=(0., 0., 0.))
    parser.add_argument("--collision-mode", choices=("original", "decomposed"), default="original")
    parser.add_argument("--tilt", type=float, default=.74236)
    parser.add_argument("--destination", type=float, nargs=2, default=(-.075, -.07))
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    print(json.dumps(run(args.output, args.render, args.height, args.offset, args.close, args.roll, args.grasp_offset, args.collision_mode, args.tilt, args.destination, args.seed), indent=2))
