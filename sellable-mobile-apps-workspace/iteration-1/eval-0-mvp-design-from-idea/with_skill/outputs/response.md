Good news first: knowing JS is most of the way there. Expo + React Native gets you iPhone and Android from one JavaScript codebase, and it runs on your actual phone over a QR code while you're editing. You don't need to learn Swift or Kotlin, and you don't need a Mac to start.

But before we write a line of code, I want to push back on "where do I start" — because starting with code is the mistake. The thing that kills these projects isn't bad code, it's building in the wrong order. So here's the order, and then the two decisions I need from you.

## Decision 1: how much app do you actually need?

Think of the architecture as a ladder, where each rung adds exactly one capability:

1. Local only, no API, no database
2. Local + API
3. Local + API + database
4. Cloud + API + database
5. Cloud + API + auth + database

Here's the thing about a water tracker: **rung 1 is a shippable product.** Everything lives on the phone. No accounts, no login, no backend, no server bill, nothing to leak. You can put that on both stores and it works.

Adding a database before the design has settled is the single most expensive mistake in this whole process. Once data is live, every layout change that touches it means schema migrations and dead rows. So: build it local, get the design finished, and only add a backend if you later want cross-device sync. Most water trackers never need one.

## Decision 2: design the MVP before building it

Not "spec it." Design it, through five specific slots. When all five are filled, that document *is* the prompt you hand to Claude Code. Here's my draft for yours — correct me where I'm wrong, because these are your calls:

**1. Core function.** The one thing that, stripped of everything else, still makes it the app. For you: *tap a glass, it logs, the day's total goes up.* That's it. Not the settings page, not the charts.

**2. Core loop.** The core function turned into an action-to-reward cycle, ideally under 30 seconds. The reward has to be **sensory, not informational.** A number going from 3 to 4 is informational and forgettable. What you want: the container visibly fills, a haptic thump, a soft water sound, and something that escalates as the day fills up. This is the entire app. If the tap doesn't feel good, nothing else matters.

**3. Accessory features.** Only what feeds the loop. History and a simple weekly chart, custom glass sizes (250ml vs a 750ml bottle), a daily goal. One thing to be explicit about with Claude: water is **volume-based, not binary.** A habit tracker logs "done / not done" once. Yours logs 6-8 times a day toward a target. If you don't say that, you'll get the wrong data model.

**4. Surface area check.** Cap it at 5-7 screens, and honestly a water tracker should be 3-4: home/log, history, settings, onboarding. The test: one run-through should be enough to onboard a new user. Complexity is the default failure here, not a risk. Your entire competitive position is "not bloated" — protect it.

**5. Retention hook.** A deliberate unfinished state that brings people back. The standard move is a 3-day challenge right after onboarding, which works because completing it *requires* three separate sessions across 72 hours.

I'll be straight with you on that last one: engineered incompletion is a manipulation technique. Ordinary, everywhere, and still manipulation. The honest alternatives are streaks the user opts into, notifications they configure themselves, and genuine periodic value (a weekly summary that's actually interesting). Given that your pitch is "the app that isn't trying to squeeze you," the opt-in version might also just be better positioning. Your product, your call — I'll build either.

## Then the order of operations

- **Build.** Dump all five slots into Claude Code as one block and ask for a complete build, not phases. It'll try to split into phases; tell it you want all of it.
- **Design while state is still local.** Screenshot an app whose layout you like, have it emulate that, then change palette, typography and corner radius so it isn't a clone. Two cheap levers that make an app look expensive: *reduce* corner rounding (rounded-everything is the amateur tell), and force every icon and emoji to be monochrome within your palette. Mixed-colour emoji is the number one reason a vibe-coded app looks cheap.
- **Test on three surfaces, in this order:** desktop browser, phone mirror, then the physical phone. The third one is not optional and it matters more for your app than most — haptics, chime audio, push notifications, thumb reach and notch overlap exist *only* on a real device. Your entire reward mechanism is invisible on desktop.
- **Build a dev panel early.** A 3-day challenge can't be QA'd in real time. Ask for buttons that simulate challenge completion, generate 30 days of fake history, and reset onboarding. Testing a simulation beats waiting three days.
- **Security audit, then ship.** Lighter for a local-only app, but still worth two passes.

One concrete trap since you'll hit it: **pin AsyncStorage to v2.2.0.** v3 is incompatible with Expo Go and fails only on device, not in the browser, which makes it maddening to diagnose.

## On the $9.99/mo glass icon

Your irritation is the market position. Lean into it.

Worth knowing: a local-only water tracker has essentially zero marginal cost per user. There's no inference bill, no server, nothing recurring to fund. Subscription is the default for tracker apps mainly when there's an AI or sync cost to cover, and you have neither. So a one-time unlock (roughly $3-5) or free-with-a-generous-tier fits the actual shape of the value, and it's the thing your competitors can't copy without abandoning their revenue model.

Whatever you charge, the placement rule holds: let people complete the core loop for free at least once. Nobody pays for a feeling they haven't had yet.

Flagging my sourcing: the pipeline above is one practitioner's method that I think is sound, and the pricing section is general practice rather than part of it. Treat the money advice as a starting point, not gospel.

## Two things I need from you

1. **Do you own an Android device?** Google Play requires you to verify access to a physical Android phone and test on it. There's no way around it. If you're iPhone-only, that changes your launch plan — you'd ship iOS first and sort Android later. Better to know now than at submission.
2. **Retention hook: 3-day challenge, or opt-in streaks?** This shapes the build, so I'd rather decide it up front than retrofit.

Also budget for store accounts when you get there: Apple's developer program is a yearly fee (around $99 last I checked) and Google Play is a one-time registration (around $25). Both worth verifying at signup since they change.

If you answer those two, I'll write the full MVP spec with all five slots filled, and we can hand it straight to a build. We could have something running on your phone today.
