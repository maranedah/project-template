# KPI definitions

Read this when: adding a KPI datapoint to `../02-planning/tracking/kpis.csv` (ids must
match) or reporting in a weekly update.

| Id | Name | Formula / how measured | Source of the number | Target |
|---|---|---|---|---|
| KPI-01 | <!-- FILL: e.g. workflow W-01 duration --> | <!-- FILL: exact measurement method --> | <!-- FILL: e2e timing / API log / manual --> | <!-- FILL --> |
| KPI-02 | <!-- FILL --> | <!-- FILL --> | <!-- FILL --> | <!-- FILL --> |

Record datapoints append-only:

```bash
echo "2026-08-13,KPI-01,412,ms,e2e/test_smoke,first paint" >> docs/02-planning/tracking/kpis.csv
```
