---
globs: ["docs/**"]
description: Docs conventions — auto-applied when docs are touched.
---

# Docs rules

- Nothing new at the top level of `docs/`; every folder/file numbered; run
  `python docs/lint_docs.py` after structural changes.
- Every doc opens with "Read this when: …". Budget: ≤120 lines (lint warns).
- Never restate a documented fact — link it (SSOTs in CLAUDE.md). Full writing
  rules: docs/05-guidelines/03-writing.md.
- Tasks/features: copy the TEMPLATE, keep front-matter valid (backlog sorting
  depends on it). Benchmarks append to docs/04-findings/benchmarks/<constraint>.md;
  other findings get NNNN-slug.md + an index row.
- Tracking CSVs are append-only; ids must exist in 01-project-definition.
