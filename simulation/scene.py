"""Compose two pinned SO101 arms and simple tabletop props in MuJoCo."""
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
JOINTS = ("shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper")
ARM_JOINTS = tuple(f"{side}_{joint}" for side in ("left", "right") for joint in JOINTS)


def camera_axes(position, target) -> str:
    z = np.asarray(position, dtype=float) - target
    z /= np.linalg.norm(z)
    x = np.cross([0., 0., 1.], z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    return " ".join(map(str, np.r_[x, y]))


def build_scene() -> str:
    source = ROOT / ".cache" / "so101" / "so101_new_calib.xml"
    if not source.exists():
        raise FileNotFoundError("Run python tools/fetch_so101.py first")
    upstream = ET.parse(source).getroot()
    root = ET.Element("mujoco", model="lineproof_dual_so101_feasibility")
    compiler = deepcopy(upstream.find("compiler"))
    compiler.set("meshdir", (source.parent / "assets").as_posix())
    root.append(compiler)
    ET.SubElement(root, "option", timestep="0.002", integrator="implicitfast")
    for defaults in upstream.findall("default"):
        root.append(deepcopy(defaults))
    root.append(deepcopy(upstream.find("asset")))
    visual = ET.SubElement(root, "visual")
    ET.SubElement(visual, "global", offwidth="960", offheight="640")
    ET.SubElement(visual, "headlight", diffuse="0.7 0.7 0.7", ambient="0.35 0.35 0.35")
    world = ET.SubElement(root, "worldbody")
    ET.SubElement(world, "light", pos="0 -0.4 1.8", dir="0 0 -1", directional="true")
    ET.SubElement(world, "geom", name="floor", type="plane", size="2 2 .05", pos="0 0 -.06", rgba=".22 .22 .20 1")
    ET.SubElement(world, "geom", name="table", type="box", size=".48 .34 .02", pos="0 0 0", rgba=".68 .61 .49 1")
    actuators = ET.SubElement(root, "actuator")
    for side, x, quat in (("left", -.29, "1 0 0 0"), ("right", .29, "0 0 0 1")):
        body = deepcopy(upstream.find("./worldbody/body"))
        for node in body.iter():
            if "name" in node.attrib:
                node.set("name", f"{side}_{node.get('name')}")
        body.set("pos", f"{x} 0 .022")
        body.set("quat", quat)
        world.append(body)
        for actuator in upstream.find("actuator"):
            item = deepcopy(actuator)
            item.set("name", f"{side}_{item.get('name')}")
            item.set("joint", f"{side}_{item.get('joint')}")
            actuators.append(item)
    # Primitive objects are physics props, not a validated dinner-task scene.
    objects = (("cube", "box", ".018 .018 .018", "0 -.08 .04", ".7 .2 .12 1"),
               ("plate", "cylinder", ".055 .005", "-.10 -.18 .028", ".86 .86 .82 1"),
               ("cup", "cylinder", ".022 .035", ".10 -.16 .058", ".15 .35 .30 1"),
               ("spoon", "box", ".007 .038 .003", "-.05 .12 .028", ".70 .72 .74 1"),
               ("fork", "box", ".008 .038 .003", ".03 .12 .028", ".56 .59 .62 1"))
    for name, kind, size, position, color in objects:
        body = ET.SubElement(world, "body", name=name, pos=position)
        ET.SubElement(body, "freejoint", name=f"{name}_free")
        ET.SubElement(body, "geom", name=f"{name}_geom", type=kind, size=size,
                      rgba=color, mass=".03", friction="1 .005 .0001")
    for name, position in (("front", [0., -.95, .8]), ("side", [.85, .15, .75])):
        ET.SubElement(world, "camera", name=name, pos=" ".join(map(str, position)),
                      xyaxes=camera_axes(position, np.array([0, 0, .13])), fovy="48")
    return ET.tostring(root, encoding="unicode")


class LocalScene:
    """12 joint-target inputs. Stop pauses this simulator, not physical hardware."""

    def __init__(self):
        self.model = mujoco.MjModel.from_xml_string(build_scene())
        self.data = mujoco.MjData(self.model)
        self.joint_ids = np.array([self.model.joint(name).id for name in ARM_JOINTS])
        self.qpos_ids = self.model.jnt_qposadr[self.joint_ids]
        self.ctrl_ids = np.array([self.model.actuator(name).id for name in ARM_JOINTS])
        self.limits = np.stack((np.maximum(self.model.jnt_range[self.joint_ids, 0],
                                            self.model.actuator_ctrlrange[self.ctrl_ids, 0]),
                                np.minimum(self.model.jnt_range[self.joint_ids, 1],
                                            self.model.actuator_ctrlrange[self.ctrl_ids, 1])), axis=1)
        self.epoch = 0
        self.stopped = True
        # The two upstream zero poses overlap. Start with separated pan angles.
        self.home = np.zeros(12)
        self.home[[0, 6]] = .65
        self.home[[5, 11]] = .4
        self.reset()

    def reset(self):
        self.epoch += 1
        mujoco.mj_resetData(self.model, self.data)
        self.data.qpos[self.qpos_ids] = self.home
        self.data.ctrl[self.ctrl_ids] = self.home
        mujoco.mj_forward(self.model, self.data)
        self.stopped = False
        return self.epoch

    def stop(self):
        self.stopped = True
        self.epoch += 1

    def step(self, targets, *, epoch: int, steps: int = 50):
        if self.stopped or epoch != self.epoch:
            raise ValueError("Stopped or expired episode action")
        targets = np.asarray(targets, dtype=float)
        if targets.shape != (12,) or not np.isfinite(targets).all():
            raise ValueError("Expected 12 finite joint targets in radians")
        if np.any(targets < self.limits[:, 0]) or np.any(targets > self.limits[:, 1]):
            raise ValueError("Joint target outside allowed range")
        if not isinstance(steps, int) or not 1 <= steps <= 50:
            raise ValueError("A chunk must contain 1 to 50 physics steps")
        self.data.ctrl[self.ctrl_ids] = targets
        mujoco.mj_step(self.model, self.data, nstep=steps)
        if not np.isfinite(self.data.qpos).all() or not np.isfinite(self.data.qvel).all():
            self.stop()
            raise RuntimeError("Physics produced nonfinite state")
        return self.data.qpos[self.qpos_ids].copy()

    def render(self, renderer, camera="front"):
        renderer.update_scene(self.data, camera=camera)
        return renderer.render().copy()
