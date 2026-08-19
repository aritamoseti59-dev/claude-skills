# Shipping to the App Store and Play Store

**[from the course]** unless marked otherwise.

Read this before starting submission. Several requirements block you and are easy to
discover too late: a hosted privacy policy, a working test account for the reviewer, and —
for Google Play — a physical Android device.

## Do these in parallel

The production build sits in a free-tier queue for a while. Use that time for the account
and compliance work below rather than watching it.

---

## 1. Prepare for production

Claude generates all of this — you don't hand-write any of it:

| Artifact | Notes |
|---|---|
| `app.json` | App name, bundle identifier, version, icon references |
| `eas.json` | Expo Application Services build configuration |
| App icon | **1024×1024 px** |
| Splash screen | |
| Adaptive icon (Android) | Foreground image on a coloured background, so it works in light and dark mode |
| Permission declarations | Must match what the app actually does — e.g. camera use often also needs audio |
| Runtime version policy | |

Run this as a deliberate final pass even though some of it is generated during development.
The point is confirming everything is present, not creating it from nothing.

```
Generate app.json and eas.json for production. Include the app name, bundle identifier,
version, a 1024x1024 icon, splash screen, and an Android adaptive icon. Check that all
required permission declarations are present for the features this app actually uses.
```

## 2. Build for production

Development builds and production builds are different things. Expo dev is a live version
you edit in real time; the production build **crystallises** it — fixing parameters so it
runs faster and can be distributed.

- `cd` into the project directory first. Running EAS commands from the wrong directory is a
  common and confusing failure.
- Ensure the EAS CLI is installed, then log in (`expo.dev/signup` if needed — though you'll
  already have an account from the Expo Go testing step).
- Free-tier builds queue. Paid builds jump the queue.

## 3. Store accounts

**Apple Developer** — `developer.apple.com/account`
**Google Play Console** — `play.google.com/console/signup`

Two things that save real time:

- ⭐ **Register Play with a business email on your own domain**, not a personal Gmail. A
  Google Workspace account (~$6–7/month) means Google has already verified you, and the
  developer-account verification moves much faster.
- ⚠️ **Google Play requires you to verify access to a physical Android device** and to test
  on it. There is no way around this. If the user only owns an iPhone, surface this early —
  it changes their launch plan.

Both consoles change their flows frequently, so treat any step-by-step as indicative and
follow what's actually on screen.

## 4. Privacy and compliance — the laborious step

Both stores **require a publicly accessible web page** carrying:
- a **privacy policy**
- a **support page**

Ideally on the same domain as your contact email.

The efficient method: feed the store's own published submission guidelines to Claude and
have it generate the pages from those requirements.

```
I'm submitting an app called [NAME] to the App Store. Here are the submission guidelines
[PASTE]. Create a privacy policy and a support page for it.
```

Include honest disclaimers where the app's output is approximate — an AI nutrition estimator
should say estimates are a guide, not a measurement. Reviewers read these, and overclaiming
in a privacy policy is a rejection risk.

## 5. Submit

```
eas submit --platform ios
```

- Choose **select a build from EAS**, pick the build ID
- Log in to the Apple developer account (an existing key on the machine can automate this)
- The App Store Connect API key gets wired up automatically
- Submission takes roughly **3–5 minutes**, then a link opens the App Store Connect page

Expo also supports **over-the-air updates** after launch, which lets you push fixes without
a full resubmission.

## 6. App Store Connect checklist

Work top to bottom. Anything optional is labelled as such — skip those.

| Field | Notes |
|---|---|
| **Screenshots** | Required for the current reference iPhone display size and iPad (larger sizes auto-generate smaller variants). ⚠️ Apple changes the required size with each hardware generation — read the size App Store Connect is asking for rather than trusting any hardcoded value, including this one. ⭐ Claude can produce these by driving a browser through the app |
| **Promotional text** | Short hook shown above the description |
| **Description** | The main sell |
| **Keywords** | ⭐ Your primary free acquisition lever — see `monetisation.md` on ASO |
| **Support URL** | **Required.** The support page from step 4 |
| **Marketing URL** | Your homepage |
| **Version** | `1.0` |
| **Copyright** | Your name or company |
| **Build** | Tie to the build you just submitted |
| ⭐ **Sign-in required** | **A working test account (username + password) for the human Apple reviewer to log into your app.** Forgetting this is a common rejection — the reviewer literally cannot see past your login screen |
| **Release** | "Automatically release this version" is the usual choice |
| **App information** | Name, age ratings, content rights, category |
| **App privacy** | Privacy policy URL and declared data types. (User-privacy-choices URL is optional) |
| **Pricing** | **Required** — you must select a schedule even if free |
| **In-app purchases** | Must be declared clearly if present |
| **Gambling declaration** | Confirm the app is not gambling |

Then **Submit for Review**, top right.

## 7. ⚠️ Common rejection triggers **[added — not from the course]**

The source course covers the submission *mechanics* but not Apple's actual review rules, so
this list is ours. These are the ones that most often bounce an otherwise-working app, and
several are invisible until you're rejected.

**Account and identity**
- **In-app account deletion is mandatory** (guideline 5.1.1(v)) for any app that lets users
  create an account. A "contact us to delete" link does not satisfy it — deletion must be
  reachable inside the app.
- **Sign in with Apple is required** (4.8) if you offer any third-party social login (Google,
  Facebook, etc.). Offering only email/password is fine; offering Google *without* Apple is not.

**Permissions and privacy**
- **Purpose strings must be specific.** `NSCameraUsageDescription` saying "we need your camera"
  gets rejected; it needs to say what for. Same for photo library, notifications, health data.
- **Privacy nutrition labels** in App Store Connect are separate from your privacy policy page
  and must match what the app actually collects.
- **Privacy manifest** (`PrivacyInfo.xcprivacy`) is required, including for third-party SDKs.
- **Disclose third-party AI processing.** If user content goes to an external model API, say so
  in the privacy policy and the labels.

**Purchases**
- **Restore purchases** must be present and working, or IAP apps are rejected.
- **Terms and privacy links must appear at the paywall itself**, not only in settings.
- Digital goods must use IAP. Linking out to an external payment flow is a hard rejection.

**Assets and metadata**
- **The app icon must have no alpha channel / transparency.**
- Screenshots must reflect the actual app — no marketing mockups of features that don't exist.
- No placeholder text, no "beta"/"coming soon" in metadata.

**Content and claims**
- **Health claims** (1.4.1) — a calorie, fitness, or nutrition app must not present estimates as
  medical fact. State clearly that AI-derived figures are approximate.
- **Minimum functionality** (4.2) — thin apps get rejected. This is a real risk for a
  single-purpose tracker; the accessory features from the design framework are what carry it
  past the bar.

**Build and compliance**
- Test the **production EAS build**, not just Expo Go — they behave differently.
- Set the **export compliance** flag (encryption declaration).
- Put the **reviewer's demo credentials in the review notes field**, not just the sign-in fields.

**⭐ The one people miss: reviewers will use your app wrong on purpose.** For anything with a
camera or AI input, a reviewer *will* photograph a stapler and see what your food scanner does.
If it hallucinates a confident calorie count or crashes, that's a rejection. Handle the
low-confidence and unrecognised cases explicitly and gracefully — this is the single most
app-specific thing to get right for AI-vision apps, and it doesn't come up in normal testing
because you only ever photograph food.

## 8. Expectations on review

Acceptance is not guaranteed. What you control is whether the submission is complete — the
pages, the test account, the accurate declarations. If rejected, reviewers usually give
specific remediation guidance; it's normal to go a round or two.

## 9. ⭐ TestFlight — do not skip this

The course skips TestFlight purely because a two-week test period doesn't fit in a video, and
says explicitly that you shouldn't:

> "It's kind of weird to just build the app and then launch it and submit it to the app store
> immediately. Typically you're going to want to do some testing."

TestFlight distributes a private link to real testers before public launch. Apple reviews the
build within ~24 hours and you can invite up to several thousand testers. Real users on real
devices find things three surfaces of your own testing will not.

**[added]** Treat TestFlight as the point where you first learn whether the *product* works,
not just the code. Watch where testers stall in onboarding and whether they return on day two
— those two signals predict retention, and retention is what any subscription depends on.

## 10. Post-launch

App Store Connect surfaces: product page optimization, custom product pages, promo codes,
Game Center, and analytics. This is where you iterate once you have real users.

**[added]** Instrument before you launch, not after — see `monetisation.md`. Shipping without
activation and retention tracking means the post-launch optimisation tools have nothing to
optimise against.
