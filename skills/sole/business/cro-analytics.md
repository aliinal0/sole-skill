# CRO and analytics

## Find the leak before fixing

1. Map the funnel: visit -> key page -> signup/add-to-cart -> activation/checkout -> paid/repeat.
2. Get numbers per step (analytics export, or ask the user). The biggest drop with the most traffic is the first target.
3. Look for *why*: session recordings, heatmaps, on-page surveys, support tickets, form-field drop-off.

## Common fixes by step

- **Landing page**: headline states the outcome for a specific person; proof near the CTA; one primary action; page speed.
- **Signup**: fewer fields, social login, no forced credit card unless intended, clear error messages.
- **Activation**: get the user to the first real result in minutes; empty states that show what to do; checklist.
- **Checkout**: total cost up front, guest checkout, trust signals, saved cart.

## Testing

- Hypothesis: "Because [data], changing [X] for [audience] will improve [metric] by [estimate]."
- One change per test unless traffic is high enough for multivariate.
- Check the volume first: write the monthly count of the exact metric a test would move ("30 paid conversions a month") and say plainly whether it is enough. Under ~1,000 conversions/month, prefer bold changes, a higher-volume step and qualitative checks over micro A/B tests.
- Write the sample size and duration into the plan before the test starts; do not stop early on a lucky day.

## Tracking hygiene

Define events once (name, trigger, properties) in a tracking plan; use UTM conventions; verify events fire before trusting a report.

## Output

Prioritised list: issue, evidence, fix, expected impact, effort, how to measure.
