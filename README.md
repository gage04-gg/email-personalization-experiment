# Is Email Personalization Worth It? A Three-Arm Email Experiment

I analysed a randomized email test on 64,000 customers to find out whether emailing works, whether matching the email to past purchases adds anything, and who should not be emailed at all.

## Why I did this

Most A/B testing projects I found stop at a two-proportion z-test on a landing page. I wanted to analyse an experiment the way an experimentation team or an economist would: write the analysis plan before looking at results, handle three arms and multiple testing, try variance reduction (Lin regression adjustment and CUPED), check results with permutation tests, and end with a business decision (a targeting policy) that is evaluated honestly on held-out data.

## Data

Kevin Hillstrom's **MineThatData E-Mail Analytics Challenge** (March 2008). It is a **public dataset from a US retailer, 2008**, not client work. 64,000 customers who bought in the last year were randomly assigned to a men's merchandise email, a women's merchandise email or no email (1/3 each). Visits, conversions and spend were tracked for two weeks. Details and data-quality checks are in [data_notes.md](data_notes.md).

## Method

1. **Randomization checks** ([01](01_data_and_checks.ipynb)): sample ratio mismatch test (p = 0.90), balance table with standardized mean differences (all below 0.014), joint F-test, and minimum detectable effects.
2. **Pre-registration:** I wrote [analysis_plan.md](analysis_plan.md) and committed it to git *before* calculating any treatment effect. Changes are logged in [decisions_log.md](decisions_log.md).
3. **Main effects** ([02](02_main_effects.ipynb)): difference in means with Neyman SEs, Holm correction for the two primary tests, Lin (2013) regression adjustment with HC2 SEs, CUPED, 10,000-draw permutation tests, a bootstrap CI and winsorizing for spend.
4. **Personalization and heterogeneity** ([03](03_personalization_and_heterogeneity.ipynb)): a pre-registered test of the "matched email" effect, and two pre-registered interactions (newbie, recent buyer).
5. **Targeting policy** ([04](04_targeting_policy.ipynb)): a 50/50 train/test split, per-cell spend uplifts learned on train, and policy value on test estimated with inverse-probability weighting and bootstrap CIs, plus a margin × cost sensitivity table.
6. **Excel profit calculator** ([excel/](excel/), [excel_guide.md](excel_guide.md)): SUMIFS, INDEX/MATCH, a margin × cost sensitivity grid and the held-out results side by side.

## Key results

| Outcome | No email | Mens email | Womens email | Mens effect (95% CI) | Womens effect (95% CI) |
|---|---|---|---|---|---|
| Visit rate (primary) | 10.6% | 18.3% | 15.1% | +7.7 pts (7.0, 8.3) | +4.5 pts (3.9, 5.2) |
| Conversion rate | 0.57% | 1.25% | 0.88% | +0.68 pts (0.50, 0.86) | +0.31 pts (0.15, 0.47) |
| Spend per customer | $0.65 | $1.42 | $1.08 | +$0.77 ($0.49, $1.04)* | +$0.42 ($0.18, $0.69)* |

\* bootstrap CI

![Main effects](figures/main_effects.png)

- **Emailing works.** Both primary tests pass after the Holm correction and in the permutation test.
- **Personalization:** the matching email adds **+3.1 visit points** (CI 2.4 to 3.8). The gain comes from men's-only buyers, who ignore the women's email. Women's-only buyers respond equally to both emails. There is no significant gain in spend.
- **Heterogeneity:** the uplift is the same for new and old customers and for recent and older buyers (both interactions p > 0.4).
- **Targeting:** on held-out data, the learned policy earns $0.341 per customer vs $0.338 for "men's email to everyone". That is the same profit while **not emailing 24.5% of customers**. It clearly wins only when emails are expensive.
- **Variance reduction** cut SEs by only about 1.5% (Lin) and 0.02% (CUPED), because past-year spend barely predicts 2-week spend.

The one-page summary is in [memo.md](memo.md).

## What I would do differently

- Use a pre-period version of the **same** outcome (for example visits or spend in the 2 weeks before the email) for CUPED. The yearly spend figure was almost useless as a covariate.
- Learn the targeting policy with a model that shares information across cells (for example a regression with interactions), because some cells had only about 150 customers per arm and the noise ate most of the targeting gain.
- Track unsubscribes and longer-run revenue, because the real case for sending fewer emails lies there.
- Pre-register the Mens vs Womens comparison as well. I only looked at it as exploratory.

## How to run

```bash
python3 -m venv ~/.venvs/email-experiment
source ~/.venvs/email-experiment/bin/activate
pip install -r requirements.txt

mkdir -p data
curl -L -o data/hillstrom.csv "http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv"

jupyter notebook
```

Then run the notebooks in order, 01 to 04 (Restart & Run All). All random steps use seed 2026, so the numbers reproduce exactly. The CSV is not committed because I could not find clear redistribution terms on the source page. (I keep the virtual environment outside the project folder because Python refuses to create one in a path containing `:`.)

---

*Gandharv Gedam, M.Sc Economics, IIT Kanpur*
