# /write-devlog — add a devlog chapter

Write a new entry in docs/02-planning/devlog/ covering work since the last entry.

1. Find the range: last entry's closing commit (its blockquote) → `git log --oneline`
   since then. Pick ONE theme; if the range spans two themes, write two entries.
2. Copy devlog/TEMPLATE.md → `YYYY-MM-<theme-slug>.md`. Fill the commit-range
   blockquote with real short SHAs, messages, and the date range.
3. Write 2-5 narrative sections — the story of the work (what was tried, what broke,
   what it feels like now), NOT a change list. Narrative titles, no "Bugfixes".
4. Screenshots: reference `images/NN-slug.png`; for missing art leave
   `> 📷 *Screenshot to add later: …*`.
5. Wire navigation: **Next:** link in the previous entry → this one; back-links to
   index; add the chapter line + teaser in index.md and refresh its At-a-glance table.
6. Style check: docs/05-guidelines/03-writing.md (this is the one place prose may
   breathe, but still no filler).
