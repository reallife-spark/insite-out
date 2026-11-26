# Plan

current: all seven sub-issues implemented or designed locally — awaiting review, no implementation frontier.

## Completed

1. [x] Bootstrap the full numbered spine from `vault_templete` and initialise Git.
2. [x] Create the public GitHub repo and add the `origin` remote.
3. [x] Register the repo in Home's index, glossary map, backlinks and pointer doc.
4. [x] Configure Matt Pocock skills: GitHub Issues, Home triage labels, full domain model.
5. [x] Replace placeholder steering in `00_System/`, `02_Daily/` and `05_Knowledge/`.
6. [x] Capture the pasted AI Mode answer and its cited pages one layer deep.
7. [x] Distill the SDK contract, source synthesis, domain model, project hub, contract and ADRs.
8. [x] Pass repo-fitness spine and registry checks.
9. [x] Write and publish the Crown + Watch5 Pro physiological feedback spec (issue #1).
10. [x] Break the spec into seven approved tracer-bullet sub-issues (#2–#8) with native blocking edges.
11. [x] Implement and test the validated feedback-event envelope for issue #2.
12. [x] Implement and test the Crown adapter for issue #3.
13. [x] Decide and record the Watch metric vocabulary for issue #4.
14. [x] Record advisory-only authority and the direct-trigger follow-up for issue #5.
15. [x] Implement the Watch tracer: recorded heart-rate payload to agent event, with local bridge
    and ADR 0003, for issue #6.
16. [x] Complete the approved Watch metric set with replay coverage for issue #7.
17. [x] Write the deferred composed-state design and ADR 0005 for issue #8.

## Next step (not started)

- Review issues #2–#8. No further implementation is planned: #8 is design-only and any future
  implementation must be authorised by a new ticket that reverses the parallel-events rule.

Definition of done for issue #2:

- one validated agent-facing contract for both Crown and Watch physiological feedback;
- structured `source` with device, model and metric;
- generic `watch-metric` kind with metric, unit and value;
- `observed_at` and `expires_at` with explicit stale-feed readiness;
- advisory-only authority stated in the contract;
- glossary and acquisition-boundary decisions aligned with two sources.
