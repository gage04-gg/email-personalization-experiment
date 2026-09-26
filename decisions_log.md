# Decisions log

Every change to the original plan (my project brief) is written here with the date and the reason, before it is run.

## 26 Sep 2026: winsorization cut-off for spend (before the plan was committed)

- **Original idea:** winsorize spend at the 99th percentile.
- **Problem found in `01_data_and_checks.ipynb`:** only 0.9% of customers have spend > 0, so the 99th percentile of spend over all customers is $0. The 99th percentile of positive spend is $499, which is the top-code already in the source file. Both versions would make the robustness check meaningless.
- **Decision:** winsorize spend at the **95th percentile of positive spend, pooled over all three arms** ($362.20). This is written into `analysis_plan.md`.
- **Why this is still honest:** it was decided using only pooled spend, before any arm-vs-control comparison was calculated.

## 26 Sep 2026: small details fixed in the plan (before the plan was committed)

My original project brief left a few details open. They are fixed in `analysis_plan.md` before any treatment effect is calculated:

- The Holm-corrected confirmatory test for H1 uses the difference-in-means z-test with the Neyman SE. Lin regression, CUPED and permutation p-values are supporting results.
- The permutation test is run for visit (primary) and also for spend (secondary, because spend is heavy-tailed and this is where a normal approximation is weakest).
- The H3 interaction tests get a Holm correction across the two interactions.
- The "random emails" benchmark in H4 means each customer gets M, W or no email with probability 1/3 each (the experiment's own policy).
- Ties in the H4 policy go to "no email".
