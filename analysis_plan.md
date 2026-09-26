# Pre-registered analysis plan

Written and committed on 26 Sep 2026, **after** the data and randomization checks in `01_data_and_checks.ipynb` and **before** any outcome was compared across arms.

Only the tests in this file are confirmatory. Anything else is labelled **Exploratory**. Any change after this commit goes into `decisions_log.md` with a date and reason before it is run.

## Setup and notation

- Data: Hillstrom MineThatData E-Mail Challenge (public, 2008, US retailer), 64,000 customers.
- Arms: **C** = No E-Mail, **M** = Mens E-Mail, **W** = Womens E-Mail. Random assignment, probability 1/3 each.
- Potential outcomes: Y_i(C), Y_i(M), Y_i(W). Estimands: ATE_M = E[Y(M) − Y(C)] and ATE_W = E[Y(W) − Y(C)].
- Covariates X (all pre-treatment): recency, history, mens, womens, newbie, zip code (Urban and Suburban dummies, Rural is the base), channel (Web and Multichannel dummies, Phone is the base).
- All tests are two-sided. α = 0.05. Every random step uses `np.random.seed(2026)`.

## H1: Does emailing work? (CONFIRMATORY)

- **Primary outcome:** `visit`. **Secondary outcomes:** `conversion`, `spend`.
- **Primary comparisons:** M vs C and W vs C on `visit`. This is 2 tests with a **Holm correction** at α = 0.05.
- **The confirmatory test** is the difference-in-means z-test with the Neyman (unequal-variance) SE. The other estimators below are supporting results.

For each arm vs control and each outcome, report:

1. **Difference in means** with SE = sqrt(s²_T / n_T + s²_C / n_C), a 95% CI and a p-value.
2. **Regression adjustment (Lin 2013):** OLS of Y on the treatment dummy, the centered covariates and treatment × centered covariates, using only the two arms being compared, with **HC2** robust SEs. Report the % reduction in SE compared with the difference in means.
3. **CUPED for `spend`:** θ = Cov(spend, history) / Var(history), estimated on the pooled sample of all three arms. Adjusted outcome = spend − θ · (history − mean history). Report the difference in means of the adjusted outcome and the % reduction in SE.
4. **Randomization inference:** permutation test with 10,000 reshuffles of the arm labels within the two arms being compared. Test statistic: difference in means. p = (number of |permuted diff| ≥ |observed diff| + 1) / (10,000 + 1). Run for `visit` (primary) and for `spend` (secondary, heavy-tailed). As a check, Holm is also applied to the two primary permutation p-values.
5. For `spend`: a **percentile bootstrap 95% CI** for the difference in means (2,000 draws, resampling within each arm), and a robustness check with spend **winsorized at the 95th percentile of positive spend, pooled over all arms** ($362.20). The 99th percentile could not be used because it equals $0 over all customers and equals the source top-code of $499 among buyers (see `decisions_log.md`).

Secondary outcomes are reported with unadjusted p-values and are clearly marked as secondary.

## H2: Is personalization worth it? (CONFIRMATORY, one test)

- **Sample:** customers who bought from only one category last year (mens only, or womens only) **and** got an email (M or W). Control customers and both-category buyers are not in this test.
- `matched = 1` if the email category equals the category they bought before (mens-only buyer got M, or womens-only buyer got W).
- **Model:** `visit ~ matched + mens_only`, OLS with HC2 robust SEs. The confirmatory test is the t-test on the `matched` coefficient.
- Emails are randomized within each past-category group, so the coefficient on `matched` is the causal effect of getting the matching email instead of the other one, averaged over the two groups.
- The same model for `conversion` and `spend` is reported as secondary.
- **Descriptive only (not a test):** visit uplift vs control for each email type in each buyer group (mens only, womens only, both), with 95% CIs, shown in one chart.

## H3: Heterogeneity (pre-specified, only these two)

- Full sample. `email = 1` for M or W, `0` for C.
- Model A: `visit ~ email + newbie + email:newbie`, HC2 SEs.
- Model B: `visit ~ email + recent + email:recent`, where `recent = 1` if recency ≤ 6 months, HC2 SEs.
- The two confirmatory tests are the interaction coefficients, with a Holm correction across the two.
- Nothing else is tested as confirmatory.

## H4: Targeting policy (evaluated on held-out data)

1. Split customers randomly 50/50 into **train** and **test** (`np.random.seed(2026)`, then a random permutation of the rows).
2. **Cells:** past category (mens only / womens only / both) × recent buyer (yes / no) × newbie (yes / no) = up to 12 cells.
3. On **train**, estimate for each cell the uplift in mean spend for M vs C and for W vs C (difference in cell means). Visit and conversion uplifts are also estimated for the Excel sheet.
4. Profit of an action in a cell (per customer) = margin × spend uplift − cost per email. "No email" has profit 0. Base case: **margin 30%, cost per email $0.10** (both are assumptions, not data). The **policy** picks the action (M, W or none) with the highest profit in each cell. Ties go to "none".
5. On **test**, estimate the value of each policy with inverse-probability weighting (propensity = 1/3 for every arm):
   value = mean over test customers of [ 1(assigned arm = policy action) × profit_i / (1/3) ],
   where profit_i = margin × spend_i − cost × 1(customer was emailed).
6. Compare the policy with: **email nobody**, **everyone gets M**, **everyone gets W**, and **random emails** (each customer gets M, W or none with probability 1/3, value = average of the three single-action values). Bootstrap 95% CIs (1,000 draws, resampling test customers, policy kept fixed) for each value and for the difference policy − everyone gets M.
7. Report the **share of customers the policy says to stop emailing** and the profit difference vs "everyone gets M", per customer and scaled to 64,000 customers.
8. **Sensitivity:** margin 20% / 30% / 50% × cost per email $0.05 / $0.10 / $0.50. For each of the 9 combinations the policy is re-learned on train and evaluated on test.
9. The per-cell train estimates go into `excel/email_profit_calculator.xlsx` (input sheet only).

## Exploratory

Any other subgroup, outcome definition or model. It is labelled **Exploratory** in the notebooks, README and memo.
