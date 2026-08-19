# Monetisation

> ## ⚠️ Provenance
>
> **Almost nothing in this file comes from the source course.** Its chapter titled
> "Monetizing Your Skills" is ~90 seconds of advertising for the author's paid community and
> contains no app-monetisation methodology — no paywall, no subscription integration, no
> pricing, no acquisition, no analytics.
>
> The one genuinely useful line, an aside two and a half hours in, is quoted in §1. Everything
> else here is **ours**. Tell the user that when it matters — they should know which advice
> carries the source's authority and which is general practice.

---

## 1. The one thing the course does say **[from the course]**

> "My job is the app dev. Your requests are passed through my Anthropic API key. I pay for the
> usage and then I just charge you a monthly subscription with enough margin to make me some
> delta."

That's the AI-app model in a sentence, and it's correct: **absorb the inference cost, charge a
subscription, price for margin.** The rest of this file is what you need to actually make that
arithmetic work.

## 2. Pick a revenue model **[added]**

Match the model to the shape of the value, not to what's fashionable.

| Model | Fits when | Watch out for |
|---|---|---|
| **Subscription** | Value recurs — tracking, coaching, anything with a streak or history | Needs genuine ongoing value or churn eats you. This is the default for the tracker-shaped apps this pipeline produces |
| **One-off purchase** | Value is delivered once — a tool, a calculator, a utility | No recurring revenue to fund ongoing inference costs. Bad fit for AI features |
| **Freemium** | The free tier is genuinely useful and the paid tier is clearly better | The free tier still costs you inference. Bound it hard |
| **Usage credits** | Costs scale sharply per user and vary a lot | Friction at exactly the moment of use; users hate surprise depletion |
| **Ad-supported** | Very high volume, very low intent | Needs scale most solo apps never reach. Usually the wrong answer |

**Key the choice to the architecture rung, not the app category.** The rung determines whether
you have a marginal cost per user at all, and that changes the answer completely:

- **Rung 1–2 (local, no server-side AI)** — your marginal cost per user is *zero*. A local
  water tracker costs the same whether it has 10 users or 100,000. A subscription here is hard
  to justify to users and hard to sustain, because you're charging rent on something that costs
  you nothing to keep running. **A one-off unlock or a generous free tier with a paid
  convenience layer usually fits better** — and it's a genuine differentiator when every
  competitor charges $9.99/mo for a glass icon.
- **Rung 3–5 with server-side AI** — now every active user has a real recurring cost, and a
  subscription is both defensible and necessary. This is where §3's margin arithmetic applies.

The common mistake is defaulting a tracker-shaped app to subscription because trackers are
usually subscriptions, when the app in question has no recurring cost to fund. Ask what each
active user costs you per month; if the answer is nothing, justify the recurring charge on
value alone or don't charge recurrently.

For an AI-powered tracker on rung 4–5, **subscription with a bounded free tier** is almost
always right.

## 3. ⭐ The margin arithmetic **[added]**

This is the calculation the course gestures at and never performs. Do it *before* building the
paid tier, because it determines what the tier can contain.

**Subtract the store's cut first — it comes off the top, before you see anything:**

```
net_revenue           = subscription_price × (1 − store_cut)
per_user_monthly_cost = requests_per_user_per_month × cost_per_request
gross_margin          = net_revenue − per_user_monthly_cost
```

`store_cut` is **30%** on Apple and Google by default, dropping to **15%** for subscribers
after their first year, and 15% from day one if you qualify for the small-business programmes
(under ~$1M/year — which is most people reading this). Forgetting this is the most common
error in indie app pricing: at $4.99 you are working with roughly **$3.49** in hand, or $4.24
at the 15% rate. Every downstream number depends on getting this right.

Work a real example. A coaching feature that fires daily, ~2k input + 500 output tokens per
call, on a mid-tier model:

- ~30 calls/month/user
- Cost lands in the low tens of cents per user per month
- Against ~$4.24 net at the 15% rate, that's still a healthy gross margin — **but only for the
  average user.**

**The number that kills you is the p99, not the mean.** A power user who triggers generation
30× a day costs 30× the average. Model that user before you price.

**Get real prices before you compute anything.** Model pricing changes and guessing it defeats
the purpose of the exercise — load the `claude-api` skill for current per-token rates rather
than working from memory.

**Two levers dominate this exact workload.** A scheduled, non-interactive AI feature — the
daily nudge, the weekly reflection, anything fired by a cron — is the textbook case for both:

- **Batch API — 50% off.** A daily coaching message has no latency requirement whatsoever. If
  it generates at 3am and the user reads it at 8am, batch processing is free money. Most
  scheduled features in apps built with this pipeline qualify and almost nobody uses it.
- **Prompt caching.** Your system prompt and instructions are identical across every user and
  every run; only the user's data varies. Caching that shared prefix cuts input cost sharply
  at high call volumes.

Together these routinely take a per-user cost from tens of cents to single-digit cents, which
changes what your free tier can afford to include.

Non-negotiable protections:
- **Rate-limit every paid-API endpoint per user, server-side.** The security audit's
  "expensive operations" finding is a margin leak as much as a vulnerability.
- **Cap generations per billing period**, with a clear message rather than a silent failure.
- **Cache aggressively.** A daily reflection should be generated once and stored, not
  regenerated on every app open. The course does this — its coaching message is written to the
  database and reused within a 12-hour window.
- **Use the cheapest model that clears the quality bar**, and re-check that choice as prices
  move.

## 4. Paywall placement **[added]**

Placement matters more than design. The rule: **let the user complete the core loop at least
once for free.** They cannot value what they haven't felt. A paywall before first value
converts far worse than one placed just after it.

Ordering that works for a tracker-shaped app:

1. **Onboarding** — no paywall. Get them to a configured, personalised state.
2. **First core-loop completion** — free. This is the reward moment the whole design exists to
   produce.
3. **First real friction point** — the paywall. Typically the second or third session, or the
   moment they hit a free-tier bound (history depth, number of tracked items, AI generations).
4. **Retention hook completion** — a natural upgrade prompt. Finishing the 3-day challenge is
   the highest-intent moment in the entire app; that's where the offer belongs.

Free-tier bounds that work well: limited history depth, a cap on tracked items, a small number
of AI generations per month. Bounds that don't: crippling the core loop itself, which just
teaches people the app doesn't work.

**Trials.** A 7-day free trial with a card up front converts better than no trial and much
better than a 30-day one. Requiring the card is the single biggest lever on trial-to-paid
conversion. Send a reminder before it converts — it costs a little revenue and saves a lot of
chargebacks and one-star reviews.

## 5. Integration path **[added]**

Do **not** hand-roll StoreKit and Play Billing. Receipt validation, restore-purchases,
subscription state across platforms, grace periods, and refunds are a genuine swamp.

**Use RevenueCat.** It's the standard abstraction over both stores, has a free tier that runs
well past first revenue, and gives you subscription state as a single cross-platform source of
truth. It's the default recommendation for Expo/React Native.

What you still have to get right yourself:
- **Entitlement checks server-side.** A client-side check is a suggestion. Gate the actual
  paid-API call in your edge function on verified subscription state, or the paywall is
  decorative.
- **Restore purchases** must work. Apple rejects submissions without it.
- **Declare all IAPs** in App Store Connect (see `shipping.md`).
- **Handle the lapsed state gracefully** — read-only access to their existing data beats a
  hard lockout, and it converts win-backs better.

## 6. Instrument before launch **[added]**

Shipping without analytics means the post-launch optimisation tools have nothing to optimise
against. The minimum useful set:

| Metric | Why it matters |
|---|---|
| **Activation** — % completing the core loop once | If this is low, nothing downstream matters. Fix onboarding first |
| **D1 / D7 / D30 retention** | The direct measure of whether the retention hook works. D1 below ~25% means the loop isn't rewarding |
| **Paywall view → trial start** | Tests placement and offer |
| **Trial → paid conversion** | Tests whether the paid tier is actually worth it |
| **Monthly churn** | Under ~5%/month is healthy for consumer subscription; above 10% means you're refilling a leaking bucket |
| **Cost per active user** | The margin check from §3, measured rather than assumed |

Retention is the load-bearing metric. A subscription business with poor D7 retention is an
acquisition treadmill, no matter how good the paywall is.

## 7. Acquisition **[added]**

**ASO is the free channel and the one this pipeline already touches.** The submission fields in
`shipping.md` *are* your ASO surface:
- **Keywords** — the highest-leverage field. Research what people actually search, not what you
  call your product internally
- **Title and subtitle** — carry the most ranking weight
- **Screenshots** — the actual conversion driver on the store page. Lead with the core loop's
  reward moment, not a settings screen
- **Ratings** — prompt for a review *after* a reward moment (challenge completion), never on
  cold launch

Beyond ASO, the realistic options for a solo builder are building in public, a narrow community
where the problem is felt acutely, and content demonstrating the core loop. Paid acquisition
rarely works before you know your LTV, and you don't know your LTV until you have churn data —
so it belongs after §6, not before.

## 8. Sequence

Get these in order; each depends on the one before:

1. Core loop that genuinely rewards → **activation**
2. Retention hook that genuinely returns people → **D7**
3. Paywall placed after first value → **conversion**
4. Margin protection and caching → **unit economics**
5. Instrumentation → **knowing which of the above is broken**
6. Acquisition → **only once 1–5 hold**

Running these out of order — most commonly acquisition before retention — is how apps with good
code and real users still make no money.
