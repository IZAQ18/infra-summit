# LineProof feasibility record

## 16 September local execution checkpoint — supersedes unexecuted setup below

The user authorized bounded local work while Intel approval is pending, revising
the previous requirement to wait for cloud allocation before any local experiment.
Python 3.12.14 / MuJoCo 3.13.0 now run a two-arm SO101 scene on Windows 11. Both cameras,
scripted motion, stop/reset and rejected invalid actions were exercised. Ten tests
passed. Initial overlapping zero poses were identified and corrected; the replacement
initial state has zero contacts. Props are primitives, with no drawer or validated grasp.

A separate environment installed LeRobot 0.6.0, CPU PyTorch 2.11.0, torchvision 0.26.0
and OpenVINO 2026.3.1. ACT with two 128x128 images, 18 state inputs and 12 action outputs
ran with random parameters. Direct OpenVINO conversion and CPU inference passed
numerical parity for two input fixtures at the fixed shapes. This is not the Studio
training package, a trained checkpoint, a VLM, a task controller or final Core Ultra evidence.
See [commands, limitations and artifacts](LOCAL_FEASIBILITY.md) and [timings](../BENCHMARKS.md).

G1 remains unresolved on usable final hardware and a full-task learned route.
G2/G3 are unpassed; no training or task evaluation was performed. The next local
experiment should establish real contact-based manipulation and a credible full-task
demonstration source before committing compute to learning. The old 45-minute
scene-plus-data-plus-training plan below is unvalidated and must not be treated as an estimate.

## 16 September cloud access checkpoint

Account and catalog access are now verified. A Core Ultra Series 3 Windows 11 instance has been requested for one week. The authenticated portal reports **Pending Review**, with a USD 0.00 hourly rate and total cost. No host has been allocated or connected. Windows 11 was the only offered image; the previously researched Ubuntu setup must not be treated as installed or directly validated here. G1 remains unresolved because usable hardware and a full-task baseline are still missing. G2/G3 have not started. No software installation, model run, benchmark or robotics success is claimed.

## 15 September recovery checkpoint

G1 remains unresolved; G2/G3 have not started. The fully loaded [event schedule](https://lablab.ai/ai-hackathons/ai-infra-summit-hackathon) explicitly confirms submission closing at **16 September 23:30 PKT (18:30 UTC)**. Its online track still requires the full dual-SO-101 table-setting workflow and final Core Ultra Series 2/3 execution. Account registration or a requested instance does not establish allocated compute.

Two additional starting points were inspected as documentation only: [MolmoAct2 SO-101 simulation](https://github.com/ataghof/molmoact2-so101-sim), a single-arm cube task whose 5B policy quickstart recommends a 24 GB GPU for training/evaluation; and [EE5108 ACT simulation](https://github.com/EE5108-DigitalTwins/lerobot_mujoco_sim), a single-arm block-to-bin collection/training/deployment recipe. Neither establishes a trained full-task bimanual baseline. No code or model from either was incorporated, no environment was installed and no robotics measurement was produced. The ACT recipe is a possible collector reference, not a reason to mix its LeRobot 0.5.x environment with the Studio candidate below.

The planned feature freeze has passed with the product gates unfulfilled. Proceed only when usable required compute and a credible scene/data/policy path are established; do not treat unrelated demonstrations or other participants' submission descriptions as evidence of eligibility or our own success.

## 12 September source and resource investigation

12 September 2026 · G1 official-brief reconciliation and resource plan

**G1 UNRESOLVED; G2/G3 NOT STARTED.** The official online brief is available and ACT is permitted. The remaining blockers are usable Core Ultra Series 2/3 compute and a working full-task scene/data/policy path. No robotics dependency was installed, model downloaded, training started, simulation executed or product benchmark measured in this investigation.

This replaces the current decision in the 11 September record, preserved in git history at `7f52a6e862a061e6c5100dee5bfedd3d58155bce`. That investigation could not retrieve the full brief. Its missing-brief, mandatory-organizer-starter and ACT exclusion assumptions are superseded. A supplied pretrained checkpoint is a preferred shortcut, not an organizer prerequisite.

## Authoritative requirements and implications

The [official five-page online brief](https://drive.google.com/file/d/1xSisqTQUAFQiLOpjLZrCVTCsQi4bMCpO/view) was read through the event's linked PDF on 12 September. Pages 1–2 permit ACT/related imitation policies alongside VLA options and require multimodal reasoning for multi-step dinner-table manipulation. Pages 3–4 require final MuJoCo and AI inference plus benchmarks on Core Ultra Series 2/3; physical arms are unnecessary and Intel supplies no training compute. Page 4 requires scene/randomization, training/fine-tuning/evaluation/inference code, setup, an Intel benchmark script, architecture/README and video evidence across 10 randomized seeds. See [PRD v0.2](PRD.md) for task scope, rubric and acceptance criteria.

The brief's pouring sequence is an example; our chosen full task uses drawer/cutlery/plate/cup placement and a cup handoff. The prior handoff-only proposal is a development slice, not the submission. Numerical tolerances and success targets are our choices. The organizer workflow includes simulator state; separating privileged scoring from model inputs is our integrity design, not a quoted organizer prohibition.

The online track links [Intel Hack-a-thon Resources](https://docs.openedgeplatform.intel.com/dev/edge-ai-suites/robotics-ai-suite/resources/hackathon_resources.html) and the [official workshop](https://www.youtube.com/watch?v=HRG5qJPH8EQ). The resource page describes Ubuntu 24.04, Python 3.11, OpenVINO 2026.3 and LeRobot/XPU tooling. Its OS/driver installation instructions were not executed. Workshop video fetch was throttled; no unseen transcript content is asserted here. The event-linked PDF and inspected source files provide the findings below.

## Concrete candidate and inspected artifacts

These are source candidates, not a tested compatible installation. Preserve upstream licenses and notices when importing assets/code and mark modifications.

| Component | Exact source/version | Verified and remaining work |
|---|---|---|
| SO-101 geometry | [SO-ARM100 revision eecbe3e](https://github.com/TheRobotStudio/SO-ARM100/tree/eecbe3e0a9ebb23e25ad7b2759b03884c6660903/Simulation/SO101); full SHA `eecbe3e0a9ebb23e25ad7b2759b03884c6660903` | Read `scene.xml`, `so101_new_calib.xml` and repository Apache-2.0 license. Single arm has six radian position actuators and 13 referenced mesh files. Add a namespaced second arm, drawer/items/cameras and scorer; there is no ready dinner-table environment here. |
| ACT training/export | [Physical AI Studio revision 0388c19](https://github.com/open-edge-platform/physical-ai-studio/tree/0388c19b220fe4597da709f26010ea5642586dfe/library); full SHA `0388c19b220fe4597da709f26010ea5642586dfe` | Apache-2.0 ACT source; configurable state/action dimensions, equal-shaped camera inputs, ResNet18 initialization and action chunks. Native ACT plus OpenVINO export is the selected implementation candidate. No task-trained weights selected. |
| Dataset dependency | [LeRobot 0.6.0](https://pypi.org/project/lerobot/0.6.0/) | Studio pins this version; Python >=3.12. Wheel SHA256 `b38a564fbc441d98380576863bf68635dde5fc2c42ddc2a39d0486640dc9e9a8`. Apache-2.0. Build an explicit local LeRobot-format dataset; do not upload automatically. |
| Latest LeRobot inspected, not selected | [Revision b6ec006](https://github.com/huggingface/lerobot/tree/b6ec0060779550c0a157ae34feb89e0cf86012a8); full SHA `b6ec0060779550c0a157ae34feb89e0cf86012a8` | Its package version is 0.6.2 and requires Python >=3.12. Do not combine it with Studio's 0.6.0 pin. |
| Reasoning model | [SmolVLM2-256M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-256M-Video-Instruct/tree/067788b187b95ebe7b2e040b3e4299e342e5b8fd); revision `067788b187b95ebe7b2e040b3e4299e342e5b8fd` | Apache-2.0 image/text model. Candidate for structured phase/arm-role/continue decisions, not joint actions. No task recognition or completion accuracy measured. |
| VLM OpenVINO path | [Hugging Face/Intel export guide](https://huggingface.co/blog/openvino-vlm) | Documents Optimum conversion and INT8 weight compression of this model. Its older dependency example is not a tested lock for the selected 2026 stack. Export/processor compatibility remains a preflight check. |
| ACT export evidence | [Pinned upstream parity test](https://github.com/open-edge-platform/physical-ai-studio/blob/0388c19b220fe4597da709f26010ea5642586dfe/library/tests/integration/test_act_openvino_parity.py) | Contains native/export action and closed-loop comparisons using `lerobot/act_aloha_sim_transfer_cube_human` in ALOHA. We inspected code, did not run it. ALOHA task success would not establish dual-SO-101 dinner compatibility. |
| Rejected baseline shortcut | [OpenVINO/act-fp16-ov model card](https://huggingface.co/OpenVINO/act-fp16-ov) | Explicitly random weights for testing, with an example 8-dimensional state. Conversion/runtime smoke material only; never a task-trained baseline. |

The [LeRobot ACT guide](https://huggingface.co/docs/lerobot/act) describes an approximately 80M-parameter policy and gives roughly 50 demonstrations and hours of GPU training as introductory guidance. Those are vendor examples, not our required data count, our measured training time or a guarantee for a harder multi-stage task. Base image weights do not make an untrained action head competent.

## Environment and compute decision

Use an isolated **Python 3.12 CPU environment** for the selected Studio revision and its LeRobot 0.6.0 dependency. The [pinned package manifest](https://github.com/open-edge-platform/physical-ai-studio/blob/0388c19b220fe4597da709f26010ea5642586dfe/library/pyproject.toml) requires Python >=3.12,<3.15 and OpenVINO >=2026.3; its runtime source pin is `openvinotoolkit/physicalai@8e4021703ef43387a835c6647b993cecc069ca85`. Resolve the Studio CPU extra using its published CPU wheel index, then save the actual lock. Do not install latest LeRobot or mix this environment with the workshop's Python 3.11 environment. This is a manifest-compatible candidate, not a completed resolver/import test. The VLM export environment can be isolated if its Transformers/Optimum constraints differ; inference artifacts must preserve exact preprocessing and model revisions.

Final target: an actually allocated Core Ultra Series 2/3 host running both MuJoCo and required model inference. Start with its CPU path; test iGPU only if available and compatible. NPU and INT4 are not mandatory. Record device/OS/driver, memory, remaining session time, disk and export access. Do not assume the final allocation permits or supplies training. Coordinator owns account/cloud access verification.

Training candidate: the existing i5-1245U laptop with 32 GB RAM, CPU only. Availability of an isolated compatible environment, wheel resolution and useful training speed remain unmeasured. No CUDA, free GPU notebook or second machine is assumed. A desktop Python available for document work does not establish a training environment. The [Intel cloud guide](https://www.intel.com/content/www/us/en/developer/articles/guide/ai-pc-cloud-quick-user-guide.html) describes variable availability; free advertising or a portal page is not an allocation.

## Observation, action and reasoning contract

Proposed scene interface, to verify before collecting data:

- Two RGB views at 128×128 for the initial cost pilot; model preprocessing may resize, and that cost must be counted. Input image tensors use the implementation's validated channel/order/normalization contract. Increase resolution only as a new recorded configuration if cutlery is not observable.
- Joint vector is 12 radian positions: left then right, each `shoulder_pan, shoulder_lift, elbow_flex, wrist_flex, wrist_roll, gripper`. The SO-101 gripper is a hinge angle, not an arbitrary 0–1 aperture. Preserve source actuator limits and verify action-to-joint mapping.
- Six phase values: open drawer, place spoon, place fork, place plate, handoff cup, place cup. Append the six-way one-hot phase code to joint state, making proposed ACT state dimension 18 and action dimension 12. Train with the same phase representation used at inference. The phase is an intended skill, not proof that the prior skill succeeded.
- Proposed `chunk_size=10`, `n_action_steps=1`, 10 Hz control: predict ten steps but authorize only one 100 ms simulated step before the next validity boundary. This avoids treating the upstream 100-step default as our freshness contract. Actual useful cadence remains a G2 measurement.
- SmolVLM receives current images and instruction and chooses a supported phase, arm assignment and continue/reacquire/stop response. A deterministic validator only rejects impossible transitions or invalid output; it cannot silently pick the correct next phase for the model. Store raw structured decisions and resulting phase inputs.
- Teacher phases and exact object poses may be used in training demonstrations. During evaluation, model-selected phases and camera/proprioception inputs are used. Scoring, teacher control and evaluation control are separate interfaces. Any deterministic sequencing baseline, welded grasp aid or scripted intervention gets a separate label and metric.

A phase-selector check must include changed images with the same instruction and changed supported instructions with the same image. Select ten development cases spanning phases and ambiguous/occluded states. Proposed continuation criterion is at least eight correct structured decisions and no completion claim on the ambiguous cases; failure is reported, not concealed by scripted sequencing. A VLM cannot alone certify final success; fresh post-action visual verification remains separately tested.

## Quantified bounded task-training proposal — not executed

This is **task training of a motor policy initialized with an image backbone**, not adaptation of an already trained dinner-table checkpoint. We have found no compatible demonstrations or competent checkpoint. The proposed demonstration source is an original MuJoCo scripted teacher using explicit geometry/IK and phase labels, solely for data generation. Writing and debugging that teacher is a major dependency; no existing teacher is claimed. Do not copy another participant's results or imply their learned policy is ours.

| Item | Proposed fixed budget / check |
|---|---|
| Coverage | 20 complete training demonstrations plus 5 validation demonstrations, each covering all six phases. Seeds and randomization separate from final evaluation. Partial episodes are labelled and excluded from the complete-demo quota. |
| Duration/data | At most 120 simulated seconds per demonstration, sampled at 10 Hz: 24,000 training samples, 6,000 validation samples. Two RGB 128×128 uint8 cameras imply at most 2.359 GB training + 0.590 GB validation raw image payload (decimal units), excluding metadata, video overhead and caches. |
| Collection cost | At real-time pacing, 25×120 seconds is 50 minutes before training. At an actually measured 10× simulation/render throughput it is 5 minutes. No such throughput has been measured; a slow renderer or difficult teacher can invalidate the budget. |
| Initial model | Studio ACT/ResNet18 configuration; batch size 4, two views, state 18/action 12, chunk 10. Keep the initial architecture fixed for the pilot. Freeze/backbone caching is a separate proposed change, not a free assumed speedup. |
| Training cap | At most 2,000 optimizer steps **or 20 minutes elapsed training time**, whichever comes first; one configuration, no sweep. First 100 steps count toward both limits. Stop early if the first 100 steps cannot finish within 3 minutes. |
| Resource cap | Proposed process-RAM cap 16 GB on the 32 GB laptop; stop on out-of-memory, sustained swapping, nonfinite loss or incompatible data/schema. Reserve up to 10 GB for dataset, checkpoints and exports after checking free space; dependency caches/downloads are additional and must be measured. |
| Timing estimate | After 100 steps, use measured seconds/step plus observed checkpoint/validation overhead. 2,000 steps at 0.5 s/step is 16.7 minutes; at 2 s/step it is 66.7 minutes. These examples are arithmetic, not hardware measurements. Stop/reassess if projected work exceeds the cap; do not silently expand it. |
| Continuation evidence | Validation action error must improve against the untrained initialization under identical normalization. Then three fresh full-task learned-policy runs must execute, with at least one complete success to pass G2. Loss improvement, teacher success or one successful phase alone cannot pass. |
| Failure rule | If no complete teacher/data path fits the approved preparation budget, or training/resources/recognition fail the cap or criteria, retain evidence and stop. No automatic extra demonstrations, larger model or new training campaign. |

The pilot is deliberately a low-cost test of whether there is a viable route. Twenty demonstrations and 2,000 steps may be insufficient for this task. This uncertainty is why G1 has not passed and why training has not begun. A failed budget test is not proof ACT is unsuitable; it establishes that this candidate path does not fit the current constraints.

## Next executable sequence after prerequisites resolve

1. **Resource preflight:** coordinator establishes usable Core Ultra access; finalize separate training permission/resource and available session time. Record pinned source/model/asset licenses and a compatible dependency lock. No installs or G2 until this plan and required compute are resolved.
2. **Scene and data preparation:** compose the two-arm MJCF; add the full dinner task, scorer and randomization manifest; verify 12-joint ordering, limits, RGB observations and simulator stop. Implement the teacher and show at least one complete teacher episode before generating the dataset. Label all of this scripted preparation. It is not a learned baseline. Budget this preparation explicitly within the next authorized execution block; if it cannot fit, stop instead of hiding it as setup.
3. **Measure the fixed pilot:** validate the 20/5 dataset split, execute the 100-step timing probe, and continue only within the 2,000-step/20-minute and memory caps. The preparation, probe, training and evaluation together must fit that block's 45-minute active-work ceiling; the training cap is not an additional allowance. Save checkpoint, config, timing and validation evidence.
4. **Learned baseline gate:** remove teacher/oracle inputs and run three full-task attempts. Record both phase-selector behavior and learned arm motion. At least one full success is required for G2; otherwise stop. Calibrate action/observation/episode budgets only on development cases.
5. **Export and G3:** use Studio's ACT export API and the documented VLM Optimum export path; compare reference/export outputs and development task decisions before closed-loop testing on Core Ultra. First compare reference/FP32 or FP16-compatible execution; try INT8 only if supported and quality is preserved. Then demonstrate fresh observe → reason → learned action → verify plus stale-action rejection and two-arm stop. Report actual optimization device/precision; no benchmark exists yet.
6. **Only after gates:** implement the viewer/trace comparison and run the official 10-seed suite, additional registered fault experiments and required video/reproducibility package before freeze. All failures remain in the evidence.

Steps 2–5 describe code and experiments still to be created, not commands that already work in this repository. The concrete resources and interface are identified, but demonstration production and runtime behavior are unproven. This is the remaining executable-plan gap, separate from the external Core Ultra access gap.

## Current decision and bounded-work record

| Gate | Status | Reason |
|---|---|---|
| G1 | UNRESOLVED | Official requirements resolved. Source/model licenses, candidate revisions and resource budget documented. Actual final compute, resolved environment and working full-task scene/data/policy path remain unverified. |
| G2 | NOT STARTED | No installation, training pilot, learned checkpoint execution or baseline attempt. |
| G3 | NOT STARTED | No integrated reasoning/action/verification run or Intel benchmark. |

The reconciliation block began 12 September at 10:02:34 PKT (05:02:34 UTC), was interrupted, and resumed on the user's continue message. The pause does not start a second 45-minute active-work allowance. Research ends with this document review/publication; no speculative execution is added. Source reads and arithmetic are evidence about a plan, not measurements of a robot product.
