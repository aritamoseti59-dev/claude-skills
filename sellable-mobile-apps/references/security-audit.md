# Pre-launch security audit

**[from the course]** — the procedure and vulnerability classes.
**[added]** — the audit prompt text below is reconstructed from the classes and output
format described in the course; the course's own prompt was shown on screen but not read
aloud, so this is our implementation of its stated shape, not a transcription.

## Why this stage exists

Adding a database and auth moved the app from "running on my laptop" to "reachable by
anyone on the internet". Everything that follows is a consequence of that.

The realistic goal is **not** perfect security. It's raising the cost of attacking you above
the cost of attacking the next app. From the course:

> "Get it to the point where somebody would look at your app and say, that's actually pretty
> secure, I don't really think that's worth hacking, let me just move on to the next one
> that's a little less secure."

What's actually at risk, in rough order of how often it bites:
- **Leaked API keys running up your bill.** Providers reimburse loosely at best — it's your
  key. This is the most common and most immediately expensive failure.
- **Cost-exhaustion attacks** — an unprotected endpoint that calls a paid model can be looped
  by anyone who finds it. This is a *margin* problem as much as a security one.
- **User data leaks** — reputational damage that doesn't wash out, plus liability.
- **Regulatory exposure** where health, financial, or bank-connector data is involved.

## When to run it

Only after all three test surfaces (desktop, mirror, physical device) pass and the app is
otherwise launch-ready. Auditing a moving target wastes both passes.

## Procedure

### Pass 1

1. **`/clear` first.** This isn't housekeeping — it's the point. An auditor carrying the
   context of the conversation that wrote the code will rationalise that code. You want it
   reading the repository cold, as an attacker would.
2. Paste the audit prompt (below).
3. Read the findings. Expect 40–60 of them and expect several outright failures. In the
   course's own run: hard-coded secrets passed, but **startup validation**, **protected API
   routes**, **error information leakage**, and **expensive operations** all failed outright,
   with `.gitignore` coverage and console error leaks partial. A clean first pass usually
   means the audit didn't look hard enough.
4. Fix:
   ```
   Run through and fix all of these errors end to end. After you're done, test and ensure
   they're 100% solved.
   ```

### Pass 2 — the part people skip

5. **`/clear` again and run the identical audit prompt from scratch.**

   The reasoning, from the course: *"sometimes in solving one problem, it creates another
   somewhere else... see if a future version of Claude can spot issues that a past version of
   Claude has created."* A model that just wrote a fix is the worst possible reviewer of that
   fix. A cold context is a genuinely independent second reader.

6. Fix again:
   ```
   Great work. Fix all things even if they're partial. Once sorted, let me know if the
   changes produced new vulnerabilities.
   ```

Two passes gets you to roughly "90% satisfied" by the course's estimate. Stop there unless
the app handles sensitive data.

## The audit prompt

```
You are performing a pre-launch security audit of this mobile application codebase. Read the
repository directly — do not rely on anything discussed previously.

Audit against the following classes of vulnerability, which are the ones that most commonly
appear in AI-assisted codebases:

1. HALLUCINATED / UNVERIFIED PACKAGES
   Dependencies that don't exist, are typosquats of real packages, are unmaintained, or were
   invented. Check every import against the lockfile and every lockfile entry against the
   registry.

2. HARD-CODED SECRETS
   API keys, tokens, passwords, connection strings anywhere in source, config, or committed
   history. Verify .env is gitignored and that no secret is reachable from the client bundle.
   Flag any secret that a public-prefixed environment variable would expose to the client.

3. DATABASE POLICY
   Row Level Security enabled on every table. No default-open policies. Every policy actually
   scopes rows to the authenticated user. Check for tables that were added later and missed.

4. AUTHENTICATION AND AUTHORISATION
   Consistent auth middleware across every route and edge function. No endpoint that reads or
   writes user data without verifying identity. Session and token handling. Check that
   authorisation is enforced server-side, not merely hidden in the UI.

5. SERVER-SIDE VALIDATION
   Every input validated on the server regardless of client-side checks. Schema validation on
   all request bodies. Type and range checks on anything reaching the database.

6. EXPENSIVE OPERATIONS / COST EXHAUSTION
   Any endpoint invoking a paid API. Are they authenticated, rate-limited, and bounded in
   size? Could an attacker loop them to exhaust the API budget? This is both a denial-of-
   service and a direct financial exposure.

7. ERROR AND INFORMATION LEAKAGE
   Stack traces, internal paths, database errors, or key fragments reaching the client or the
   console in production builds.

8. STARTUP VALIDATION
   Does the app fail loudly and early when required configuration is missing, rather than
   running in a degraded or insecure state?

9. DEPENDENCY HYGIENE
   Unused dependencies, known-vulnerable versions, and packages with excessive permissions.

For EACH finding, report:
  - SEVERITY: critical | high | medium | low
  - CATEGORY: which class above
  - LOCATION: file and line
  - CWE: the Common Weakness Enumeration identifier
  - VERDICT: pass | partial | fail
  - EVIDENCE: the specific code that led to the finding
  - FIX: the concrete change required

Order the findings by severity, highest first. Conclude with a summary table of every check
and its pass/partial/fail verdict.

Do not fix anything yet. Report only.
```

The final line matters: separating diagnosis from repair keeps the report honest and lets you
see the true starting state before anything is patched.

## Prerequisites set earlier in the pipeline

- **Automatic RLS enabled at Supabase project creation** (Stage 5). Retrofitting row-level
  security onto populated tables is materially harder than enabling it up front.
- **Secrets in `.env`, `.env` in `.gitignore`** from the moment the first key exists.

## Honest limits — say this to the user

Two AI passes remove low-hanging fruit. That is genuinely worth doing and puts the app ahead
of most of what ships. It is **not** a security review.

If the app handles personal health data, financial data, payment credentials, or any OAuth
connector to a bank or third-party account, it needs a human specialist. Say so plainly
rather than letting a passing audit imply a level of assurance it doesn't provide.
