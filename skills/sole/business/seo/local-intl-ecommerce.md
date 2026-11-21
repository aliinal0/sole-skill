# Local, international and e-commerce SEO

## Local SEO

Type: brick-and-mortar (customers visit), service-area business (you visit them; hide address), or hybrid.

| Area (rough weight) | Check |
|---|---|
| Google Business Profile (25%) | Verified, primary category exact, secondary categories, hours incl. holidays, photos, services/products, posts, Q&A |
| Reviews (20%) | Count, rating, recency, replies to reviews (especially negative), no gating or incentives |
| Local on-page (20%) | City/area in title and H1 where natural, real local content, embedded map, click-to-call |
| NAP consistency (15%) | Name, address, phone identical on site, GBP and major directories |
| Local schema (10%) | LocalBusiness subtype, address, geo, openingHours, `sameAs` to profiles; one entity per location |
| Local links (10%) | Local press, associations, sponsorships, chambers of commerce |

Multi-location: one page per real location with unique content (see location-page limits in `content.md`).

## International (hreflang)

1. Every page lists itself (self-reference) and all alternates; every alternate links back (return tags).
2. `x-default` for the language selector or global fallback.
3. Valid codes: ISO 639-1 language (`en`), optional ISO 3166-1 region (`en-GB`, not `en-UK`).
4. Hreflang URLs are the canonical, indexable, 200-status versions; same protocol and host format.
5. Use one method consistently (HTML head, HTTP headers or sitemap).

Common mistakes: missing return tags, hreflang to redirected/noindex URLs, language detection redirects that hide alternates from Googlebot.

## E-commerce

Product page checklist: unique title and description (no manufacturer copy), real photos (multiple angles, zoom), price and availability visible, Product + Offer schema with shipping and return policies, reviews with AggregateRating only if genuine, breadcrumbs, internal links to category and related products, canonical for variants (or ProductGroup), out-of-stock pages kept with alternatives (not 404) when the product returns.

Category pages: unique intro text, faceted navigation that does not create infinite indexable URL combinations (canonical or `noindex` for filters), pagination crawlable.

Marketplace and Google Shopping data (prices, competitors) need paid data sources; offer, do not assume.

Credit: condensed from `claude-seo` (seo-local, seo-hreflang, seo-ecommerce) by AgriciDaniel (MIT). Modified.
