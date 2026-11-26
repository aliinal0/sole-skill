# Security audit - defensive, evidence-first

Find vulnerabilities that cross a real trust boundary, prove them with source evidence, and give the smallest fix. Defensive only: the user's own code, local checks, no attacks on live systems.

## Mode

- **Guidance** (default): a security question, a focused review of one file/feature/PR, or triage of one finding. Use only the relevant parts below. Write no files unless asked.
- **Quick scan**: Phase 1 only (dependencies, secrets, config). Good before every release.
- **Full audit**: only when the user asks for a full/complete audit or a report. All phases, report file at the end.

If unclear which, ask one question.

## Safety rules (every mode)

- Reading source is fine. Run the project's code, tests or PoCs only locally, with dummy data and no external network. (Dependency audit tools such as `npm audit` may contact their public advisory database; that is fine. The project's own code never gets network access during an audit.)
- Never probe deployed endpoints, production data, other people's systems or third-party services. Never print or copy real secrets; show `file:line` and the first 4 characters only.
- Do not modify the target code during an audit; describe fixes. Apply them only when the user asks afterwards.

## Phase 1 - Supply chain and secrets

- Dependencies: run the ecosystem's audit if available (`npm audit --omit=dev`, `pip-audit`, `cargo audit`, `govulncheck`, `bundle audit`); otherwise check lockfiles for known-bad versions with a search. Note unpinned versions and install scripts.
- Secrets: grep for keys/tokens/passwords/private keys and `.env` files tracked by git (`git ls-files | grep -i env`). Check git history only if asked.
- Config: debug mode on, permissive CORS (`*` with credentials), missing security headers, default credentials, open admin routes, overly broad cloud/IAM policies, CI secrets exposed to forks.
- LLM features: prompt injection paths (untrusted text reaching tools or system prompts), model output rendered as HTML, tools with more permission than needed.

## Phase 2 - Code review (OWASP Top 10 lens)

Map entry points first (routes, handlers, CLI args, file/queue consumers, webhooks). For each, follow untrusted input to sinks:
- Broken access control / IDOR: is ownership checked on every object read/write? A route that serves an object by name or id with no owner check is a finding, not a "needs checking" note, when its neighbours scope by user.
- Injection: SQL/NoSQL/OS command/template/LDAP built from input; path traversal; SSRF from user-supplied URLs.
- Auth and sessions: password storage (bcrypt/argon2), token expiry and rotation, JWT `alg`/secret handling, CSRF on cookie auth, rate limiting on login/reset.
- XSS: unescaped output, `dangerouslySetInnerHTML`/`v-html`/`innerHTML`, markdown rendering.
- Insecure deserialization, unsafe file upload (type, size, location, execution).
- Crypto misuse: home-made crypto, ECB, static IVs, `Math.random` for secrets.
- Logging: secrets/PII in logs; missing audit logs for sensitive actions.

Launch one `security-auditor` agent per area or per subsystem, in parallel, for large codebases.

## Phase 3 - Threat model (STRIDE), full audit only

Per component (client, API, DB, queue, third-party): Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. One line each: threat - existing control - gap.

## Phase 4 - Validate every candidate

A finding is **confirmed** only when you can name: the lower-trust actor, the input/action, the control that should stop it, the boundary crossed, and the concrete result (whose data, what action). Otherwise it is:
- **needs validation**: name the exact missing fact (e.g. "depends on proxy config not in repo") - no severity;
- **rejected**: a best-practice gap with no reachable impact.

Have a fresh `security-auditor` agent re-check each confirmed finding against the source before reporting.

Severity (confirmed only, never higher than the demonstrated impact):
- **critical**: unauthenticated code execution, full data-store access, arbitrary account takeover;
- **high**: auth bypass, cross-tenant read/write, stored XSS affecting others, authenticated RCE;
- **medium**: real boundary violation with narrow reach or unusual preconditions;
- **low**: non-secret internals disclosed, minimal gain for effort;
- **info**: hardening note.

## Report

**Only real findings.** Do not pad with generic hardening tips (rate limiting, HTTPS, headers, debug mode, resource leaks) unless the code shows a concrete exploitable path, or the user asked for hardening advice. Missing best practice is not a vulnerability. If useful, end with one line: "Hardening suggestions available on request."

Summary (counts by severity + overall verdict) -> confirmed findings (title, severity, `file:line`, evidence path, impact, smallest fix at the last trusted decision point, regression test idea) -> needs validation -> what was out of scope. Full audits save to `docs/sole/security/YYYY-MM-DD-audit.md` (ask before writing inside the repo; a report describing open vulnerabilities should usually not be committed to a public repo; never include secret values). State clearly that one pass is not exhaustive.

Credit: method condensed from `security-audit` by Cloudflare (MIT) and `security-audit` in Claude-Code-Workflow by catlog22 (MIT). Modified.
