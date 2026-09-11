# LineProof PRD review

11 September 2026 (PKT) · Review of [PRD version 0.1](PRD.md)

**Documentation is ready for review. Implementation feasibility is unresolved.** This note records a document review, not a robot test, eligibility determination or product validation.

## Main decisions

- One handoff-and-place job is proposed only if the official starter and compatible pretrained policy support it. Otherwise the PRD must be revised around one supported bimanual job.
- Actual VLA control and the event's accepted multimodal reasoning path need execution evidence. Scripted motion and recorded replay cannot satisfy those requirements.
- The supervisor rejects stale actions, checks fresh post-action camera evidence, permits one recovery replan and otherwise stops. Hidden simulator state is restricted to scenario preparation, fault injection and scoring.
- The comparison uses the same policy and matched held-out scenarios. It preserves baseline safeguards and reports unsuccessful attempts, false completion claims, recovery, stops, latency and overhead.
- Five expected-stop scenarios are included in the all-episode success denominator. A correct stop is reported as stop behavior, never as completed manipulation. The completion target uses a separately disclosed, predeclared eligible subset.
- Intel/OpenVINO remains conditional on rules and actual compatibility. Local inference measurements cannot substitute for any required sponsor-device benchmark.

## Review findings resolved

1. Removed the stale statement about the README's prior direction.
2. Distinguished action-completion acknowledgement from command dispatch before post-action verification.
3. Required verification-frame coverage across the dwell interval and acknowledged the limits of sampled visual evidence.
4. Added explicit evidence for the event's multimodal reasoning requirement; retrospective captions do not qualify.
5. Clarified success denominators so intentionally unrecoverable cases do not pressure the implementation to mislabel stops.

## Documentation checks

Passed: LP-01 through LP-13 are unique and their references resolve; Markdown fences and table widths are consistent; whitespace and relative-link checks pass; PKT/UTC deadline conversions agree; public-content and credential-pattern scans found no matches. The tracked diff whitespace check also passed. The only files authored in this review are PRD.md and PRD_REVIEW.md. Markdown structure was checked without a rendered-layout test.

Primary event announcements and research abstracts were inspected during drafting; the full track specification and authenticated submission form were not available. The general submission-guide link is only a checklist reference, not verified event-specific requirements. Link-form checks do not establish access to authenticated resources.

All LP-01 through LP-12 requirements remain proposed, and LP-13 is deferred. No acceptance criterion or feasibility gate is marked passed. Numerical outcome thresholds and timing budgets are targets requiring calibration and evidence. No product tests or benchmarks were run in this documentation phase.

## Unresolved go/no-go items

- Official online brief, starter revision, exact supported task and compatible pretrained checkpoint.
- Enrollment/eligibility, mandatory hardware/runtime, permitted free local or remote access and resource limits.
- Accepted multimodal reasoning architecture, observable task predicates, coordinated action/stop contracts and feasible inference timing.
- Live judging expectations, any mandated sponsor-device benchmark and the final submission fields.

The next phase consists of the three bounded feasibility blocks in the PRD: requirements/access, actual baseline, then observe–act–verify with required inference. Each block is at most 45 minutes. None has been completed by writing these documents. No implementation, dependency installation, commit or push is part of this review.
