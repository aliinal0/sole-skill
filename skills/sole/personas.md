# Specialist personas (Agency Agents library, loaded on demand)

[msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (MIT) holds ~300 role prompts ("UX Researcher", "Growth Hacker", "Reality Checker"...). Installing them all as agents would put every description into every session's context, so Sole fetches **one persona only when a task needs that specialist's lens**.

## When to use one

- A second opinion from a specific role (an accessibility auditor reviewing a UI, a paid-media auditor reviewing a campaign).
- A deliverable in a role's established format (a product manager's PRD, a sales discovery call plan).
- Not for simple tasks; Sole modules already cover the method. Personas add a lens, not the process.

## How

1. Fetch the file (pinned version, so links never break):
   ```bash
   curl -s "https://raw.githubusercontent.com/msitarzewski/agency-agents/8ae6164602c95ca78828b148b9052460ee426885/<path>"
   ```
2. Launch a general-purpose subagent whose brief = the persona text + the task + the relevant Sole module path(s) + this skill folder's absolute path. The persona's style applies; Sole's rules (honesty, no invented facts, file locations, safety) still win.
3. Personas describe invented "experience" ("you've fixed 2 million rows"). That is role-play framing: never present it, or anything not verified, as a fact to the user.
4. To browse everything: `curl -s https://api.github.com/repos/msitarzewski/agency-agents/contents/<division>` (divisions: design, engineering, marketing, paid-media, product, project-management, sales, security, strategy, support, testing, specialized, finance, game-development, academic, ...).

## Index by Sole area

| Sole area | Persona (path) |
|---|---|
| UI / design (`build/deslop-ui.md`) | UX Researcher `design/design-ux-researcher.md` · UX Architect `design/design-ux-architect.md` · UI Designer `design/design-ui-designer.md` · Brand Guardian `design/design-brand-guardian.md` · UI Finish-Gate Reviewer `design/design-ui-finish-gate-reviewer.md` · Whimsy Injector `design/design-whimsy-injector.md` |
| Media (`build/deslop-media.md`) | Visual Storyteller `design/design-visual-storyteller.md` · Image Prompt Engineer `design/design-image-prompt-engineer.md` · Short-Video Editing Coach `marketing/marketing-short-video-editing-coach.md` |
| Code | Frontend Developer `engineering/engineering-frontend-developer.md` · Backend Architect `engineering/engineering-backend-architect.md` · Rapid Prototyper `engineering/engineering-rapid-prototyper.md` · Code Reviewer `engineering/engineering-code-reviewer.md` · Senior Developer `engineering/engineering-senior-developer.md` |
| Testing / review (`build/review.md`) | Reality Checker `testing/testing-reality-checker.md` · Accessibility Auditor `testing/testing-accessibility-auditor.md` · Performance Benchmarker `testing/testing-performance-benchmarker.md` · Evidence Collector `testing/testing-evidence-collector.md` |
| Security (`build/security-audit.md`) | Application Security Engineer `security/security-appsec-engineer.md` · AI-Generated Code Security Auditor `security/security-ai-generated-code-auditor.md` · Secrets & Credential Hygiene `security/security-secrets-credential-engineer.md` |
| Ads (`business/ads.md`) | PPC Campaign Strategist `paid-media/paid-media-ppc-strategist.md` · Paid Social Strategist `paid-media/paid-media-paid-social-strategist.md` · Ad Creative Strategist `paid-media/paid-media-creative-strategist.md` · Paid Media Auditor `paid-media/paid-media-auditor.md` · Tracking & Measurement `paid-media/paid-media-tracking-specialist.md` |
| Growth / ideas (`business/ideation.md`) | Growth Hacker `marketing/marketing-growth-hacker.md` · Trend Researcher `product/product-trend-researcher.md` · Product Manager `product/product-manager.md` · Feedback Synthesizer `product/product-feedback-synthesizer.md` |
| SEO / GEO (`business/seo-geo.md`) | SEO Specialist `marketing/marketing-seo-specialist.md` · AI Citation Strategist `marketing/marketing-ai-citation-strategist.md` · Agentic Search Optimizer `marketing/marketing-agentic-search-optimizer.md` · App Store Optimizer `marketing/marketing-app-store-optimizer.md` |
| Social / content | Content Creator `marketing/marketing-content-creator.md` · LinkedIn Content Creator `marketing/marketing-linkedin-content-creator.md` · TikTok Strategist `marketing/marketing-tiktok-strategist.md` · Instagram Curator `marketing/marketing-instagram-curator.md` · Reddit Community Builder `marketing/marketing-reddit-community-builder.md` · Email Marketing Strategist `marketing/marketing-email-strategist.md` |
| Sales | Discovery Coach `sales/sales-discovery-coach.md` · Outbound Strategist `sales/sales-outbound-strategist.md` · Proposal Strategist `sales/sales-proposal-strategist.md` · Offer & Lead Gen Strategist `sales/sales-offer-lead-gen-strategist.md` |
| Research (`research/deep-research.md`) | Research Synthesist `research/research-synthesist.md` · Executive Summary Generator `support/support-executive-summary-generator.md` |
| Projects | Senior Project Manager `project-management/project-manager-senior.md` · Sprint Prioritizer `product/product-sprint-prioritizer.md` · Meeting Notes Specialist `project-management/project-management-meeting-notes-specialist.md` · Experiment Tracker `project-management/project-management-experiment-tracker.md` |

Paths are valid for the pinned version above. If one 404s after a future update of this index, browse the division (step 4).

Credit: persona library by Michael Sitarzewski and contributors, [agency-agents](https://github.com/msitarzewski/agency-agents) (MIT). Not bundled; fetched on demand.
