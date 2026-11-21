# Design references - learn from real systems, never clone them

The open collection [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (MIT) holds `DESIGN.md` analyses of well-known product sites: colours, type, spacing, elevation, radius, motion. Sole does not ship them; it fetches the one you need on demand (cheaper and always current).

## Fetch one

```bash
curl -s "https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/<name>/DESIGN.md"
```

If that 404s, list the folder names first:
```bash
curl -s "https://api.github.com/repos/VoltAgent/awesome-design-md/contents/design-md" | grep '"name"'
```

Names include (not exhaustive): airbnb, airtable, apple, cal, clickhouse, cohere, coinbase, cursor, elevenlabs, expo, figma, framer, hashicorp, ibm, intercom, linear.app, lovable, mintlify, miro, mistral.ai, mongodb, notion, nvidia, ollama, posthog, raycast, replicate, resend, revolut, sanity, sentry, shopify, slack, spotify, stripe, supabase, superhuman, uber, vercel, warp, webflow.

Read only the sections you need (e.g. `## Typography`, `## Colors`) with `grep -n` + a line range; these files are ~500 lines.

## How to use a reference (transpose, not clone)

1. Name what you admire in one line ("Stripe's restraint: one accent, generous whitespace, precise type scale").
2. Extract the **principle**, not the values: scale ratio, density, how accents are rationed, elevation approach.
3. Rebuild it with the client's own subject, palette and type. Different hues, different typefaces, different signature move.
4. Never copy a brand's logo, exact palette, typefaces, copy, illustrations or signature effect, and never make a page that could be mistaken for that brand.
5. Record the reference and what was transposed in `DESIGN.md` -> "References (transposed, not copied)".

Two or three references from **outside** the client's category usually produce more original results than one from inside it.
