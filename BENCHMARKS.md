# Benchmarks

No full-task or Core Ultra benchmark has been run. The measurements below
are local feasibility probes, with no task-trained checkpoint or task success rate.
Later [event guidance permits older Intel deployment](docs/DEPLOYMENT_FALLBACK.md).

## 16 September 2026 — local Windows feasibility

Host: Intel Core i5-1245U, approximately 32 GB RAM, Windows 11 build 26200.
Python 3.12.14. Exact package sets are in `requirements-sim.lock` and
`requirements-policy-preflight.lock`. This laptop is not Core Ultra; the later
Intel-XPU deployment allowance is documented separately above.

Executed code revision: `a1c4e765ba96700a1fc587ed37797b8becff9a3a`.
The follow-up publication changes documentation/evidence packaging only.
Raw measurement JSON is preserved byte-for-byte by `.gitattributes`.
Run commands from the repository root:

```powershell
.venv/Scripts/python.exe tools/local_smoke.py --output artifacts/local-smoke-separated
.cache/act-venv/Scripts/python.exe tools/policy_preflight.py --openvino --output artifacts/policy-preflight-verified
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

| Probe | Measured result | Scope |
|---|---|---|
| Scripted SO101 physics, 02:21 PKT / 15 Sep 21:21 UTC | 80 chunks, 50 physics steps each, 8 simulated seconds | MuJoCo 3.13.0; 2 ms step; 12 actuators |
| Physics chunk latency | p50 4.251 ms, p95 6.419 ms | Excludes rendering, model inference and encoding; no discarded warmup |
| Complete recorded smoke run | 22.333 wall seconds | Includes compilation, rendering and GIF encoding; not real time |
| Pan travel | 0.39996 rad per arm | Scripted targets; no manipulation/task success |
| Stop/reset | Rejected motion after stop, unchanged paused state, reset error 0 rad | Single-threaded simulator pause, not physical safety |
| ACT native CPU, 10:02 PKT / 05:02 UTC | median 60.634 ms | Five calls after one warmup; random parameters; FP32, four threads |
| ACT OpenVINO CPU, same probe | median 42.649 ms | Five calls after one warmup; FP32 hint, four threads |
| Native/OpenVINO agreement | max absolute error 0.000001386 | Passes atol/rtol 0.0001 on original and changed-value fixtures |
| Repository tests | 10 passed | Six foundation tests and four physics integration tests |

ACT: LeRobot 0.6.0, PyTorch 2.11.0+cpu, torchvision 0.26.0+cpu, OpenVINO 2026.3.1;
51,569,548 parameters, seed 7, no checkpoint, no pretrained backbone. Two 128x128
RGB simulator images and 18 state values produce a tensor of shape 1x10x12.
No model action was executed. Five samples and one scene do not support general
performance claims. Conversion is validated only for the specified input shapes.

The earlier exploratory ACT run measured medians 61.657 ms native and 51.421 ms
OpenVINO. The final run above adds a changed-input parity test. This variation is
another reason not to advertise a production speedup from these small samples.

Raw evidence and SHA-256:

- `docs/evidence/local-smoke-report.json`: `1ccbeefa6d69580b9e06013f125dd6529dd5fe3b3afd9d856dd00870755e4593`
- `docs/evidence/policy-preflight-report.json`: `475209d35cc99ed78add0b34d08ca552cdc0a186beb1efdbda8025c22f031410`
- `docs/evidence/joint-trajectory.json`: `1206843a943e19b56a1e1794b43a548dafc294c8a8b59c4d03e648ef4c6af513`

The scene assets use the pinned Apache-2.0 SO-ARM100 model described in
[THIRD_PARTY.md](THIRD_PARTY.md). There is no training/evaluation dataset yet.
Initial zero-pose arm intersection was discovered visually and through contact
inspection, then corrected before the reported smoke run. Primitive props and the
absence of a drawer/grasp pipeline mean this is not a full dinner-table scene.

Future runs must record command, commit, date in PKT, hardware, model/version,
dataset/license, sample count, warmup, runtime, precision and raw artifact hash.
Report failed runs as failures; distinguish measured, replayed and simulated data.

## Contact and training-runtime probes (16 September)

On the same i5-1245U laptop, scorer v3's nominal scripted cube trial held the cube
79.54 mm above its starting height, retained sampled jaw contacts through transfer,
lowered with grasp/table support, and released stably at 9.14 mm XY error. Ten seeds
with cube XY +/-5 mm and yaw +/-0.12 rad yielded 6 passes and 4 failures. These are
scripted oracle experiments, not learned or full dinner-table results.
See docs/CONTACT_EXPERIMENT.md for exact command, scoring, failures and raw evidence.
Thirteen tests pass, including a regression that rejects a recorded dropped cube
which an earlier endpoint-only check incorrectly accepted.

A single synthetic ACT forward/backward/AdamW step on CPU took 3.101 seconds, with
finite gradients (batch 1, two 128x128 images, PyTorch 2.11.0+cpu, four CPU threads).
Command: `.cache/act-venv/Scripts/python.exe tools/training_preflight.py --device cpu`.
This is one cold runtime sample, not a training throughput estimate or task learning.
No checkpoint was saved. Raw output: docs/evidence/training-preflight-cpu.json.
CUDA execution on the proposed NVIDIA desktop is not yet verified.
