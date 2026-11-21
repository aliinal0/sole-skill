# Technical SEO

Score each category 0-10 only if you checked it. Evidence = URL + what you saw.

## 9 categories

1. **Crawlability**: `robots.txt` (no accidental `Disallow: /`, sitemap listed), status codes (no 4xx/5xx on internal links, no redirect chains > 1 hop), orphan pages, crawl depth (key pages <= 3 clicks from home).
2. **Indexability**: `noindex` mistakes, canonical points to itself or the right master, duplicate/near-duplicate pages, parameter URLs, soft 404s, thin pages (see `content.md` quality gates).
3. **Security**: HTTPS everywhere, HTTP -> HTTPS 301, no mixed content, HSTS, valid certificate.
4. **URL structure**: short, lowercase, hyphens, descriptive, stable; no session IDs; one URL per piece of content.
5. **Mobile and page experience**: viewport meta, readable font size, tap targets >= 24 px, no intrusive interstitials, no horizontal scroll.
6. **Core Web Vitals** (75th percentile of real users): LCP <= 2.5 s, INP <= 200 ms, CLS <= 0.1 (poor: > 4.0 s, > 500 ms, > 0.25). INP replaced FID in March 2024; never cite FID. LCP = TTFB + resource load delay + resource load duration + element render delay; fix the biggest part first. Lab data (Lighthouse, DevTools) diagnoses; field data (CrUX, Search Console) is what ranks. CWV acts mostly as a tie-breaker between similar-quality pages.
7. **Structured data**: present, valid, matches visible content -> `schema.md`.
8. **JavaScript rendering**: compare raw HTML with the rendered DOM (title, meta description, canonical, H1, links, JSON-LD). Content or links that exist only after JS are at risk. Use `build/browser-checks.md` for the rendered view.
9. **IndexNow / Bing**: optional instant URL submission for Bing/Yandex; suggest for sites that change often.

## Images

Descriptive `alt` (empty `alt=""` only for decoration), modern format (WebP/AVIF), sized to display (responsive `srcset`/`sizes`), explicit width/height (prevents CLS), `loading="lazy"` below the fold, **never** lazy-load the LCP image; LCP image gets `fetchpriority="high"`, others `decoding="async"`; descriptive file names; served from a CDN when traffic is high.

## Sitemaps

Valid XML, only 200-status canonical indexable URLs, `<lastmod>` real (not "today" on every URL), <= 50,000 URLs / 50 MB per file (else a sitemap index), listed in `robots.txt` and submitted in Search Console. Image/video/news extensions only when relevant.

## Agent-friendly pages (short)

Real `<button>`/`<a>`/`<label>` elements, a clean accessibility tree, server-rendered key content: the same things that help screen readers help AI agents browse the site. Details in `geo-agentic.md`.

## Output

`Technical score: XX/100 (N of 9 categories measured)`, then a table per category: status, top issues with URLs, exact fix, effort.

Credit: categories and thresholds condensed from `claude-seo` (seo-technical, seo-images, seo-sitemap, CWV reference) by AgriciDaniel (MIT). Thresholds per Google's published Core Web Vitals definitions.
