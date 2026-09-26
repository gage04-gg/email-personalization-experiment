# Memo: Is email personalization worth it?

**Data:** Kevin Hillstrom's MineThatData E-Mail Challenge. It is a public dataset from a US retailer in 2008, not client work. 64,000 past customers were randomly split three ways: a men's merchandise email, a women's merchandise email, or no email. Visits, purchases and spend were tracked for two weeks.

**Question:** Does emailing work, does matching the email to what a customer bought before add anything, and who should the company stop emailing?

**Answer in one sentence:** Emailing clearly works, and the men's email works best for almost everyone. Matching the email to past purchases raises visits, but a targeting rule built on it earns about the same profit as simply sending the men's email to everyone, while sending **25% fewer emails**.

## Three findings

1. **Emailing drives traffic and sales.** The men's email raised the two-week visit rate from 10.6% to 18.3% (+7.7 points, 95% CI 7.0 to 8.3). The women's email raised it to 15.1% (+4.5 points). Both pass a Holm-corrected test and a 10,000-draw permutation test. Spend per customer rose by $0.77 (men's, bootstrap CI $0.49 to $1.04) and $0.42 (women's), from a base of $0.65.
2. **Personalization helps visits, but lopsidedly.** For customers who bought from only one category, the matching email lifted visits by 3.1 points more than the non-matching one (CI 2.4 to 3.8, pre-registered test). The gain in spend (+$0.21) was not significant. The descriptive split shows why: men's-only buyers hardly respond to the women's email (+1.1 points vs +6.9 for the men's email), while women's-only buyers respond equally to both (+7.1 vs +7.4).
3. **The uplift is the same for new and old customers, and for recent and older buyers.** Neither pre-registered interaction is significant (Holm p = 0.98). Segmenting on these two variables alone does not change the size of the email effect.

## Targeting recommendation

I learned a rule on half the customers (12 cells: past category × recent buyer × newbie) and evaluated it on the other half, assuming a 30% margin and $0.10 per email.

- The rule earns **$0.341 per customer**, against $0.338 for "men's email to everyone" and $0.189 for "email nobody". The gain over blanket emailing is +$0.0035 per customer (CI −$0.07 to +$0.07): **no measurable profit gain**.
- The rule **stops emailing 24.5% of customers** (about 15,700 of 64,000): both-category older newbies, men's-only older repeat customers, and women's-only recent repeat customers. It sends the women's email to 22% and the men's email to the rest.
- **Recommendation:** send the men's email as the default. Adopt the targeting rule where sending volume has a cost that this 2-week profit misses (unsubscribes, spam complaints, list fatigue): it keeps the same profit with a quarter fewer messages. When emails are expensive ($0.50 each), blanket emailing loses money and the rule is clearly better (+$0.27 per customer at a 30% margin).

## Limits

- A 2008 US retailer and a 2-week window. Long-run effects, including unsubscribes, are not observed.
- Margin and email cost are assumptions. The sensitivity table covers 20–50% margin and $0.05–$0.50 per email.
- Only 0.9% of customers bought, so spend effects are noisy. Some policy cells had about 150 customers per arm in training, which limits how much targeting can gain.
- Covariate adjustment (Lin, CUPED) cut SEs by only 0.02–1.5%, because past-year spend barely predicts 2-week spend (correlation 0.02).

## What this means for Indian e-commerce CRM

Apps like Meesho, Myntra and Swiggy send push notifications, WhatsApp messages and emails at huge volume. Every message has a direct cost (business messages on WhatsApp are charged by Meta), and too many irrelevant messages push users to mute notifications, block the business number or uninstall. Three lessons carry over. First, measure incremental impact against a randomized hold-out group, not raw open or click rates. Second, "personalized" content should be tested, not assumed: here matching helped for one customer group and not the other. Third, once a message has a real cost (money or opt-outs), a targeting rule that removes non-responders can keep the same revenue with far fewer sends, but judge it on held-out data, because in-sample estimates overstate the gain.
