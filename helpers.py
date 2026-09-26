import numpy as np
import pandas as pd
import statsmodels.api as sm


def load_data():
    df = pd.read_csv("data/hillstrom.csv")
    df["zip_urban"] = (df["zip_code"] == "Urban").astype(int)
    df["zip_suburban"] = (df["zip_code"] == "Surburban").astype(int)
    df["channel_web"] = (df["channel"] == "Web").astype(int)
    df["channel_multi"] = (df["channel"] == "Multichannel").astype(int)
    df["mens_email"] = (df["segment"] == "Mens E-Mail").astype(int)
    df["womens_email"] = (df["segment"] == "Womens E-Mail").astype(int)
    df["any_email"] = (df["segment"] != "No E-Mail").astype(int)
    df["recent"] = (df["recency"] <= 6).astype(int)
    df["past_category"] = "both"
    df.loc[(df["mens"] == 1) & (df["womens"] == 0), "past_category"] = "mens only"
    df.loc[(df["mens"] == 0) & (df["womens"] == 1), "past_category"] = "womens only"
    return df


def diff_in_means(y_treat, y_control):
    diff = y_treat.mean() - y_control.mean()
    se = np.sqrt(y_treat.var(ddof=1) / len(y_treat) + y_control.var(ddof=1) / len(y_control))
    return diff, se


def lin_regression(data, outcome, treat_col, covariates):
    X = data[covariates] - data[covariates].mean()
    for col in covariates:
        X[col + "_x_treat"] = X[col] * data[treat_col]
    X[treat_col] = data[treat_col]
    X = sm.add_constant(X)
    model = sm.OLS(data[outcome], X).fit(cov_type="HC2")
    return model.params[treat_col], model.bse[treat_col]


def permutation_test(y_treat, y_control, n_perm):
    observed = y_treat.mean() - y_control.mean()
    pooled = np.concatenate([y_treat, y_control])
    n_treat = len(y_treat)
    count = 0
    for i in range(n_perm):
        shuffled = np.random.permutation(pooled)
        perm_diff = shuffled[:n_treat].mean() - shuffled[n_treat:].mean()
        if abs(perm_diff) >= abs(observed):
            count = count + 1
    return (count + 1) / (n_perm + 1)


def bootstrap_ci(y_treat, y_control, n_boot):
    diffs = []
    for i in range(n_boot):
        t = np.random.choice(y_treat, size=len(y_treat), replace=True)
        c = np.random.choice(y_control, size=len(y_control), replace=True)
        diffs.append(t.mean() - c.mean())
    return np.percentile(diffs, 2.5), np.percentile(diffs, 97.5)


def holm(pvalues):
    order = np.argsort(pvalues)
    m = len(pvalues)
    adjusted = np.zeros(m)
    running_max = 0
    for rank in range(m):
        i = order[rank]
        value = min(1, (m - rank) * pvalues[i])
        running_max = max(running_max, value)
        adjusted[i] = running_max
    return adjusted
