"""Record a scripted physics smoke test. No learned policy or task success."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mujoco
import numpy as np
from PIL import Image
from simulation.scene import ARM_JOINTS, LocalScene


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("artifacts/local-smoke"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    scene = LocalScene()
    compiled_seconds = time.perf_counter() - started
    timings, frames, trajectory = [], [], []
    initial_contacts = scene.data.ncon
    with mujoco.Renderer(scene.model, height=640, width=960) as renderer:
        for camera in ("front", "side"):
            Image.fromarray(scene.render(renderer, camera)).save(args.output / f"initial-{camera}.png")
        initial = scene.data.qpos[scene.qpos_ids].copy()
        for frame in range(80):
            target = scene.home.copy()
            target[[0, 6]] += .20 * np.sin(frame / 79 * 2 * np.pi)
            tick = time.perf_counter()
            positions = scene.step(target, epoch=scene.epoch)
            trajectory.append(positions.tolist())
            timings.append((time.perf_counter() - tick) * 1000)
            frames.append(scene.render(renderer))
        Image.fromarray(frames[-1]).save(args.output / "final-front.png")
    before_stop = scene.data.qpos.copy()
    stop_time = scene.data.time
    old_epoch = scene.epoch
    scene.stop()
    stop_rejected = False
    try:
        scene.step(np.zeros(12), epoch=old_epoch)
    except ValueError:
        stop_rejected = True
    stop_unchanged = bool(np.array_equal(before_stop, scene.data.qpos) and scene.data.time == stop_time)
    scene.reset()
    reset_error = float(np.max(np.abs(scene.data.qpos[scene.qpos_ids] - initial)))
    # GIF is a recording of actual rendered scripted simulation frames, not AI control.
    images = [Image.fromarray(frame) for frame in frames]
    images[0].save(args.output / "scripted-motion.gif", save_all=True, append_images=images[1:],
                   duration=100, loop=0)
    report = {"kind": "SCRIPTED_PHYSICS_SMOKE_NOT_LEARNED_POLICY", "utc": datetime.now(timezone.utc).isoformat(),
              "python": platform.python_version(), "os": platform.platform(), "mujoco": mujoco.__version__,
              "joint_order": ARM_JOINTS, "actuator_count": scene.model.nu,
              "simulated_seconds": stop_time, "physics_chunks": len(timings), "chunk_steps": 50,
              "physics_chunk_ms_p50": float(np.median(timings)), "physics_chunk_ms_p95": float(np.percentile(timings, 95)),
              "compile_seconds": compiled_seconds, "whole_run_wall_seconds": time.perf_counter() - started,
              "initial_contacts": initial_contacts,
              "pan_travel_rad": np.ptp(np.asarray(trajectory)[:, [0, 6]], axis=0).tolist(),
              "stop_rejected_action": stop_rejected, "stop_state_unchanged": stop_unchanged,
              "reset_max_error_rad": reset_error, "task_success": None, "learned_policy": None,
              "artifacts": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in args.output.glob("*") if p.suffix in (".png", ".gif")}}
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    (args.output / "joint-trajectory.json").write_text(json.dumps(trajectory) + "\n")
    print(json.dumps(report, indent=2))
    if not stop_rejected or not stop_unchanged or reset_error > 1e-10:
        raise RuntimeError("Stop or reset failed")


if __name__ == "__main__":
    main()
