Nice — "works on my phone" is a real milestone, and you're closer than most people who ask this question. But there's a gap between "works" and "submittable", and for your app specifically it splits into two piles:

1. **Things that get you rejected.** Annoying, recoverable, usually a one-round fix.
2. **Things that don't get you rejected but quietly cost you money.** For an app that fires a Claude vision call every time someone photographs a sandwich, this is the pile that actually matters, and it's the one nearly everyone skips.

Let me do pile 2 first, because it's the one you can't fix after launch.

---

## First: where does your Anthropic API key live?

This is the single most important question before you submit anything.

If the vision call goes from the phone directly to the Anthropic API, your key is in the app bundle. Not "hidden in the bundle" — *in* it. Anyone can pull an IPA apart in about ten minutes. And in Expo, anything with an `EXPO_PUBLIC_` prefix is compiled into the client by design, so if Claude wired it up as `EXPO_PUBLIC_ANTHROPIC_API_KEY`, it's already public.

The bill lands on you, and API providers reimburse loosely at best.

The fix is architectural, not cosmetic: the key lives in a **Supabase Edge Function**, the app calls the edge function, the edge function calls Anthropic. Nothing sensitive touches the client. That's the shape you want anyway — serverless, spins up for about a second per call, far cheaper than an always-on server at solo-app scale.

While you're in there, three things on the same endpoint:

- **Require auth on it.** An unauthenticated endpoint that calls a paid vision model is a free vision API for the whole internet.
- **Rate-limit per user, server-side.** Client-side limits are a suggestion. The user who costs you money isn't the average one — it's the person who photographs 200 things a day, or the person who found your endpoint.
- **Cap image size before it goes out.** Vision pricing scales with image tokens. A full-resolution 12MP photo costs meaningfully more than a downscaled one and won't estimate calories any better.

## Second: is RLS actually on, on every table?

Supabase's anon key *is* meant to be public — that part's fine. What makes it dangerous is the combination: **public anon key + a table without row-level security = your entire food log, and possibly your user table, readable by anyone who opens your app bundle.**

Check every table, including any you or Claude added later in the build — those are the ones that get missed. Confirm each policy actually scopes rows to `auth.uid()` and isn't a default-open "allow all authenticated" policy.

And make sure the `service_role` key isn't anywhere in the app. It bypasses RLS entirely.

## Run the full audit, twice, from a cleared context

Don't just check those three things by hand. Run a proper pre-launch audit — and run it from `/clear`, in a fresh session. That's not housekeeping, it's the whole point: Claude reviewing code it just wrote will rationalise it. You want it reading the repo cold.

Ask it to check for hallucinated or typosquatted packages, hard-coded secrets, RLS coverage, auth on every route, server-side input validation, cost-exhaustion on paid-API endpoints, error/stack-trace leakage to the client, startup validation when config is missing, and dependency hygiene. Have it report severity, file, line, evidence and fix — and explicitly tell it **not to fix anything yet**, so you can see the true starting state.

Expect 40–60 findings. A clean first pass means the audit didn't look hard enough.

Then fix them, `/clear` again, and **run the identical audit a second time.** Fixing one thing routinely breaks another, and a model that just wrote a patch is the worst possible reviewer of that patch.

Two passes gets you to roughly "not the easiest target on the street", which is the realistic goal. Be aware that it is *not* a security review — and food and nutrition logs sit in health-adjacent territory. If you ever add HealthKit sync, weight tracking, or anything a regulator would call health data, that deserves a human specialist rather than two AI passes.

---

## Now the rejection pile

These are the "dumb things" you asked about. In rough order of how often they bite:

**A test account for the reviewer.** You have Supabase auth, so an Apple reviewer opens your app and hits a login screen. If you don't give them working credentials in the "Sign-In Required" field in App Store Connect, they literally cannot see your app, and they reject it. This is the most common avoidable rejection there is. Make the account real, seeded with a few logged meals so the app doesn't look empty.

**In-app account deletion.** If users can create an account, Apple requires you to let them *delete* it from inside the app — not via an email request, not via a web form. This one catches a huge number of first submissions. Supabase makes it straightforward via an edge function, but you have to actually build it.

**Camera and photo-library permission strings.** `NSCameraUsageDescription` and `NSPhotoLibraryUsageDescription` need to be in your `app.json` infoPlist and they need to be *specific*. "This app needs camera access" gets rejected. "Used to photograph meals so they can be analysed for nutritional estimates" doesn't. Also check whether your camera setup pulled in microphone permission you don't actually use — declaring a permission you never exercise is its own rejection reason.

**Privacy policy and support page, publicly hosted.** Both are required, both need to be real URLs, ideally on the same domain as your contact email. Yours has a specific disclosure obligation most trackers don't: **user photos leave the device and go to a third-party AI provider.** That must be stated plainly in the policy and declared honestly in App Store Connect's App Privacy section — photos, plus health/fitness data for the nutrition logs. Don't overclaim on retention; state what actually happens.

**Health claims and disclaimers.** A photo-based calorie estimate is an estimate. Say so, in the app and in the store listing. Apple scrutinises anything that could be read as medical measurement, and calorie trackers get extra attention around eating-disorder harm. Don't imply clinical accuracy, don't promise weight-loss outcomes, and set your age rating honestly.

**Sign in with Apple** — only if you offer Google or another social login. If you did, Apple requires an equivalent Apple option alongside it. If you're email/password only, you can skip this.

**Encryption export compliance.** Set `ITSAppUsesNonExemptEncryption` to `false` in `app.json` (assuming you're just using HTTPS, which you are). Otherwise App Store Connect asks you the same question on every single build forever.

**The rest of the App Store Connect form:** screenshots at the sizes the console currently demands (it'll tell you — and Claude can drive a browser through your app to generate them), promotional text, description, keywords, support URL, marketing URL, version `1.0`, copyright, the build tie-in, category, content rights, the gambling declaration, and a **pricing schedule — required even if the app is free.** If you have any paywall, declare the IAPs and make sure "restore purchases" works; Apple rejects without it.

---

## Two more things before you hit submit

**Test the production build, not Expo Go.** If your phone testing was through Expo Go, you haven't yet tested the thing you're shipping. Environment variables resolve differently, native permission dialogs behave differently, dev-only error handling disappears, and the release bundle is a different artifact. Do a full round on an EAS build: photograph real food in bad lighting, kill the network mid-analysis, deny the camera permission and see what happens, check the safe area against the Dynamic Island.

**Don't skip TestFlight.** It's tempting to go straight to submission since it all works. Apple turns TestFlight builds around in about a day and you can invite a lot of people. Real users find things your own testing structurally cannot — and more importantly, TestFlight is where you learn whether the *product* works, not just the code. Watch where testers stall in onboarding and whether they come back on day two.

One practical note on sequencing: EAS free-tier builds sit in a queue. Kick the production build off first, then do the store account setup, privacy policy, and screenshots while it cooks. Don't watch the queue.

---

## The question you didn't ask

If you're launching free with unlimited vision calls, every single user is a cost centre and your best users are your most expensive ones. Worth deciding *now* — before submission, since IAPs have to be declared in the same form — whether there's a bounded free tier (say, a handful of photo analyses a month, shallow history) with a subscription above it. Manual entry stays free, AI photo analysis is the paid feature. That maps cleanly onto where your actual costs are.

If you'd rather ship free first and monetise later, that's a legitimate call — just cap the free usage server-side anyway so the downside is bounded, and put basic analytics in before launch (activation, D1/D7 retention, cost per active user). Shipping without instrumentation means you'll have no idea which part is broken when the numbers disappoint you.

---

**Where I'd start, concretely:** check whether that Anthropic key is in the client bundle. If it is, everything else waits until it isn't. Want me to go look at how the vision call is currently wired up?
