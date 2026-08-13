# Connectors

Read this when: adding or debugging an integration with an external API.

One section per connector. Env vars live in `.env.example` (link, don't restate).
Rate limits and quirks belong in [04-findings](../../04-findings/00-index.md) — link the
finding id here. Adapter code goes in `backend/app/infrastructure/<connector>/`.

## <!-- FILL: connector name (e.g. Gemini, BrightData, Mercado Público, GitHub) -->

| | |
|---|---|
| Purpose | <!-- FILL: what we use it for --> |
| Auth | <!-- FILL: key/OAuth/none + which env var in .env.example --> |
| Docs | <!-- FILL: official docs URL --> |
| Limits | <!-- FILL: rate/quota + link to finding if measured --> |
| Offline fallback | <!-- FILL: fixture/Null adapter used when offline --> |
| Update command | <!-- FILL: command that refreshes the offline backup/fixtures --> |
