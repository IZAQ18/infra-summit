# LineProof feasibility record

11 September 2026 · G1 requirements and free-access investigation

**Decision: G1 BLOCKED. G2 and G3 NOT STARTED.** An authoritative online task specification, accepted starter/checkpoint and usable permitted compute allocation have not been established. This is an access/requirements decision, not evidence that robotics cannot run on the laptop. No simulator, policy, sponsor inference or product benchmark was executed.

Investigation began at **21:07:58 PKT (16:07:58 UTC)**. The evidence checkpoint below was taken at **21:12:58 PKT (16:12:58 UTC)**, five minutes into the original 45-minute maximum block. The block has not been restarted. Research stopped short of speculative installation because the essential requirements remain unresolved; the remaining work in this block is documenting, checking and publishing this record.

## Purpose and decision rule

Determine whether the [provisional PRD](PRD.md) has an eligible, zero-spend path to an actual pretrained bimanual baseline. The distinction is between finding robotics software and establishing a usable, accepted task/model/compute combination. A general library, an advertised free cloud service or another participant's demo does not establish that combination.

Proceed to G2 only after the full online rules, supported task, policy compatibility, permitted inference location and actual mandatory resource access are verified. No purchase, system installation, new training project or integration with another sponsor is part of this investigation.

## Gate status

| Gate | Status | Evidence / reason |
|---|---|---|
| G1: official requirements and free access | BLOCKED | Primary announcements confirm the broad online route. Exact task, starter, accepted pretrained model and mandatory execution/judging conditions remain unresolved; usable mandatory resource access is unverified. |
| G2: actual pretrained baseline | NOT STARTED | G1 prerequisite not met. No environment installation, model download or baseline episode. |
| G3: observe → act → verify | NOT STARTED | No G2 baseline. No inference, action execution, verification or stop claim. |

No PRD acceptance criterion has passed through this investigation. The PRD's proposed handoff-and-place job, numerical targets and hardware conditions remain unchanged.

## Primary-source findings

| Source checked | What it establishes | What it does not establish |
|---|---|---|
| [Organizer live dashboard](https://lablab.ai/ai-hackathons/ai-infra-summit-hackathon/live) and [Intel track page](https://lablab.ai/ai-hackathons/ai-infra-summit-hackathon?track=intel-bimanual-vla-manipulation-with-multi-modal-reasoning) | An Intel bimanual VLA track is listed. The indexed dashboard states submission closes 16 September 2026 at 23:30 PKT (18:30 UTC). | Full online technical requirements, enrollment, accepted starter or checkpoint, or final form/judging access. |
| [Organizer Intel announcement](https://www.linkedin.com/company/lablab-ai) | The indexed company announcement distinguishes physical onsite SO-101 work from online dual SO-101 simulation in MuJoCo using VLA and multimodal reasoning. | That onsite hardware/software requirements also apply online; a specific accepted model or task. The current company feed is dynamic and did not retain the older Intel post in its directly opened excerpt. |
| [Intel AI PC development page](https://www.intel.com/content/www/us/en/developer/topic-technology/ai-pc/download-get-started.html) | Intel advertises free AI PC Cloud access to Core Ultra hardware. | Guaranteed admission, current capacity, an assigned instance, a quota sufficient for judging or acceptance of the current laptop as a benchmark substitute. |
| [Intel AI PC Cloud quick guide](https://www.intel.com/content/www/us/en/developer/articles/guide/ai-pc-cloud-quick-user-guide.html) | The published registration route requires a company or university email. The catalog includes Core Ultra Series 2/3; availability varies by user and capacity. The guide says requests are processed within 48 hours. | A hackathon exception, automatic approval or an actual allocation for this project. |
| [Intel Hack-a-thon Resources](https://docs.openedgeplatform.intel.com/dev/edge-ai-suites/robotics-ai-suite/resources/hackathon_resources.html) | A published preinstalled-stack/setup reference targets Ubuntu 24.04 LTS and Core Ultra/Arc, with Python 3.11, OpenVINO 2026.3, Anomalib 2.6.0, LeRobot/PyTorch XPU and Physical AI Studio. | That this setup governs the online track, or that it supplies the dual-SO-101 task/checkpoint. Its driver, OS and reboot instructions were not executed. |
| [Intel humanoid pipelines](https://docs.openedgeplatform.intel.com/dev/edge-ai-suites/robotics-ai-suite/software_references/humanoid/index.html) | Intel provides robotics reference pipelines, including ACT/RDT on ALOHA and a Pi0.5 VLA pipeline. | Compatibility of those embodiments/checkpoints with the online dual SO-101 task. |
| [Hugging Face SmolVLA guide](https://huggingface.co/docs/lerobot/smolvla) | SmolVLA uses camera views, robot state and language; its guide describes adapting the base model with task data for optimal setup-specific performance. | A ready checkpoint for the proposed handoff scene, or evidence that base weights will complete it without adaptation. No training was started. |

Source pages were read on 11 September 2026. Generic platform documentation is supporting evidence, not event rules. No free-service advertising was converted into an access claim.

## Access states kept separate

| Access stage | State at this checkpoint |
|---|---|
| Free Intel AI PC Cloud advertised | Verified in Intel's public development page |
| Project eligible for its registration/access route | Not verified |
| Instance requested by this investigation | No |
| Instance actually allocated and reachable for this project | Not verified |
| Required runtime/model successfully executed there | No |
| Availability for the event's judging window | Not verified |

Account identifiers, email addresses and session details are intentionally absent from this public record. No organizers were contacted and no account creation or cloud request was submitted.

## Retrieval and repository checks actually performed

| Check | Observed result |
|---|---|
| Browser surface discovery through the supported browser tool, then one retry | Both failed with `Unable to load browser request-header policy`. No browser session was inspected; empty discovery is not evidence that the user is signed out. |
| Public lablab event/track retrieval through web tools | Indexed track/date information available; no authoritative full online brief obtained. One direct track open returned an internal retrieval error. |
| Public event URL request using Python standard-library `urllib.request.urlopen`, 30-second timeout | HTTP 403. No authenticated cookies or alternate credentials were used. |
| `gh search repos 'AI Infra Summit' --limit 20 --json fullName,description,url` | Returned project repositories including two participant dinner-table implementations; no official starter identified in this result set. |
| GitHub searches for SO-101/hackathon code, an Intel SO101/MuJoCo repository, lablab bimanual repositories, and hackathon references in Physical AI Studio | No matching official online starter returned. Search absence is not proof that a starter does not exist. |
| Official Intel documentation link traversal | Found the Hack-a-thon Resources page and the official Physical AI Studio / Physical AI runtime repositories. |
| GitHub API reads of official repository HEADs and pinned README files | Exact revisions recorded below; read-only inspection, no clone/import/install. |
| Local processor/GPU inventory and version commands | i5-1245U and Iris Xe reconfirmed; Python 3.14.6, Git 2.55.0.windows.3, GitHub CLI 2.96.0. No runtime compatibility or performance test. |

Repository baseline at investigation start: `9a722b4bea772f90c6ae5cdc30b5155c29c5fe23`. Working tree was clean. The known development environment remains Windows 11 with about 32 GB RAM; no verified NVIDIA/WSL target. The generic Intel stack's Python 3.11 is a documented version, not the installed project runtime.

### Official code references inspected

- [Physical AI Studio README at 0388c19](https://github.com/open-edge-platform/physical-ai-studio/blob/0388c19b220fe4597da709f26010ea5642586dfe/README.md): policy-training, benchmark and export framework. README blob `5ed1ea8011f2bbaf10b70abcd0c31d993377f336`. No accepted event-specific task/checkpoint was established by the inspected README.
- [Physical AI runtime README at a5e2750](https://github.com/openvinotoolkit/physicalai/blob/a5e275065f7a241a808b182bdcc31b62f6fc0a60/README.md): SO-101 robot-interface examples are available, but that does not supply a verified online simulated bimanual policy. README blob `4bd1733b160db3b9d8528c5f32acbb96c5ce2701`.

These revisions were obtained using `gh api repos/OWNER/REPO/commits/HEAD`, then README content was read using the exact revision. They are inspection references, not selected dependencies. No simulator, policy checkpoint, task manifest, model license or compatible package set has been selected.

### Participant leads, not authoritative requirements

[Table for Two](https://github.com/suzyeth/table-for-two) describes a dinner-table task and Core Ultra target; it discloses trained ACT, scripted assistance and constraint-assisted grasping. [Bimanual dinner-table SO101](https://github.com/jianwang-ntu/bimanual-dinner-table-so101) also describes a dinner-table scenario and separates controller/policy outcomes. Their public README descriptions were inspected to look for official source links, not to adopt their interpretation or reproduce their claimed results.

Observed repository HEADs: Table for Two `72ee5aaa3c939da4176347a2c14721c07c7196ab`; Bimanual dinner-table SO101 `cd04f44fb8f8f05c10f18d8950a823cf69b2a857`. These observations do not establish eligibility, claim accuracy or the versions used for their reported results. No participant code or assets were copied or run.

**Implication to verify:** the required job may be broader than the PRD's one handoff. Obtain the actual brief before changing scope. These leads are insufficient to revise the approved PRD or substitute a trained participant ACT policy for the required accepted VLA.

## Exact blockers and restart evidence

| Blocker | Evidence needed to resolve it |
|---|---|
| Official online task and rules | Full organizer/sponsor brief with task, scoring, permitted scene modifications, required models/architecture, optimization/precision deliverables and live-versus-recorded judging rules |
| Starter/checkpoint compatibility | Official or explicitly accepted starter and model links; pinned revision; checkpoint/license; documented camera, joint/action and preprocessing compatibility for the chosen bimanual task |
| Compute route | Confirmation of required hardware/runtime and permitted local/remote inference; an actually reachable free allocation if the rules demand a device unavailable locally |
| Participant/judging eligibility | Verified enrollment/team status and applicable online judging/submission access requirements, kept outside public account notes |
| One-job scope | Confirmation that the selected handoff is sufficient or a PRD revision based on the official task, not participant descriptions |

A request for the full brief/starter/model links, enrollment confirmation and any allocated cloud access is pending. No extra permission is needed to continue the already authorized gates once this evidence resolves G1. Waiting for it is not a gate pass.

## Recommendation and next action

**Hold LineProof implementation and do not start G2 yet.** Obtain the official brief and usable resource evidence first. If the track mandates inaccessible hardware, an unsupported task, or new training to obtain a baseline, record a no-go under the current zero-spend/time limits and reassess the entry with the project owner. Do not silently switch to a different sponsor, task or scripted controller.

If G1 resolves, bind the PRD to the accepted task/checkpoint and execute G2 in an isolated project environment, with its own maximum 45-minute block: three fresh baseline attempts and at least one scored bimanual success, with actual inference and timing records. G3 follows only after G2 passes. Local inference evidence must remain separate from any mandated sponsor-device benchmark.

The useful outcome of this block is a concrete evidence checklist and identified access risk. There is no new product functionality, no measured success rate and no basis for a winning-probability claim.

## Documentation checks and handoff

At **21:15:39 PKT (16:15:39 UTC)**, 7 minutes 41 seconds after the original start, the G1 decision and documentation checks were complete. Markdown/table structure, local links, whitespace, gate-status statements and scans for private paths/credential patterns passed. The only changed project files were this record and its README link. No product code changed, so no new robot or application tests were run. Publication of the reviewed documentation follows this checkpoint; the resulting commit and verified remote hash are reported in the task handoff.
