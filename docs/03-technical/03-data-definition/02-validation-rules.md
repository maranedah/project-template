# Data validation rules

Read this when: ingesting data or writing validation code.

## Universal rules (apply to every entity)

- **No null** in required columns; **non-empty** strings (whitespace-only = empty).
- **No duplicates** on natural keys — declare the key per entity below.
- **Type validation** at the boundary (pydantic on API input, checks on ingestion).
- **Source column mandatory**: every datum records where it came from —
  `file:<path>`, `api:<name>`, `url:<address>`, or `manual:<who>`.

## Cross-validation with sources

<!-- FILL: for each ingested dataset, how a sample is checked against the original
source (spot-check N records, count totals, checksum). Discrepancies → finding. -->

## Per-entity rules

| Entity | Natural key (no-dup) | Extra rules |
|---|---|---|
| item | <!-- FILL: e.g. name+source --> | <!-- FILL --> |
