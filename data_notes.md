# Data notes

## Source

- Kevin Hillstrom, "MineThatData E-Mail Analytics And Data Mining Challenge", MineThatData blog, March 2008.
- Blog post: https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html
- File: http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv
- Downloaded on 26 Sep 2026 and saved as `data/hillstrom.csv` (3.96 MB).
- Public dataset from a US retailer, 2008. This is not client work.

## Licence / terms

The blog post shares the file openly for the challenge and invites people to analyse it and share findings. I could not find an explicit licence or redistribution terms on the page. Because this is unclear, the CSV is **git-ignored** and the README gives the download command instead of committing the file.

## Basic facts (checked in `01_data_and_checks.ipynb`)

- 64,000 rows, 12 columns, exactly as documented.
- No missing values.
- 6,562 rows are exact duplicates of another row. There is no customer ID and the covariates are coarse (recency is a whole number of months, and history is often repeated), so this is expected and not a data error. All rows are kept.
- `zip_code` values are `Urban`, `Surburban` (misspelled in the source) and `Rural`. I kept the source spelling in the code.
- `channel` values: Phone (28,021), Web (28,217), Multichannel (7,762).
- `recency` runs from 1 to 12 months. `history` runs from $29.99 to $3,345.93 (mean $242.09, median $158.11).
- `mens` and `womens` are never both 0. So every customer is in exactly one of: mens only (28,818), womens only (28,734), both (6,448).
- `newbie`: 32,144 new customers, 31,856 not new.

## Arm sizes

| Arm | Customers |
|---|---|
| Mens E-Mail | 21,307 |
| No E-Mail | 21,306 |
| Womens E-Mail | 21,387 |

SRM chi-square against 1/3 each: 0.20, p = 0.90.

## Outcomes (pooled over all arms only, before the plan)

- Visit rate 14.68%, conversion rate 0.90%, mean spend $1.05.
- Spend > 0 exactly when conversion = 1 (578 buyers). Every converter also visited.
- Spend among buyers: min $29.99, median $80.80, mean $116.36, max $499.00.
- **Spend is top-coded at $499 in the source file** (12 buyers are exactly at $499).
- Because only 0.9% of customers bought, the 99th percentile of spend over all customers is $0, and the 99th percentile of positive spend is $499 (the cap). A 99th-percentile winsorization would therefore do nothing useful. See `decisions_log.md`.
