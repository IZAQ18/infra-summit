"""Preserve gripper concavities with reproducible CoACD collision parts."""
import hashlib
import json
from pathlib import Path
import struct
import time

import coacd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "simulation" / "collision_parts"
NAMES = ("wrist_roll_follower_so101_v1", "moving_jaw_so101_v1")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    coacd.set_log_level("info")
    options = dict(threshold=.004, real_metric=True, max_convex_hull=12, resolution=500,
                   mcts_nodes=5, mcts_iterations=10, mcts_max_depth=2, preprocess_resolution=20, seed=0)
    manifest = {"method": "CoACD 1.0.14", "options": options, "meshes": {}}
    for name in NAMES:
        started = time.perf_counter()
        raw = (ROOT / ".cache/so101/assets" / f"{name}.stl").read_bytes()
        count = struct.unpack_from("<I", raw, 80)[0]
        if len(raw) != 84 + 50 * count:
            raise ValueError("Expected binary upstream STL")
        triangles = np.frombuffer(raw, dtype=np.dtype([("normal", "<f4", 3), ("vertices", "<f4", (3, 3)), ("attribute", "<u2")]), offset=84)["vertices"]
        vertices, inverse = np.unique(triangles.reshape(-1, 3), axis=0, return_inverse=True)
        mesh = coacd.Mesh(vertices.astype(float), inverse.reshape(-1, 3).astype(np.int32))
        print(f"Decomposing {name}, {len(vertices)} vertices", flush=True)
        parts = coacd.run_coacd(mesh, **options)
        files = []
        for index, (v, f) in enumerate(parts):
            path = OUT / f"{name}_{index:02}.obj"
            lines = ["# Derived from Apache-2.0 SO-ARM100 STL; see THIRD_PARTY.md"]
            lines.extend("v " + " ".join(f"{x:.9g}" for x in point) for point in v)
            lines.extend("f " + " ".join(str(int(x) + 1) for x in face) for face in f)
            path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
            files.append({"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        manifest["meshes"][name] = {"source_sha256": hashlib.sha256(raw).hexdigest(), "parts": files}
        print(name, len(parts), f"{time.perf_counter()-started:.2f}s", flush=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
