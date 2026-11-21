# SEO + GEO - classic search, AI search and agent readiness

Entry point for every SEO request. Read only the reference file the command needs.

## Commands

| Command (or plain-language request) | Read | Output |
|---|---|---|
| `audit <url>` - full site audit | all of `business/seo/` as needed, agents in parallel | Health score + prioritised plan |
| `page <url>` - one page in depth | `technical.md` + `content.md` + `schema.md` | Page report |
| `technical <url>` | `business/seo/technical.md` | 9-category technical report |
| `content <url>` / `content-brief <topic>` | `business/seo/content.md` | E-E-A-T review / writer's brief |
| `schema <url>` | `business/seo/schema.md` | Found / valid / missing JSON-LD |
| `images`, `sitemap` | `business/seo/technical.md` | Fix list |
| `geo <url>` / `agentic <url>` | `business/seo/geo-agentic.md` | AI-citation and agent-readiness report |
| `local`, `hreflang`, `ecommerce` | `business/seo/local-intl-ecommerce.md` | Section report |
| `plan`, `cluster`, `programmatic`, `competitor-pages`, `sxo`, `backlinks`, `drift` | `business/seo/strategy.md` | Plan / pages / monitoring |

## Before starting

Site URL, goal (traffic, leads, sales), markets and languages, main competitors, and which data the user can share (Search Console, analytics, an SEO tool export). Without data, work from public pages and say so in the report.

**Detect the business type** from the homepage: SaaS (pricing, features, docs, "free trial"), local service (address, phone, service area, map), e-commerce (products, cart, product schema), publisher (blog, authors, dates), agency (case studies, clients). It changes priorities: local -> also `local`; shop -> also `ecommerce`; blog-heavy -> also `cluster`.

## How to fetch pages

- HTML and headers: `research/web-access.md` (fetch script; Jina for JS-heavy pages).
- What Google actually renders (JS-injected titles, canonicals, JSON-LD), Core Web Vitals lab data, mobile layout: `build/browser-checks.md` when the browser plugin is installed. Without it, say which checks need a rendered view.
- Many pages: `web-fetcher` agents in parallel, each returning only the fields you need.
- Field data (real users): PageSpeed Insights / CrUX public API, or the user's Search Console.

## Full audit flow

1. Detect business type. 2. Launch in parallel (one agent each): technical, content, schema, sitemap+images, GEO/agentic; plus local / ecommerce / cluster / backlinks when relevant. 3. Merge.

## Synthesis rules (every recommendation)

- **Observation** it rests on (what you saw, where).
- **Dependency**: what must happen first, what it unblocks.
- **Falsifiable**: "how would we know this did not work?"
- **Leading indicator** the user can watch without another audit (e.g. impressions for the page in Search Console within 4 weeks).
- Bucket into Critical / High / Medium / Low only after the above.

**Never score what you did not measure.** A health score (0-100) shows each category's score and marks categories that were not checked as "not measured", never as 0 or 100. Quote the date of any statistic or Google policy you cite; SEO facts change monthly.

## Output

1. One-paragraph summary and the 3 highest-impact fixes.
2. Score card per category (or "not measured").
3. Fix list: issue - page(s) - evidence - exact fix - effort (S/M/L) - indicator.
4. Content opportunities if requested.

Write page copy with `write/docs-copy.md` + `write/humanize-text.md`. No promotional footers or links to third-party communities in reports.

## Deeper tooling (optional)

The full Claude SEO plugin adds Google API connectors (Search Console, GA4, PageSpeed), PDF reports, drift databases and paid data sources. If it is installed (its skill appears as `claude-seo:seo`), use its `/seo` commands for those data pulls instead of repeating the work here.

Credit: method condensed from `claude-seo` by AgriciDaniel (MIT), `seo-audit` and `ai-seo` by Corey Haines (MIT) and `seo-geo-claude-skills` by Aaron He Zhu (Apache-2.0). Modified.
