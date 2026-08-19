Good news first: the API cost almost certainly isn't your problem. But the thing you're *actually* worried about (unit economics) has a landmine in it that isn't the one you're looking at. Let me do the maths and then get to the pricing and paywall stuff.

## The API cost, roughly

One nudge a day. Call it ~2,000 input tokens (system prompt, the user's habits, streaks, recent completion history, tone preferences) and ~200 output tokens for a short personalised message. That's ~66k tokens in and ~6k out per user per month.

At roughly current per-million rates (check these before you rely on them, they move):

| Model tier | ~Cost per user per month |
|---|---|
| Haiku-class | ~$0.09 |
| Sonnet-class | ~$0.27 |
| Opus-class | ~$1.35 |

Now the other side. At $4.99 you don't get $4.99. Apple/Google take 30%, or 15% if you're enrolled in the App Store Small Business Programme / Play's reduced rate, which you will be under $1M a year. So you're netting about $4.24 per subscriber per month.

So: $4.24 revenue against $0.27 of inference is a ~94% gross margin. Even on an Opus-class model you're at ~68%. Add Supabase (free tier until you have real traction, then $25/mo flat) and Expo push notifications (free) and your fixed costs are noise. **One nudge a day is a cheap feature.** You could charge $2.99 and still be fine on cost.

## The actual landmine

Cost per *paying* user is not the number that matters. Cost per *user* is.

If AI nudges go to everyone on the free tier and 3% of your users convert (which is a normal-to-decent consumer app number), then every paying subscriber is subsidising ~32 free users. At Sonnet-class rates that's 32 × $0.27 = **$8.64 of cost against $4.24 of revenue.** You'd be upside down, and the more successful the app gets the faster you bleed.

Two rules fall out of this:

1. **AI coaching is a paid feature, or a trial feature, never an indefinitely-free one.** Free users get tracking, streaks, charts, reminders. That's a complete, genuinely useful free app. The coach is what they're buying.
2. **Generate nudges server-side.** Supabase edge function on a cron, key in the environment, never in the client bundle. If your Anthropic key ships inside the Expo app, someone will find it and your cost model stops being a spreadsheet exercise. Also put a hard per-user daily cap in the function so a bug can't loop.

If you later add anything conversational — "chat with your coach" — redo this whole calculation, because unbounded turns per user is where AI app economics actually go wrong. Meter it (e.g. 20 coach messages a month) from day one rather than retrofitting a limit onto users who got used to unlimited.

## On the $4.99

Cost isn't the reason to move off it. Churn is.

Consumer subscription apps churn somewhere around 8-15% a month. At 10%, your average monthly subscriber sticks around ~10 months, so a $4.99/mo subscriber is worth about $42 gross, ~$36 after store fees. That's your entire budget for acquiring them, and if you ever want to spend money on ads it's thin.

A few things I'd push you on:

**You're probably underpriced, not overpriced.** Habit trackers with AI features cluster around $5-10/month and $30-60/year. $4.99 doesn't read as "cheap and appealing" to a consumer, it reads as "this is a small thing." Price is a signal about how much the app is going to do for you. I'd test $7.99 or $8.99 monthly.

**Sell the annual plan, hard.** This is the single biggest lever for an app like yours. A $49.99/year plan collects ~$42 net up front and completely sidesteps the month-3 churn cliff. Habit apps are seasonal-intent purchases — people buy in January, or the Monday after a bad week — and annual captures the full value of that motivation spike. Structure it so annual looks obviously correct: $8.99/mo or $49.99/yr ("save 54%"), with annual pre-selected. Expect most of your revenue to come from annual.

**Consider a lifetime tier.** $99 or $129. A small but real slice of habit-tracker buyers hate subscriptions and will happily pay once. Cash up front, and your marginal cost to serve them is under $4/year. Only do this once you're confident about the ongoing cost profile.

**Don't discount early.** Launch discounts train people to wait and permanently anchor your price low. Use a free trial instead.

## Where the paywall goes

The honest answer is that you should end up with more than one, at different points, but here's where I'd start.

**Onboarding paywall, after the setup flow, before the home screen.** Let them pick their habits and set their goals first — that's a few minutes of investment and a moment where they've just articulated what they want to change, which is the highest-intent point in the entire lifecycle. Then show the paywall. Offer a 7-day free trial with the reminder toggle on (Apple/Google will notify them before the charge). Make it dismissible with a visible, non-dark-pattern close button. A hard wall converts a bit better on paper but kills your top of funnel, your reviews and your word of mouth, and for a habit app the free user who tells a friend is worth a lot.

**Then a second trigger at the first real value moment.** For your app that's the moment the AI would produce a genuinely good nudge — day 3 or 4, when there's enough history that the coaching isn't generic. Show them the nudge, partially, and paywall the rest. "Your coach noticed something about your Tuesday evenings." That converts far better than a paywall shown before the app has any data to be impressive with.

**And one on the streak-break.** When someone misses two days, that's when they most want help and most doubt themselves. A gentle "want your coach to help you restart?" is well-timed rather than exploitative, as long as the copy is kind.

Practical bits: use RevenueCat rather than wiring StoreKit and Play Billing yourself — free under $2.5k monthly tracked revenue, saves you weeks, and gives you the cohort analytics you'll need. You must use in-app purchase for this; you can't route it through Stripe inside the app. And build the paywall so the price, trial length and feature list come from remote config, because you will want to change them without shipping a build and waiting on review.

## What to actually watch

Ignore revenue for the first couple of months and watch four numbers: install → trial start, trial → paid conversion (under 40% means the trial isn't demonstrating value fast enough, so move the paywall later or improve the day-1 nudge quality), D30 retention among payers, and blended API cost per active user. If D30 retention is bad, no pricing change saves you — that's a product problem wearing a pricing problem's clothes, and it's worth fixing before you spend anything on acquisition.

If you tell me your rough onboarding flow and what the nudge prompt looks like, I can get more specific about where the trial breaks and what the free tier should hold back.
