# DECISIONS.md - decision & learnings log

A short running note of the real choices you made: what you tried, what failed and why, what
you changed. This is your engineering judgement on the record - it is what separates a builder
from a button-presser, and it is graded (from git history + this file + PROMPTS.md, NOT from
an auto audit log, which may be empty on cloud models).

Append a 1-2 line entry whenever you make a real decision or hit/fix a wall. Add a timestamp.

Format:
`[HH:MM] <decision or problem> -> <what you did and why>`

---

## Example (replace with your own)
- `[10:20]` Used `Unique Inlinks` for orphan detection, not `Inlinks` -> `Inlinks` counts
  duplicate links (nav appearing twice), so it never hits 0; `Unique Inlinks` is the real
  orphan signal.
- `[11:05]` Path-segment clustering merged unrelated root pages -> kept it as the starter but
  added TF keywords so the topic-agent can split/name them properly.
- `[12:40]` Dashboard not updating live -> server tool wasn't emitting the SSE event; added
  `_emit(...)` in each li_* tool.

---

## My log
- `[--:--]` ...
- `[12:55]` Initialized Git repository and connected GitHub remote -> created public repository and pushed starter bundle before development to preserve build history.
-`[13:45]` Reviewed cluster_pages() before modification -> identified URL-path clustering as the primary weakness because topic keywords are computed but not used to determine cluster membership.
-`[13:55]` Rejected simple home-page reassignment approach -> improves only the "(home)" cluster and does not fully satisfy the rulebook requirement that clustering be based on titles, headings, and body text.
-`[14:05]` Evaluated keyword-seed clustering proposal -> stronger than URL-path clustering because it uses content-derived keywords and is robust to flat URL structures. Deferred implementation pending review of cluster stability and false-positive risks.
-`[14:15]` Selected graph-based connected-component clustering over URL-path and seed-based approaches -> deterministic, content-driven, order-invariant, and more robust to hidden exports with flat URL structures.
-`[14:35]` Replaced URL-path clustering with graph-based connected-component clustering using filtered keyword overlap and adaptive Jaccard thresholds. Reduced cluster count from 47 to 13 while preserving report generation.
-`[14:50]` Reviewed link_candidates() against rulebook section E -> current implementation ranks only by relatedness and ignores orphan, under-linked, and scattered-cluster priorities required by the specification.
-`[15:05]` Designed strategic recommendation ranking to prioritize orphan, under-linked, and scattered-cluster targets rather than sorting solely by relatedness.
-`[15:18]` Implemented strategic recommendation ranking using multiplicative scoring. Added orphan, under-linked, and scattered-cluster prioritization plus a relevance floor of 0.1. Recommendation count reduced from 30 to 28 due to removal of weak matches.
-`[15:20] Verified cluster naming not implemented -> searched codebase and confirmed cluster["name"] remains None throughout pipeline.
-`[15:39] Implemented topic-agent cluster naming workflow. Verified names flow through li_topics(names=...) into report.json. Current environment fell back to cluster keys because model endpoint did not return names.
-`[15:51]` Implemented topic-agent cluster naming workflow through run.py and li_topics(names=...). Verified model-generated names populate report.json with fallback to cluster keys when generation fails.
-`[15:55] Implemented cluster naming orchestration path with fallback behavior. Naming currently falls back to cluster keys under current execution environment and requires further debugging.
-`[16:05]` Implemented deterministic suggested anchors using target page Title 1, H1-1, and shared-topic fallbacks -> removed null suggested_anchor values from recommendations.