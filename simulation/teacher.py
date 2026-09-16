"""Ground-truth, scripted kinematic teacher; this is not a learned policy."""
import mujoco
import numpy as np


class ScriptedTeacher:
    """Solve position and approach direction in scratch data, never live qpos."""

    def __init__(self, scene, side="left"):
        if side not in ("left", "right"):
            raise ValueError("Expected left or right")
        self.scene = scene
        self.model = scene.model
        self.scratch = mujoco.MjData(self.model)
        self.indices = np.arange(5) + (0 if side == "left" else 6)
        self.qids = scene.qpos_ids[self.indices]
        self.dofs = self.model.jnt_dofadr[scene.joint_ids[self.indices]]
        self.site = self.model.site(f"{side}_gripperframe").id

    def solve(self, position, seed=None, approach=(0., 0., -1.), iterations=250, roll=None, grasp_offset=(0., 0., 0.)):
        position, approach = np.asarray(position, float), np.asarray(approach, float)
        if position.shape != (3,) or approach.shape != (3,) or not np.isfinite(np.r_[position, approach]).all() or np.linalg.norm(approach) < 1e-8:
            raise ValueError("Expected finite position and nonzero approach vectors")
        approach = approach / np.linalg.norm(approach)
        grasp_offset = np.asarray(grasp_offset, float)
        if grasp_offset.shape != (3,) or not np.isfinite(grasp_offset).all():
            raise ValueError("Expected finite grasp offset")
        self.scratch.qpos[:] = self.scene.data.qpos
        q = self.scene.data.qpos[self.qids].copy() if seed is None else np.array(seed, float)
        if q.shape != (5,) or not np.isfinite(q).all():
            raise ValueError("Expected five finite seed angles")
        limits = self.scene.limits[self.indices]
        if roll is not None:
            if not np.isfinite(roll) or not limits[4, 0] <= roll <= limits[4, 1]:
                raise ValueError("Roll outside joint limits")
            q[4] = roll
        jp, jr = np.zeros((3, self.model.nv)), np.zeros((3, self.model.nv))
        for _ in range(iterations):
            q = np.clip(q, limits[:, 0], limits[:, 1])
            self.scratch.qpos[self.qids] = q
            mujoco.mj_forward(self.model, self.scratch)
            axis = self.scratch.site_xmat[self.site].reshape(3, 3)[:, 0]
            point = self.scratch.site_xpos[self.site] + self.scratch.site_xmat[self.site].reshape(3, 3) @ grasp_offset
            dp = position - point
            da = approach - axis
            direction_error = np.linalg.norm(da) if roll is None else abs(da[2])
            if np.linalg.norm(dp) < .0005 and direction_error < .005:
                break
            mujoco.mj_jac(self.model, self.scratch, jp, jr, point, self.model.site_bodyid[self.site])
            ja = np.cross(jr[:, self.dofs].T, axis).T
            if roll is None:
                jac = np.vstack((jp[:, self.dofs], .1 * ja))
                error = np.r_[dp, .1 * da]
            else:
                # Fix jaw rotation; the remaining four joints solve XYZ + pitch.
                jac = np.vstack((jp[:, self.dofs[:4]], .1 * ja[2:3, :4]))
                error = np.r_[dp, .1 * da[2]]
            delta = np.linalg.solve(jac.T @ jac + 1e-5 * np.eye(jac.shape[1]), jac.T @ error)
            q[:len(delta)] += delta * min(1., .15 / max(np.linalg.norm(delta), 1e-8))
        q = np.clip(q, limits[:, 0], limits[:, 1])
        self.scratch.qpos[self.qids] = q
        mujoco.mj_forward(self.model, self.scratch)
        point = self.scratch.site_xpos[self.site] + self.scratch.site_xmat[self.site].reshape(3, 3) @ grasp_offset
        error = float(np.linalg.norm(position - point))
        angle = float(np.arccos(np.clip(np.dot(approach, self.scratch.site_xmat[self.site].reshape(3, 3)[:, 0]), -1, 1)))
        return q, {"position_error_m": error, "approach_error_rad": angle}
