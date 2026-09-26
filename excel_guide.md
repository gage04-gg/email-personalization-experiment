# Excel profit calculator: how it works

File: `excel/email_profit_calculator.xlsx`. It turns the per-cell uplift estimates from the training half into a targeting decision, and shows how that decision changes with the margin and the cost of an email. Everything is formulas, so changing the two yellow cells updates the whole workbook.

## Sheets

| Sheet | What it does |
|---|---|
| `calculator` | Assumptions, profit of each action per cell, best action, totals, summary and a chart |
| `sensitivity` | The same calculation for 9 scenarios (3 margins × 3 email costs) |
| `inputs` | 24 rows (12 cells × 2 emails) of uplift estimates from `04_targeting_policy.ipynb`, training half |
| `held_out_results` | The policy values on the test half, from `results/policy_values.csv` (the numbers to quote) |

Colour code: blue text = typed-in numbers, green = pulled from another sheet, black = calculated. Yellow fill = assumptions you can change.

## `calculator` sheet, column by column

**Assumptions:** B2 = gross margin (30%), B3 = cost per email ($0.10).

**Rows 6–17 (one row per cell):**

- B, C, D pull customers and the two spend uplifts from `inputs` with SUMIFS. Only one row matches both conditions, so the "sum" is just that value:
  `=SUMIFS(inputs!$I:$I, inputs!$A:$A, $A6, inputs!$E:$E, "Mens")`
- E, F, G = profit per customer of each action. Not emailing costs nothing and gains nothing, so None = 0.
  Mens: `=$B$2*C6-$B$3`, Womens: `=$B$2*D6-$B$3`
- H = best action:
  `=INDEX($E$5:$G$5, MATCH(MAX(E6:G6), E6:G6, 0))`
  MAX finds the highest profit, MATCH finds its position, and INDEX returns the header (None, Mens or Womens). On a tie MATCH returns the first one, so ties go to "None", the same rule as in the notebook.
- I = best profit per customer, J = I × customers (policy), K and L = the profit if the whole cell gets Mens or Womens.

**Summary (rows 21–26):** total profit of the policy, of "everyone Mens" and of "everyone Womens", the policy's gain over "everyone Mens", and how many customers the policy stops emailing.

## `sensitivity` sheet

Row 4 holds the margin and row 5 the cost for each of 9 scenarios. For every cell and scenario:

`=customers × (MAX(0, Mens profit, Womens profit) − Mens profit)`

That is the policy's gain over "everyone Mens" in that cell, with the best action re-chosen in each scenario. The totals in row 19 feed the 3×3 summary table.

In Excel you can build the same grid with **Data → What-If Analysis → Data Table** on `calculator!B24` (row input B3, column input B2). I used plain formulas so the file also works in LibreOffice and Numbers, which don't handle Excel data tables well.

## Check values (base case: 30% margin, $0.10 per email)

- Targeting policy **$10,147**, everyone Mens **$6,974**, everyone Womens **−$99**
- Policy minus everyone Mens: **$3,173**
- Customers not emailed: **15,677 (24.5%)**

| Margin \ Cost | $0.05 | $0.10 | $0.50 |
|---|---|---|---|
| 20% | 1,890 | 2,644 | 23,089 |
| 30% | 2,642 | 3,173 | 19,035 |
| 50% | 4,164 | 4,531 | 14,210 |

## Why Excel shows a bigger gain than the notebook

Excel says the policy beats "everyone Mens" by $3,173 per 64,000 customers, about $0.05 each. The notebook's held-out estimate is only $0.0035 per customer (about $222), with a CI that includes zero.

The difference is the **winner's curse**. The Excel numbers are the same training estimates that were used to *choose* the actions. In any cell where noise happened to make an action look good, that action was picked, so the in-sample profit is biased upwards. The test half never saw the choice being made, so its estimate is the honest one. That's why H4 was evaluated on held-out data. The Excel file shows how the decision works and how it reacts to margin and cost. The realised gain to quote is the one on the `held_out_results` sheet.
