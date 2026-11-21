# GEO (AI-search visibility) and agent readiness

## How AI search picks sources

AI answers fan one question into many sub-queries and quote passages that answer them cleanly. Most cited pages already rank well in classic search, so technical and content SEO come first. Third-party studies (dates matter; re-check) found brand mentions on YouTube, Reddit, Wikipedia and LinkedIn correlate more with AI visibility than backlinks, and that few domains are cited by both ChatGPT and Google AI Overviews for the same query - so check each platform separately. Correlation is not proof of cause; say so.

## GEO checklist (a prioritisation heuristic, not a predicted citation rate)

1. **Citability**: a direct 1-2 sentence answer in the first 40-60 words under each question-shaped heading; self-contained passages that make sense when quoted alone; specific numbers with dates and sources; "X is..." definitions; unique data.
2. **Structure**: clean H1-H3, question headings, short paragraphs, tables for comparisons, lists for steps.
3. **Multi-modal**: original images/diagrams with descriptive alt text, video with transcripts.
4. **Authority and presence**: named authors, about/contact pages, consistent brand facts across the web; be present where AI looks (review sites, comparison articles, Reddit/forums, YouTube, Wikipedia-style references).
5. **Technical access**: the AI crawlers the user wants are not blocked in `robots.txt` (e.g. GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended - user's choice; training bots and search/answer bots are different, check the right one for the claim). Key content in server HTML, not only after JS.

**Check visibility**: ask the main buyer questions in the AI assistants the audience uses (or have the user do it) and record who is cited. Report per platform.

## Agent readiness (AI agents browsing and acting on the site)

- Accessibility tree is clean: real buttons/links/labels, form fields with labels, no click handlers on `div`s (check with `take_snapshot` in `build/browser-checks.md`).
- Key actions possible without hover-only menus, infinite scroll traps or CAPTCHA on every step.
- Machine-readable summaries: `/llms.txt` (site summary + key links), clean Markdown or text versions of docs where useful, structured data (`schema.md`).
- Stable, descriptive URLs and predictable navigation.
- Lighthouse in recent Chrome includes agent-browsing checks; run `lighthouse_audit` when the browser plugin is available and report what it measured.

Report honestly: list what was measured and what was not; no invented "AI visibility scores".

Credit: condensed from `claude-seo` (seo-geo, seo-agentic) by AgriciDaniel (MIT) and `ai-seo` by Corey Haines (MIT). Modified.
