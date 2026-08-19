Good news: this is close to the ideal first app. It's small, it has no server, no login, no payments, and you already know the only language you need. Let me split your question into two, because they have very different answers.

**"How do I get this running on my own phone?"** — a weekend, maybe less.

**"How do I get it into the App Store and Play Store?"** — a few weeks, most of which is paperwork and waiting, not code.

Almost everyone who bounces off mobile does it because they conflate those two and try to solve store logistics on day one. Don't. Build the thing you'll actually use first.

## The stack

Since you write JS: **React Native with Expo**. Not a debate for your situation. Expo is a framework/toolchain on top of React Native that handles the native build stuff you don't want to learn yet, and one codebase gives you both iPhone and Android.

Getting started is genuinely this short:

```
npx create-expo-app@latest water
cd water
npx expo start
```

Install "Expo Go" from the App Store on your phone, scan the QR code that appears in your terminal, and your app is running on your actual phone. Save a file, it hot-reloads. That loop — real device, instant refresh — is the thing that makes this fun instead of miserable.

Two flavours of React Native that will confuse you when you Google things: **Expo** and **bare/CLI React Native**. Older blog posts push you toward bare because Expo used to be limited. That hasn't been true for years. Stay in Expo.

If you know React, you know 80% of this already. The main adjustments: `<View>` instead of `<div>`, `<Text>` instead of `<p>` (and *all* text must be inside a `<Text>`, which will bite you once), styles are JS objects with a flexbox subset, and there's no CSS cascade. `expo-router` gives you file-based routing like Next.js if you want it, though a water tracker might genuinely be one screen.

## Scope for v1

Be ruthless here. Your v1 is:

- A number: how much you've drunk today.
- Two or three buttons that add a fixed amount (glass, bottle, mug).
- An undo, because you'll misclick.
- A goal, and something visual that fills up as you approach it.
- Resets at midnight.

That's it. No history screen, no charts, no settings, no reminders yet. You can build that in an evening or two, and then you'll have the far more valuable thing: an app you've used for a week that tells you what it actually needs. My guess is you'll discover the fixed amounts are wrong for you and undo matters more than you thought, and you'd never have learned that from planning.

**Storage:** you do not need a backend, a database server, or accounts. Use `@react-native-async-storage/async-storage` — it's basically `localStorage`. Store a JSON object keyed by date (`{"2026-08-13": 1400}`). If you later want a year of history and charts, move to `expo-sqlite`, but you probably won't need to. Resisting the urge to add a backend is the single biggest reason your project will survive.

**The midnight reset:** don't use a timer. Store the date with the total and compare against today's date whenever the app opens. Timers die when the app is backgrounded, and this is the classic beginner trap.

## Where you'll actually hit friction

**Notifications.** This is the one feature you'll want that isn't trivial. `expo-notifications` handles local scheduled reminders ("drink water" at 10am, 2pm, 4pm), but notification support inside the Expo Go sandbox has been progressively cut back, so you'll probably need to make a *development build* — basically your own custom version of Expo Go with your native dependencies compiled in. `npx expo run:android` or a cloud build via EAS. It's an afternoon of yak-shaving the first time and painless after. Just know it's coming, and don't let it be week one.

**iOS without a Mac.** If you're on Windows or Linux, you can still build for iPhone: **EAS Build** compiles on Expo's cloud machines. But putting an app on a real iPhone at all — even just your own — requires an Apple Developer account at **$99/year**. Android is **$25 once**. So if budget matters, ship Android first and add iOS when you're convinced the thing is real.

**The Play Store's tester requirement.** New personal Google Play developer accounts have to run a closed test with a minimum number of real testers (it's been 12 people for 14 continuous days) before you're allowed to publish publicly. It catches everyone off guard. If store release is your goal, start recruiting friends early, because it's a wall-clock delay you can't code your way around.

**Apple's "minimum functionality" rule.** Guideline 4.2 lets them reject apps they consider too simple or web-page-like. A single-screen water tracker is exactly the shape that gets flagged. The defence is polish and platform integration: a home screen widget, decent notifications, a history view, animations that feel considered, an app icon that isn't a default. Doing that work also happens to be what makes an app pleasant, so it's not wasted.

## Concretely, this week

1. Tonight: `create-expo-app`, get the default screen running on your phone via Expo Go. Just that. Prove the loop works.
2. Replace it with a big number and a "+250ml" button that increments it in React state. Nothing persisted.
3. Add AsyncStorage so it survives a restart.
4. Add the date check and the goal ring or bar.
5. Use it for a week. Write down what annoys you.

Then come back and we can talk about notifications, widgets, and whether you want to go through store submission at all.

One last thing, since you flagged it: your read on that market is right. Hydration is full of apps that either bolted a glass of water onto a calorie tracker or want a subscription for a counter and a timer. There's real room for something that costs five dollars once, or is free with a small one-time unlock for widgets and history. Not a get-rich thing — a "a few hundred people a month happily pay for the honest version" thing. But that's a conversation for after you've been using it yourself for a month. Build it for you first; you're a legitimate member of the target audience, and that's a better starting position than most people have.
