Nice — "works on my phone" is genuinely the hard part. But there's a gap between that and "passes review," and most of it isn't code. Here's what I'd work through, roughly in order of how likely it is to bite you.

## First: the one that isn't about Apple at all

**Is your Anthropic API key in the app bundle?** If you're calling the Claude API directly from the Expo client, that key is extractable — `EXPO_PUBLIC_*` vars and anything bundled into JS can be pulled out of the IPA in about five minutes. Apple won't reject you for it, but someone will find it and run up your bill.

The fix is a Supabase Edge Function that holds the key server-side. The app sends the photo (or a signed storage URL), the function calls Claude, returns the result. While you're in there, add per-user rate limiting — a cap on analyses per day — because otherwise one enthusiastic user or one scraper is your whole month's budget.

Related: **check that RLS is enabled on every table.** The Supabase anon key is public by design. If any table is missing a row-level security policy, anyone with your anon key can read your entire user base. Go through the table list in the Supabase dashboard one by one and confirm each has RLS on with policies that actually scope to `auth.uid()`. This is the single most common way indie Supabase apps leak data.

## The rejection triggers that are specific to your app

**Account deletion (Guideline 5.1.1(v)).** If users can create an account, you must let them delete it *from inside the app* — not "email support," not "visit our website." It has to delete the account and the associated data. This is one of the most common rejections for apps with auth, and it's a hard requirement, not a suggestion. Add a Delete Account option in settings, with a confirmation, that actually removes the Supabase auth user and their rows.

**Sign in with Apple (4.8).** If you offer Google sign-in (or Facebook, or any third-party login), you must also offer Sign in with Apple. If you only have email/password, you're fine and don't need it.

**Camera and photo permission strings.** Your `NSCameraUsageDescription` and `NSPhotoLibraryUsageDescription` need to be specific about *why*. "This app needs camera access" gets rejected. "Take photos of your meals so they can be analyzed for nutrition information" passes. Set these in `app.json` under `ios.infoPlist`.

**Health claims (1.4.1 / 5.2.x).** Calorie trackers sit near a line. Don't present the numbers as medical advice, don't diagnose anything, don't make claims about treating conditions. Add a plain disclaimer somewhere visible — "estimates only, not medical advice, consult a professional" — both in the app and in the App Store description. Also think about whether you want to be careful around weight-loss framing; apps in this space sometimes get pushed to a higher age rating, and Apple has been touchier about anything that could read as encouraging disordered eating.

**What happens when the reviewer photographs their desk.** This is the app-specific one people miss. App Review will not photograph a balanced meal on a nice plate. They'll photograph the ceiling, a keyboard, a coffee cup, a blurry hand. If Claude hallucinates "Grilled Chicken Salad — 420 cal" for a photo of a stapler, or the app throws an unhandled error and freezes, that's a 2.1 rejection for bugs. Make sure your prompt includes an explicit "if this isn't food, say so" escape hatch, that your parsing handles that response, and that the UI shows something graceful like "couldn't identify food in this photo — try again."

**Network failure and slow responses.** Reviewers test on bad connections and in odd states. Vision calls take a few seconds — make sure there's a loading state, a timeout, and a recoverable error rather than a spinner that never ends. Airplane-mode the app yourself and tap through everything.

## The review submission mechanics

**A demo account in the App Review Notes.** If there's a login wall, the reviewer needs working credentials. Put a real, working email and password in the notes field — not a placeholder — and verify it logs in right before you submit. Missing or broken demo credentials is an instant rejection and costs you a full review cycle.

Also use that notes field to tell them how to use the app: "Tap the camera button, photograph any food item or a photo of food on screen, results appear in 3-5 seconds." Reviewers are on a clock and won't hunt for your core feature.

**Test the actual production build, not Expo Go.** This is the classic Expo trap. Expo Go and a release build are different environments — env vars resolve differently, EAS secrets have to be configured separately, native modules behave differently, and code that works in dev mode can crash in release. Do an `eas build --profile production`, push it to TestFlight, install *that* on your phone, and run through the whole app fresh. Things that break here: missing EAS secrets, dev-only fallback URLs, console logging that masked an error, and Hermes behaving differently than the dev bundle.

**Export compliance.** Set `ITSAppUsesNonExemptEncryption: false` in your `app.json` infoPlist unless you're doing custom crypto (HTTPS doesn't count). Otherwise every single submission stops to ask you about it.

**Privacy manifest.** Expo handles the app-level `PrivacyInfo.xcprivacy` on recent SDKs, but if you pulled in third-party SDKs check they ship their own. Missing required-reason API declarations get flagged at upload now, not at review.

## Store Connect paperwork

- **Apple Developer Program** — $99/yr, and enrollment can take a few days (longer if you enroll as a company and need a D-U-N-S number). Start this now if you haven't.
- **Privacy policy URL** — mandatory for every app, no exceptions. Yours needs to disclose that meal photos are sent to a third-party AI provider (Anthropic) for analysis, what's stored, and how long. Be honest about this; the App Privacy questionnaire is a legal declaration and mismatches between it and your actual behavior are a rejection.
- **App Privacy "nutrition labels"** — fill these out to match reality. You're collecting: email/user ID (linked), photos (linked, unless you delete them post-analysis), health/fitness data (calories, weight if you track it). Under-declaring is worse than over-declaring.
- **Support URL** — required. A simple page with an email address is enough.
- **Screenshots** — at minimum the 6.9" iPhone set. If you don't want iPad, set the app to iPhone-only in the target settings; otherwise you need iPad screenshots *and* the app must actually work properly on iPad, which is extra surface area to get rejected on.
- **App icon** — 1024×1024, no alpha channel, no transparency, no pre-rounded corners. Alpha channel in the icon is an automatic upload failure.
- **Age rating questionnaire** — answer it honestly, including anything about health/medical themes.
- **Description and keywords** — no "beta," no "coming soon," no mentions of features that don't exist yet, no mentioning Android or other platforms, no using competitors' trademarked names (don't write "like MyFitnessPal") in the description or keywords.

## If you're charging money

If there's any paid tier, it has to go through Apple's IAP — no Stripe, no external checkout links, no "subscribe on our website" (3.1.1, and they enforce it aggressively). Subscriptions additionally need:

- A **Restore Purchases** button in the app
- Subscription title, duration, and price clearly shown *before* purchase
- Links to your **Terms of Use (EULA)** and **Privacy Policy** both inside the app near the paywall and in the App Store Connect metadata fields

Missing restore button and missing terms links near the paywall are two of the most common subscription rejections.

If it's free for now, skip all of that — but note that adding IAP later means another review.

## Worth doing even though it isn't required

- **Crash reporting** (Sentry has a solid Expo integration). Right now if the app crashes for a user you'll never know.
- **Delete or expire the stored photos** after analysis if you don't need them. Less data stored is less privacy surface, cheaper storage, and a simpler privacy policy.
- **Bump version and build numbers** properly — EAS can auto-increment, but confirm it's on, because a duplicate build number is a wasted upload.
- **A real onboarding path.** Reviewers open your app cold with no data. Empty states that say nothing, or a first screen that requires data you haven't got, read as "broken."

## The short version

If I had to pick the four most likely to get you bounced: **in-app account deletion**, **working demo credentials in the review notes**, **generic permission strings**, and **the app misbehaving on a non-food photo**. And the one that won't get you rejected but will hurt more: **that API key needs to be behind an Edge Function before anyone else installs this.**

Want me to go through the actual project and check any of these — the RLS policies, the permission strings, where the API key is currently living, whether account deletion exists?
