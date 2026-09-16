"""Physics integration checks; optional in the dependency-free foundation suite."""
import unittest

try:
    import numpy as np
    from simulation.scene import LocalScene, ROOT
    AVAILABLE = (ROOT / ".cache/so101/so101_new_calib.xml").exists()
except ModuleNotFoundError:
    AVAILABLE = False


@unittest.skipUnless(AVAILABLE, "Install simulation dependencies and fetch pinned SO101 assets")
class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.scene = LocalScene()

    def test_both_arms_move_without_interarm_contact(self):
        s = self.scene
        self.assertEqual(s.model.nu, 12)
        self.assertEqual(s.data.ncon, 0, "Initial model must not overlap")
        initial = s.data.qpos[s.qpos_ids].copy()
        target = s.home.copy()
        target[[0, 6]] += .15
        for _ in range(10):
            result = s.step(target, epoch=s.epoch)
            for contact in s.data.contact:
                bodies = [s.model.body(s.model.geom_bodyid[g]).name for g in (contact.geom1, contact.geom2)]
                self.assertFalse(any(b.startswith("left_") for b in bodies) and
                                 any(b.startswith("right_") for b in bodies), bodies)
        self.assertTrue(np.all(np.abs(result[[0, 6]] - initial[[0, 6]]) > .1))
        self.assertTrue(np.all(np.abs(result[[0, 6]] - target[[0, 6]]) < .02))

    def test_invalid_commands_do_not_change_physics_or_control(self):
        s = self.scene
        old_qpos, old_ctrl = s.data.qpos.copy(), s.data.ctrl.copy()
        for values in (np.zeros(11), np.full(12, np.nan), np.full(12, np.inf), np.full(12, 100)):
            with self.assertRaises(ValueError):
                s.step(values, epoch=s.epoch)
            np.testing.assert_array_equal(s.data.qpos, old_qpos)
            np.testing.assert_array_equal(s.data.ctrl, old_ctrl)
            self.assertEqual(s.data.time, 0)

    def test_stop_and_reset_invalidate_old_commands(self):
        s = self.scene
        initial_qpos = s.data.qpos.copy()
        old_epoch = s.epoch
        s.step(s.home, epoch=old_epoch)
        before_stop, stop_time = s.data.qpos.copy(), s.data.time
        s.stop()
        with self.assertRaises(ValueError):
            s.step(s.home, epoch=old_epoch)
        np.testing.assert_array_equal(s.data.qpos, before_stop)
        self.assertEqual(s.data.time, stop_time)
        s.reset()
        with self.assertRaises(ValueError):
            s.step(s.home, epoch=old_epoch)
        np.testing.assert_array_equal(s.data.qpos, initial_qpos)
        self.assertEqual(s.data.time, 0)
        s.step(s.home, epoch=s.epoch)
        self.assertGreater(s.data.time, 0)

    def test_chunk_limit_rejects_excess_work(self):
        s = self.scene
        for steps in (0, 51, -1, 1.5):
            with self.assertRaises(ValueError):
                s.step(s.home, epoch=s.epoch, steps=steps)
        self.assertEqual(s.data.time, 0)


if __name__ == "__main__":
    unittest.main()
