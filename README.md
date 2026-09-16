# Infra Summit · LineProof (provisional)

Proposed: two simulated SO-101 arms set a dinner table through a learned ACT policy
and camera/instruction reasoning, with stale-action rejection and visual verification.
See the [product requirements](docs/PRD.md).

**Current state: local physics prototype and CPU runtime preflight.** Two simulated
SO-101 arms render and perform scripted motion on Windows. Stop/reset and input
validation are tested. A random-weight ACT model runs natively and through OpenVINO.
There is no learned task policy, successful manipulation, dashboard or deployed demo.

![Recorded scripted motion — not learned control](docs/evidence/scripted-motion.gif)

[Reproduce the experiment](docs/LOCAL_FEASIBILITY.md) · [Measured results](BENCHMARKS.md)

The official brief is now resolved: a full multi-step dinner-table task, 10 randomized
seeds, and final MuJoCo/AI inference and benchmarking on Core Ultra Series 2/3 are required.
ACT is an allowed policy option; an organizer-supplied pretrained starter is not required.
The local i5 laptop does not satisfy the final hardware requirement.

**G1 remains unresolved** on usable mandatory compute and an executable scene/data/policy
path. SO-101 geometry and LeRobot ACT now have local execution evidence. The full
Studio training stack and SmolVLM2 reasoning are still untested. No task training
has run and the learned-baseline/complete-system gates remain unpassed.
See [sources, resource budget and next steps](docs/FEASIBILITY.md).

## Run in three commands

Foundation checks require Python 3.11+ and no dependencies or credentials.
The optional simulator and policy preflight use Python 3.12 and separate dependency
locks; see [local setup](docs/LOCAL_FEASIBILITY.md).

```sh
git clone https://github.com/IZAQ18/infra-summit.git
cd infra-summit
python status.py
```

Run checks: `python -m unittest discover -s tests -v`.

## Implemented foundation

```mermaid
flowchart LR
    Request --> Registry[Validated async tools]
    Registry --> Mode{Runtime mode}
    Mode -->|live / record| Adapter[Caller-supplied adapter]
    Mode -->|replay| Cache[Exact request + version cache]
    Adapter --> Validation[Validate result]
    Cache --> Validation
    Validation --> Result
```

Runtime supports bounded async calls, opt-in safe retries, metadata-only traces,
explicit sanitized recording, offline replay and ordered provider fallback.
No LLM service is configured. See `agent_core/runtime.py`.

## Evidence

| Measurement | Result |
|---|---|
| Local simulation | 12 actuators, two cameras, scripted motion; stop/reset checks pass |
| Local OpenVINO | ACT random-weight CPU conversion and numerical parity tested |
| Learned task success | Not demonstrated |
| Required Core Ultra benchmark | Not run |

See [BENCHMARKS.md](BENCHMARKS.md) for the required evidence protocol.
The recording above is a physics smoke test. No application demo or submission video exists.

## Next slice

Validate contact-based grasp/release and a full-task demonstration source before a
bounded learned-policy pilot. Obtain Core Ultra allocation for final execution.
Scripted motion and random-weight runtime checks are not the dinner-table submission.

Built by [IZAQ18](https://github.com/IZAQ18) · 2026 · MIT
