Good news first: **$4.99 covers your API costs by roughly 10–50x.** The cost isn't your problem. Let me show you the arithmetic, then argue that you're asking the wrong question about price, then get to the paywall.

One note on where this comes from: I'm working from a pipeline skill for shipping Expo/Supabase apps, and the monetisation half of it is our own material rather than inherited from the source it's built on. The margin maths and the API prices below are solid; the pricing and paywall judgement calls are opinionated practice, not gospel.

---

## 1. The margin arithmetic

The formula is:

```
per_user_monthly_cost = requests_per_user_per_month × cost_per_request
gross_margin          = net_subscription_price − per_user_monthly_cost
```

Your feature is one nudge per user per day. Call it ~2,000 input tokens (system prompt + that user's recent habit history) and ~200 output tokens (a nudge should be two sentences, not an essay). That's 30 calls/month.

| Model | Input / Output per 1M | Cost per nudge | Cost per user/month |
|---|---|---|---|
| Haiku 4.5 | $1 / $5 | $0.0030 | **$0.09** |
| Sonnet 5 | $3 / $15 | $0.0090 | **$0.27** |
| Opus 5 | $5 / $25 | $0.0150 | **$0.45** |

Now the revenue side, which people usually forget to net down:

- $4.99 gross
- Apple/Google take **15%** if you're in the Small Business Program (under $1M/yr — you qualify, and you have to actually enrol; it isn't automatic)
- → **~$4.24 net to you**

So even on Opus 5, the most expensive option, you're at **~$3.79 gross margin per subscriber**, about 89%. On Sonnet 5 it's ~$3.97. This is a comfortable business, not a knife-edge one.

**Two levers that make it cheaper still, and both fit your architecture perfectly:**

- **Batch API — 50% off.** A daily nudge is the ideal batch workload: it isn't latency-sensitive, nobody is waiting on it. Run one nightly job that generates every user's nudge in a single batch. Halves the numbers above outright.
- **Prompt caching.** Your coaching system prompt is identical for every user; only the habit history varies. If you generate in a batch, the shared prefix caches and re-reads at ~0.1× cost. Put the stable system prompt *first* and the per-user history *last* — caching is a prefix match, so a timestamp or user ID near the top invalidates everything after it.

Between those two, Sonnet 5 lands around **$0.07–0.08 per user per month**. Start on Sonnet 5, and only reach for Opus if the nudge quality genuinely isn't there. Haiku 4.5 is worth a bake-off too — for a two-sentence personalised nudge it may well clear your quality bar at a third of the price. (Heads-up: Sonnet 5's introductory $2/$10 pricing ends 31 Aug 2026, so budget against the standard $3/$15.)

**The number that actually kills margins is the p99, not the mean** — and here's where you're structurally lucky. A once-daily, server-scheduled nudge is inherently bounded: a power user *cannot* cost you 30x the average, because they can't trigger it. Protect that property:

- If you ever add a "regenerate this" button or an AI chat, you've converted a bounded cost into an unbounded one. That's the moment you need per-user server-side rate limits and a monthly generation cap.
- Rate-limit the endpoint server-side regardless. A leaked anon key plus an unprotected edge function is both a security finding and a margin leak.
- Cache the generated nudge in Supabase and serve it from there on every app open. Don't regenerate on each launch.

Don't forget your fixed costs: Supabase Pro is $25/month once you outgrow the free tier. That's your real break-even — roughly **6 paying subscribers**. Everything after that is close to pure margin.

---

## 2. You're asking the wrong question about price

Costs tell you the *floor*. They tell you nothing about the *ceiling*, and at 90%+ margins the floor is irrelevant. Price is a demand question.

So the honest framing: **what does $4.99 signal, and what would $7.99 signal?**

$4.99 is the reflexive indie default. It's under the psychological threshold, it feels safe, and it's what people pick when they haven't decided whether they're selling a utility or a coaching product. A habit tracker with a checkbox is a utility. A habit tracker with a coach that reads your history and writes to you daily is a different category — and the apps in that category (Fabulous, Finch, Rise) price higher.

Some concrete suggestions:

- **Consider $6.99–$7.99/month.** You have a differentiated feature with a marginal cost story; you don't have to compete with free checkbox trackers. Halving your conversion rate at 1.6x the price is roughly break-even — but in practice a modest price increase in this range rarely halves conversion.
- **Ship an annual plan and push it hard.** Something like $39.99/year (a ~50% discount against monthly). Most consumer subscription revenue comes from annual plans, for two reasons: better LTV per acquisition, and it converts your worst problem (monthly churn) into a once-a-year decision. If you only do one thing from this section, do this.
- **Price is the cheapest thing to test and the easiest thing to change.** Launch at one number, watch conversion, adjust. You can't A/B test it cleanly at low volume, so don't agonise — pick $6.99, ship, and revisit at 100 subscribers.

The thing that should *not* drive your pricing: the API bill. At $0.08/user, you could give the AI coaching away on the free tier and it'd cost you $80/month for a thousand free users. Which is a real consideration for the free-tier design below.

---

## 3. Where the paywall goes

**The rule: let the user complete the core loop at least once, for free.** They cannot value what they haven't felt. A paywall before first value converts far worse than one placed just after it.

Your ordering for a habit tracker:

1. **Onboarding — no paywall.** Get them to a configured, personalised state: habits created, reminder time set.
2. **First habit logged — free.** This is the reward moment your whole design exists to produce. Haptics, animation, streak starts. Don't interrupt it.
3. **First real friction point — paywall here.** Typically session two or three, or the moment they hit a free-tier bound.
4. **Retention hook completion — the highest-intent moment in the app.** If you have a 3-day or 7-day challenge, finishing it is when the user has just *proven to themselves* that the app works. That's the best offer placement you will ever get.

**The free/paid split I'd suggest:**

| Free | Paid |
|---|---|
| Up to 3 habits | Unlimited habits |
| 7 days of history | Full history + charts |
| **7 AI nudges** (roughly the first week) | Daily AI coaching, ongoing |

Free-tier bounds that work: limited history depth, a cap on tracked items, a small number of AI generations. Bounds that don't: crippling the core loop itself, which just teaches people the app doesn't work. Never gate the ability to *check off a habit*.

The AI coaching is the right thing to put behind the wall — it's your differentiator, and it's the only thing with a marginal cost. Giving away the first week of nudges is the strongest move available to you: the user experiences the actual product, and the paywall arrives at a moment of demonstrated value rather than a moment of speculation.

**On the day-8 notification.** The tempting design is a push that says "your coach has something for you" which opens to a paywall. That converts well and it's a bait-and-switch — you promised value and delivered a sales page. I'd rather you either (a) show the first line of the actual nudge and paywall the rest, or (b) send an honest "your free week of coaching is up" notification. You'll lose a few points of conversion and gain the ability to read your own reviews. Your product, your call — but you should make it knowingly rather than by default.

**Trial:** a 7-day free trial with the card up front converts substantially better than no trial, and much better than a 30-day one. Requiring the card is the single biggest lever on trial-to-paid. Send a reminder before it converts — it costs a little revenue and saves a lot of chargebacks and one-star reviews.

---

## 4. Implementation notes

**Do not hand-roll StoreKit and Play Billing.** Receipt validation, restore-purchases, cross-platform subscription state, grace periods, refunds, upgrade/downgrade proration — it's a genuine swamp. Use **RevenueCat**: it's the standard abstraction over both stores, the free tier runs well past your first revenue, and it gives you subscription state as one cross-platform source of truth. It's the default for Expo/React Native.

What you still own:

- **Entitlement checks server-side.** This is the one that matters for you specifically. A client-side `if (isPro)` is a suggestion. Your nightly nudge job must query verified subscription state in Supabase (RevenueCat webhooks → your DB) *before* it spends a token on that user. If the check only exists in the app, the paywall is decorative and you're paying Anthropic for free users.
- **Restore purchases must work.** Apple rejects submissions without it. Reliably.
- **Declare every IAP in App Store Connect** before submitting, and make sure your paywall screen shows price, billing period, auto-renew disclosure, and links to your terms and privacy policy. Missing subscription disclosures on the paywall is one of the most common review rejections there is.
- **Handle the lapsed state gracefully.** Read-only access to their existing habit data beats a hard lockout — someone with two years of streak history in your app is a very good win-back candidate, and locking them out of their own data guarantees a bad review.
- Your Supabase RLS policies need to be correct before any of this. If they're default-open, the paywall is the least of your problems.

---

## 5. Instrument before you launch the paywall

Shipping a paywall without analytics means you have nothing to optimise against and no way to tell whether a change helped. The minimum set:

| Metric | Why |
|---|---|
| **Activation** — % completing the core loop once | If this is low, nothing downstream matters. Fix onboarding first. |
| **D1 / D7 / D30 retention** | The direct measure of whether the loop and the nudge actually work. D1 below ~25% means the loop isn't rewarding enough. |
| **Paywall view → trial start** | Tests placement and offer. |
| **Trial → paid** | Tests whether the paid tier is worth it. |
| **Monthly churn** | Under ~5%/month is healthy for consumer subscription; above 10% means you're refilling a leaking bucket. |
| **Cost per active user** | The §1 arithmetic, measured rather than assumed. |

Retention is the load-bearing one. A subscription business with poor D7 is an acquisition treadmill no matter how good the paywall is — and it's also the thing that determines whether an annual plan is honest or predatory.

---

## The order to do this in

Each of these depends on the one before it. Running them out of sequence — usually acquisition before retention — is how apps with good code and real users still make no money.

1. Core loop genuinely rewards → **activation**
2. Retention hook genuinely returns people → **D7**
3. Paywall after first value → **conversion**
4. Batch + cache + server-side entitlement gating → **unit economics**
5. Instrumentation → **knowing which of the above is broken**
6. Acquisition (ASO first — your App Store keywords, title, and screenshots are the free channel) → **only once 1–5 hold**

**Concretely, next week:** wire RevenueCat, put the entitlement check in your nudge edge function, move nudge generation to a nightly Batch API job, add the analytics events above, and pick a price — I'd say $6.99/month with a $39.99 annual and a 7-day card-up-front trial. Then ship it and let the conversion numbers tell you whether the price was right.

Happy to go deeper on any of these — the paywall screen itself, the RevenueCat + Supabase webhook wiring, or the batch job structure.
