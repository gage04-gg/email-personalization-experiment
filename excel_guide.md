# Excel guide: build the email profit calculator yourself

Start file: `excel/email_profit_calculator.xlsx`. It has one sheet, `inputs`, with 24 rows (12 cells × 2 email types) of uplift estimates from the **training half**:

| Column | Content |
|---|---|
| A `cell` | e.g. `mens only / recent / newbie` |
| B `past_category` | mens only / womens only / both |
| C `recent_buyer` | 1 = last purchase ≤ 6 months ago |
| D `newbie` | 1 = new customer |
| E `email` | Mens or Womens |
| F `customers` | customers in this cell in the full 64,000 |
| G `visit_uplift` | visit rate of this email minus control, in the cell |
| H `conversion_uplift` | same for conversion |
| I `spend_uplift` | same for spend ($ per customer) |

A finished reference version is in `excel/email_profit_calculator_solution.xlsx`. Build yours first, then compare.

---

## Step 1: New sheet and assumptions block

1. Right-click the `inputs` tab → **Insert** → **Worksheet**. Rename it `calculator` (double-click the tab).
2. In `calculator`:
   - A2: `Gross margin`, B2: `0.30`. Format B2 as a percentage: **Home → Number → %**.
   - A3: `Cost per email ($)`, B3: `0.10`.
3. Colour B2 and B3 light yellow with blue text (**Home → Fill Color** and **Font Color**). This is the usual convention for input cells.

## Step 2: The list of cells

1. In row 5 type these headers, A5 to L5:
   `Cell | Customers | Mens spend uplift | Womens spend uplift | None | Mens | Womens | Best action | Best profit per customer | Total profit, policy | Total profit, everyone Mens | Total profit, everyone Womens`
2. Copy the 12 unique cell names into A6:A17:
   - Go to `inputs`, select A2:A25, and copy it.
   - Paste it into `calculator` A6.
   - With the pasted range still selected, choose **Data → Remove Duplicates** (untick "My data has headers"). 12 names should remain, in A6:A17.

## Step 3: Pull the numbers in with SUMIFS (or XLOOKUP)

In row 6, then fill down to row 17 (select B6:D6 and double-click the small square at the bottom-right corner):

- B6 (customers):
  `=SUMIFS(inputs!$F:$F, inputs!$A:$A, $A6, inputs!$E:$E, "Mens")`
- C6 (Mens spend uplift):
  `=SUMIFS(inputs!$I:$I, inputs!$A:$A, $A6, inputs!$E:$E, "Mens")`
- D6 (Womens spend uplift):
  `=SUMIFS(inputs!$I:$I, inputs!$A:$A, $A6, inputs!$E:$E, "Womens")`

SUMIFS adds up column I over rows where the cell name matches **and** the email matches. Exactly one row matches, so the sum is just that value.

**XLOOKUP version** (Excel 365 or 2021+), for C6:
`=XLOOKUP(1, (inputs!$A$2:$A$25=$A6)*(inputs!$E$2:$E$25="Mens"), inputs!$I$2:$I$25)`
Multiplying the two TRUE/FALSE tests gives 1 only where both conditions hold, and XLOOKUP finds that 1.

The `$` signs matter. `$A6` keeps the column fixed but lets the row move as you fill down. `inputs!$F:$F` never moves.

## Step 4: Profit per customer of each action

Profit per customer = margin × spend uplift − cost per email. Not emailing costs nothing and earns no uplift, so its profit is 0.

- E6: `0`
- F6: `=$B$2*C6-$B$3`
- G6: `=$B$2*D6-$B$3`

Fill down to row 17.

## Step 5: Best action per cell

- H6: `=INDEX($E$5:$G$5, MATCH(MAX(E6:G6), E6:G6, 0))`
  - `MAX(E6:G6)` finds the highest profit.
  - `MATCH(..., 0)` finds its position (1, 2 or 3). On a tie it returns the first match, and "None" comes first. That is the same tie rule as the notebook.
  - `INDEX` returns the header in that position: None, Mens or Womens.
- **IF version** (same result):
  `=IF(AND(E6>=F6, E6>=G6), "None", IF(F6>=G6, "Mens", "Womens"))`
- I6: `=MAX(E6:G6)`
- J6: `=I6*B6` (total profit of the chosen action in this cell)
- K6: `=F6*B6` (total profit if this cell gets the Mens email)
- L6: `=G6*B6` (total profit if this cell gets the Womens email)

Fill down to row 17.

## Step 6: Totals and the comparison with "email everyone"

- A18: `Total`. B18: `=SUM(B6:B17)` (should be 64,000). Copy B18 to J18, K18 and L18.
- Summary block, starting at A20:
  - A21 `Targeting policy`, B21 `=J18`
  - A22 `Everyone gets Mens`, B22 `=K18`
  - A23 `Everyone gets Womens`, B23 `=L18`
  - A24 `Policy minus everyone Mens`, B24 `=J18-K18`
  - A25 `Customers not emailed`, B25 `=SUMIFS(B6:B17, H6:H17, "None")`
  - A26 `Share not emailed`, B26 `=B25/B18` (format as %)

These are **incremental** profits compared with emailing nobody, over the 2-week window.

## Step 7: Two-way data table (margin × cost per email)

1. Pick an empty area, for example A30.
2. In A30 type `=B24`. This is the output the table will recalculate.
3. In B30, C30 and D30 type the costs: `0.05`, `0.10`, `0.50`.
4. In A31, A32 and A33 type the margins: `0.20`, `0.30`, `0.50`.
5. Select A30:D33.
6. **Data → What-If Analysis → Data Table**.
   - **Row input cell:** `B3` (the costs run across the row)
   - **Column input cell:** `B2` (the margins run down the column)
7. Click OK. Excel fills B31:D33 by putting each margin and cost into B2 and B3, recalculating the whole sheet, and reading off B24. The best action per cell changes with the assumptions, and the table captures that.
8. Optional: format A30 with a custom format `;;;` so the corner cell looks empty.

(The reference solution uses plain SUMPRODUCT formulas for this grid, because a real Data Table cannot be created from Python. The numbers are the same.)

---

## Check values (your file should show these)

Base case (margin 30%, cost $0.10):

| Cell | Mens profit / customer | Womens profit / customer | Best action |
|---|---|---|---|
| both / older / newbie | −1.0348 | −0.8950 | None |
| both / older / old customer | 0.3480 | −0.1000 | Mens |
| both / recent / newbie | 0.3233 | −0.0206 | Mens |
| both / recent / old customer | 0.6552 | −0.6357 | Mens |
| mens only / older / newbie | 0.4012 | −0.0257 | Mens |
| mens only / older / old customer | −0.0685 | −0.1237 | None |
| mens only / recent / newbie | 0.0490 | 0.0380 | Mens |
| mens only / recent / old customer | 0.2243 | 0.1377 | Mens |
| womens only / older / newbie | 0.0678 | 0.1584 | Womens |
| womens only / older / old customer | 0.0883 | 0.0314 | Mens |
| womens only / recent / newbie | 0.0873 | 0.2090 | Womens |
| womens only / recent / old customer | −0.0184 | −0.1650 | None |

- Targeting policy: **$10,147**. Everyone Mens: **$6,974**. Everyone Womens: **−$99**.
- Policy minus everyone Mens: **$3,173**.
- Customers not emailed: **15,677 (24.5%)**.

Data table (policy minus everyone Mens, $ total):

| Margin \ Cost | $0.05 | $0.10 | $0.50 |
|---|---|---|---|
| 20% | 1,890 | 2,644 | 23,089 |
| 30% | 2,642 | 3,173 | 19,035 |
| 50% | 4,164 | 4,531 | 14,210 |

## Why Excel shows a bigger gain than the notebook

Excel says the policy beats "everyone Mens" by $3,173 per 64,000 customers, about $0.05 each. The notebook's held-out estimate is only $0.0035 per customer (about $222), with a CI that includes zero.

The difference is the **winner's curse**. The Excel numbers are the same training estimates that were used to *choose* the actions. In any cell where noise happened to make an action look good, we picked that action, so the in-sample profit is biased upwards. The test half never saw the choice being made, so its estimate is the honest one. This is exactly why H4 was evaluated on held-out data. Use Excel to see how the decision works and how it responds to margin and cost. Quote the notebook's numbers for the realised gain.
