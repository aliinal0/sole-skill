# Structured data (Schema.org JSON-LD)

## Detect and validate

1. Read JSON-LD from the **rendered** page when possible (`build/browser-checks.md`: run `evaluate_script` returning all `script[type="application/ld+json"]` contents); raw HTML misses JS-injected markup.
2. Each block: valid JSON, `@context` https://schema.org, correct `@type`, required properties present, values match visible content (price, rating, author, dates). Markup that describes things not on the page is a spam signal.
3. Recommend Google's Rich Results Test and the Schema.org validator for final confirmation.

## Which types to recommend (status as checked by Claude SEO in October 2026 - re-verify before quoting)

- **Recommend freely**: Organization, LocalBusiness (and subtypes), WebSite, WebPage, BreadcrumbList, Article / BlogPosting / NewsArticle, Person, ProfilePage, Product / ProductGroup / Offer (+ shipping and return policy), Review / AggregateRating (real reviews only), SoftwareApplication / WebApplication, Service, Event, VideoObject (+ Clip, SeekToAction), Recipe, JobPosting, Course, DiscussionForumPosting, QAPage.
- **No rich result, keep if already useful**: FAQPage (Google retired FAQ rich results for all sites in May 2026 - flag at Info level, do not tell people to add it for SERP features).
- **Never recommend (deprecated)**: HowTo (rich results removed Sept 2023), SpecialAnnouncement, CourseInfo, EstimatedSalary, LearningVideo, VehicleListing, Practice Problem; ClaimReview only for fact-checking publishers (no Search rich result).
- **Not deprecated despite rumours**: Book Actions; Dataset (used by Dataset Search).

## Generate

- One `@graph` per page, stable `@id`s (`https://site.com/#organization`), connect Organization -> WebSite -> WebPage -> main entity.
- Prefer server-rendered JSON-LD; for shops, product markup injected by JavaScript can be read less reliably by Shopping crawls.
- Never invent ratings, reviews, prices or awards. Leave a property out rather than guess.

Output: table of found / valid / errors / missing-but-recommended, then ready-to-paste JSON-LD blocks.

Credit: type-status lists condensed from `claude-seo` (seo-schema) by AgriciDaniel (MIT). Modified.
