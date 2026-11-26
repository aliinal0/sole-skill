# Ads - campaigns, copy and creatives

## Before starting (ask only what is missing)

1. Goal: awareness, leads, sales, installs? Target CPA/ROAS if known.
2. Product and offer: what, price, the one reason to buy now.
3. Audience: who, what they already believe, what they fear, where they hang out.
4. Current state: running ads? Best and worst performers, budget, platforms.
5. Constraints: brand rules, legal/claims limits, languages.

If `.sole/CONTEXT.md` or a positioning doc exists, read it instead of asking.

## Platform choice

| Platform | Best when |
|---|---|
| Google Search | Demand exists - people already search for the solution |
| Meta (FB/IG) | Visual product, broad consumer audience, creative-led testing |
| TikTok | Young audience, native-looking video, fast creative churn |
| LinkedIn | B2B, job-title targeting, high ticket |
| X / Reddit | Niche communities, technical or opinionated audiences |

Start with one or two platforms. Spread budget thin across five and nothing learns.

## Structure

- Campaign = objective. Ad set = audience/budget. Ad = creative.
- Naming: `platform_objective_audience_angle_date` so reports read themselves.
- Meta today rewards broad targeting + many distinct creatives; the creative *is* the targeting. Test angles, not tiny copy tweaks.
- Budget split to start: ~70% proven, ~20% new angles, ~10% wild tests.

## Copy

Generate by **angle**, then variations per angle. Angles: pain, desired outcome, objection killer, social proof, comparison, curiosity, offer/urgency, identity ("for people who...").

Frameworks: PAS (problem-agitate-solve), AIDA, Before-After-Bridge, "feature -> so that -> benefit".

Rules:
- Hook in the first line / first 2 seconds.
- One idea per ad. Concrete numbers and nouns over adjectives.
- Write the way the customer talks (mine reviews, Reddit, support tickets for exact phrases).
- Check every variation against platform limits (e.g. Google RSA headline 30 chars, description 90).
- Only facts the user gave go into copy. A claim you would like to use but cannot support (a user count, a rate such as "10,000 steps = 50p", an integration, a partner name, "busier than ever", a review score, a fundraising target the user did not set, a first-person quote or testimonial nobody gave, "no sign-up", "on iOS and Android") goes in a short "facts to confirm" list under the ads, never into the copy itself.
- Pass final copy through `write/humanize-text.md`. Ad copy is where AI phrasing ("Unlock", "Elevate", "Seamless", "Game-changer") kills trust fastest.

## Creatives

- Video: hook (0-3 s) -> problem -> product in use -> proof -> CTA. Native look beats polished.
- Static: one message, readable at thumbnail size, product visible.
- Visual rules: `build/deslop-media.md`.

## Iterating from data

1. Rank by the goal metric, not CTR alone.
2. Winners: what angle, hook, format? Make 3-5 new variations of each winning angle.
3. Losers: kill, and note why in the test log.
4. Record the learning in `.sole/CONTEXT.md` -> `## Decisions`.

## Output

A table per angle: hook / primary text / headline / CTA / creative idea / platform. Then a test plan with budget and the metric that decides, then the "facts to confirm" list if there is one.

Credit: adapted from `ads` and `ad-creative` by Corey Haines (MIT).
