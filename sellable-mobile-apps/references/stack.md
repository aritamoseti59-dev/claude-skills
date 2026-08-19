# Stack specifics

**[from the course]** unless marked otherwise.

## Framework choice

**Expo + React Native** — JavaScript/TypeScript, one codebase targeting iOS, Android, and web.
Cloud builds via EAS. Large ecosystem. Hot reload on device, which is what makes the test loop
tolerable.

Alternatives the course explains and rejects:

| Option | Why rejected |
|---|---|
| **Flutter + Firebase** | Dart is an unfamiliar language for most; Google's Material design is opinionated and limits your look; pushes you toward a Firebase decision early. Genuinely good if you want native ARM performance and don't mind the design constraints |
| **Capacitor** | Easiest of the three — build a website, wrap it for the stores. Good if you already have a web app. Web-first rather than app-first |

The pipeline itself is stack-agnostic. If the user already knows Flutter, the eight stages
apply unchanged.

## Version gotchas

- ⚠️ **AsyncStorage v3 is incompatible with Expo Go.** Pin **v2.2.0**. This surfaces as an
  `uncaught in promise` error plus a `getItem` failure on device — confusing, because it works
  fine in the browser.
- **Expo tunnel suspension.** Creating many tunnel servers in quick succession triggers an
  anti-spam suspension that presents as `Commander failed to start tunnel`. Fix: verify your
  Expo account email. Nothing in the error suggests this.
- **`supabase login` fails in the Claude Code terminal** — it needs a TTY. Run it in a separate
  terminal, complete the browser auth, then tell Claude `logged in`. Terminal instances share
  credentials, so it can proceed from there.

## Device testing loop

1. Install **Expo Go** (App Store / Play Store), create an account, log in
2. Have Claude start the dev server in a **new terminal window** — inline gives no scannable QR
3. Scan the QR with the phone camera or Expo Go
4. App runs on the real device with hot reload

Early runtime warnings on first launch are normal. The course's advice — let it self-heal,
re-run a couple of times, and focus on core functionality before chasing warnings — is sound.

## Supabase setup

At project creation:
- **Project name**
- **Database password** — weak ones are rejected
- **Region** — pick the one nearest your users; distance is latency and it's painful to change
- **Enable the Data API** (auto-expose new tables)
- ⭐ **Enable automatic RLS** — this is what prevents the default-open-policy finding in the
  security audit

Wait for all health checks: database, PostgREST, Auth, Realtime, Storage, Edge Functions.

**Local-first caching** is the architecture to specify: keep AsyncStorage as the immediate read
layer so the app feels instant, sync to Postgres periodically. Round-tripping every read to the
network is the difference between snappy and laggy.

A typical generated schema for a tracker-shaped app:
- `habits` — name, emoji, type, reminder settings
- `completions` — date, count, habit_id
- `challenges` — name, habit_id, start_date, duration, completion, reward_claimed
- `profiles` — user-level extras beyond the auth record

**[added] Secrets.** Keys go in `.env`; `.env` goes in `.gitignore`. The publishable/anon key is
designed to be public — the direct connection string and database password are not, and neither
belongs in a chat window. The course demonstrates otherwise while telling you not to; follow
what it says.

**Email confirmation.** The course disables it to cut signup friction. Reasonable for a demo;
for anything shipping, weigh it against unlimited fake signups.

## AI feature architecture

The shape generalises to any third-party API feature:

```
mobile app
   ↓ fires on a schedule
Supabase Edge Function      ← serverless, ~1s invocation
   ↓ reads
Postgres                    → compiles a data package
   ↓ sends package + prompt
Claude API (Sonnet)
   ↓ returns generated content
Postgres (cached)
   ↓
Edge Function → app → push notification + in-app display
```

**Why Edge Functions rather than an always-on server:** they spin up for about a second, fire,
and stop. At solo-app scale an always-on server costs far more for the same work.

**Cache the generated content.** Write it to the database and reuse it within a sensible window
(the course uses ~12 hours for a daily coaching message). This is a correctness decision and a
margin decision at once — see `monetisation.md` §3.

**Sample the output before shipping it.** Ask for 10 examples and tune the runtime prompt
against their range. You cannot prompt-engineer something you've only seen once.

## Working practices

- **`/init`** after the first rough build → generates CLAUDE.md → then **`/clear`**. Re-run
  `/init` when the MVP is complete
- **`/compact`** at 250–300k tokens. Quality degrades noticeably past ~200k, particularly for
  fine-grained edits. Compaction roughly halves the length while preserving the content — do
  other work while it runs
- **`Ctrl+O`** shows what documentation and skills Claude actually loaded
- **~20k tokens is the floor** on any new session — CLAUDE.md, file reads, and tool definitions
- **Queue messages** rather than waiting; unrelated tasks don't need to be serialised
- **GitHub early.** You're letting an agent edit the codebase, so you want a cheap path back to
  a working state. Note that renaming a project folder ends the current Claude session

## Design tooling

- Generate a colour scale (the course uses UI Colors), paste the whole palette in at once
- **Reduce** corner rounding for a higher-end feel — heavy rounding is the default look
- Monochrome icons and emoji drawn from the palette; mixed-colour emoji is the most common
  reason a vibe-coded app looks cheap
- **Chrome DevTools MCP** lets Claude screenshot and self-correct autonomously. Reach for it
  when the same text instruction bounces twice — that's misunderstanding, not disobedience
