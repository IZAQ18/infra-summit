# 16 September update

[Later track guidance](DEPLOYMENT_FALLBACK.md) permits older Intel deployment.
The current i5 laptop is our documented fallback; Core Ultra cloud is no longer
the sole route. Learned full-task execution is still unproven.

# Local feasibility experiment — 16 September 2026

This is a **scripted physics and runtime experiment**, not the hackathon solution.
It demonstrates a local Windows development path while Core Ultra access awaits
approval. No learned dinner-table policy, visual verifier or full-task success exists.

## Reproduce the simulator

Python 3.12 and `uv` are used below. This downloads about 16 MB of pinned SO-101
assets, plus the dependencies in the lock file. No cloud credentials are needed.

```powershell
uv venv --python 3.12 .venv
uv pip sync --python .venv/Scripts/python.exe requirements-sim.lock
.venv/Scripts/python.exe tools/fetch_so101.py
.venv/Scripts/python.exe tools/local_smoke.py --output artifacts/local-smoke-separated
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

On Linux replace `.venv/Scripts/python.exe` with `.venv/bin/python`.
Linux execution has not been verified. Camera rendering requires a working OpenGL
context; the measured run used the Windows laptop's local graphics stack.

## What runs

- Two SO-101 arms, twelve position-target actuators, radian limits, gravity and contact physics.
- A table, red cube, and primitive plate/cup/cutlery proxies. The cup is solid and
  cutlery is rectangular. There is no drawer or validated grasp/task geometry yet.
- Front and side RGB cameras, saved images and an eight-simulated-second recording.
- Scripted pan sweeps, bounded 100 ms chunks, invalid-target rejection, pause-on-stop,
  and deterministic reset. Stop/reset invalidate old episode actions.

The adapter's stop prevents future simulation steps. It is not an emergency-stop
claim for physical hardware. It is single-threaded and does not yet enforce frame
age, inference deadlines, visual verification or concurrent command cancellation.

## Evidence and limitations

The first arrangement placed the two zero-pose arms through each other. Camera and
contact inspection found this, so the scene now initializes separated pan angles.
The corrected initial state has zero contacts. Tests exercise both-arm motion without
inter-arm contact, rejected malformed/nonfinite/out-of-range commands, chunk limits,
and stop/reset behavior. All ten repository tests passed with simulation dependencies.

The GIF plays back frames at simulation cadence. Rendering/encoding took longer than
the eight-second simulated trajectory; it is **not a real-time or learned-control demo**.
Physics-only timings exclude camera rendering, model inference and encoding.
See [BENCHMARKS](../BENCHMARKS.md) and `docs/evidence/local-smoke-report.json`.

## Remaining critical path

1. Validate a real grasp, release and placement with contact physics.
2. Establish a complete dinner-task demonstration/data source and learned policy.
3. Add actual image/instruction reasoning and post-action verification.
4. Obtain the requested Core Ultra host, execute the complete pipeline there and
   record all official randomized trials, including failures.

Runtime compatibility is a useful prerequisite; random weights and scripted motion
cannot pass the learned baseline gate. No training has been performed in this block.

## Reproduce the ACT/OpenVINO probe

Use a separate environment: the LeRobot dependency set needs a different NumPy
version from the simulator lock. This CPU setup downloads roughly 400 MB of wheels.

```powershell
uv venv --python 3.12 .cache/act-venv
uv pip sync --python .cache/act-venv/Scripts/python.exe requirements-policy-preflight.lock --index https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match
.cache/act-venv/Scripts/python.exe tools/policy_preflight.py --openvino
```

Run the simulator first to produce the two input images. The probe creates random
ACT parameters with seed 7, no pretrained backbone, 18 zero-valued state inputs,
two RGB frames resized to 128x128 with values in [0,1], ten output steps and twelve
joint outputs. This identity-normalized fixture is not a trained preprocessing contract.
Actions are never sent to the simulator. One warmup and five timed calls per runtime
are followed by a separate parity check using changed image/state values.

Direct `openvino.convert_model` on the LeRobot policy was tested. The complete
Physical AI Studio dependency set, its export adapter, training/data loading and
multimodal reasoning were not tested. Trace warnings restrict conclusions to the
tested batch size and input shapes; dynamic shapes are not established. CPU execution
uses four threads and an FP32 hint. GPU discovery is not evidence of GPU execution.
