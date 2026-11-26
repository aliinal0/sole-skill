# SEO strategy - plans, clusters, programmatic pages, comparisons, SXO, backlinks, monitoring

## `plan` - strategic SEO plan

Business type -> goals and KPIs -> current baseline (pages, rankings or impressions if available) -> competitor gap (`business/competitor.md`) -> 90-day roadmap: technical fixes first, then content clusters, then authority. Each item with owner, effort and leading indicator.

## `cluster` - topic clusters from real SERPs

1. Expand the seed keyword into 30-100 related queries (autocomplete, "people also ask", related searches, the user's Search Console queries).
2. Group queries that share several top-10 results (SERP overlap) - same results = same page; different results = different pages.
3. Label intent per group.
4. Hub-and-spoke: one pillar page per main topic, spokes for subtopics; every spoke links to the hub and to 2-3 sibling spokes.
5. Output: table (cluster - target query - supporting queries - intent - page type - new/existing URL) + internal link matrix.

## `programmatic` - pages at scale

Safe at scale: integration pages with real setup docs, templates/tools, glossary terms with real definitions, product pages with unique data, user-generated profiles. Risky: city-swapped location pages, "best X for [industry]" with no industry-specific content, "[competitor] alternative" without real comparison data, mass AI text. Require a real data source per page, a uniqueness check, canonical and sitemap plan, and start with a small batch whose indexing you measure before scaling.

## `competitor-pages` - "X vs Y", "alternatives to X", roundups

Facts from each product's own site with dates; neutral tone; a feature table that also lists where the competitor is better; clear "who should choose which"; Product/SoftwareApplication or ItemList schema only with real data. Never invent pricing, ratings or claims.

## `sxo` - search experience

Look at what Google already ranks for the query (page type, format, depth). If the user's page is a different type (a product page where guides rank, or the reverse), fix the page type before polishing the copy. Derive 3-5 user stories from the SERP and check the page answers each one.

## `backlinks`

Free signals: Common Crawl domain data, Bing Webmaster Tools, Moz free metrics, the user's Search Console "Links" report; paid tools only with the user's account. Look at referring-domain quality and relevance, anchor-text spread, lost/new links, competitor gap. Disavow only for clear manipulative links or a manual action. **Do not score what you did not measure.**

## `drift` - catch SEO regressions

Before a release or redesign, save a baseline to `.sole/seo-baseline/<host>.json` for the key URLs: status, title, meta description, canonical, robots, H1, JSON-LD types, internal link count, word count. After the release, compare and report changes by severity (lost canonical/noindex/404 = critical; title or schema change = high; copy length = low).

Credit: condensed from `claude-seo` (seo-plan, seo-cluster, seo-programmatic, seo-competitor-pages, seo-sxo, seo-backlinks, seo-drift) by AgriciDaniel (MIT). Modified.
