# did_analysis. py - DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex
# Computes the difference-in-differences estimate for the eBay paid search experiment.
# Method: Compare pre-post log revenue changes between treatment and control DMAs.
# Reference: Blake et al. (2014), Taddy Ch. 5

import pandas as pd
import numpy as np
# Load pivot tables saved by preprocess.py
treated_pivot = pd.read_csv('temp/treated_pivot.csv', index_col='dma')
untreated_pivot = pd.read_csv('temp/untreated_pivot.csv', index_col='dma')
# Compute the average log difference for treated units
avg_log_diff_treated = treated_pivot['log_revenue_diff'].mean()

# Compute the variance of the log differences for treated units and divide by the number of treated units
var_log_diff_treated = treated_pivot['log_revenue_diff'].var() / len(treated_pivot)
# Compute the average log difference for untreated units
avg_log_diff_untreated = untreated_pivot['log_revenue_diff'].mean()

# Compute the variance of the log differences for untreated units and divide by the number of untreated units
var_log_diff_untreated = untreated_pivot['log_revenue_diff'].var() / len(untreated_pivot)
# Compute the difference between the average log differences (gamma_hat)
gamma_hat = avg_log_diff_treated - avg_log_diff_untreated

# Compute the sum of the variances
sum_variances = var_log_diff_treated + var_log_diff_untreated

# Compute the standard error
standard_error = np.sqrt(sum_variances)

# Compute the 95% confidence interval for the treatment effect
ci_lower = gamma_hat - 1.96 * standard_error
ci_upper = gamma_hat + 1.96 * standard_error

# Exponentiate the midpoint and the extremes of the interval
gamma_hat_exp = np.exp(gamma_hat)
ci_lower_exp = np.exp(ci_lower)
ci_upper_exp = np.exp(ci_upper)


values = {
    "gamma": gamma_hat,
    "se": standard_error,
    "ci_low": ci_lower,
    "ci_high": ci_upper
}

latex_content = rf"""
\begin{{table}}[h]
\centering
\caption{{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}}
\begin{{tabular}}{{lc}}
\hline
& Log Scale \\
\hline
Point Estimate ($\hat{{\gamma}}$)      & {values["gamma"]:.4f} \\
Standard Error                        & {values["se"]:.4f} \\
95\% CI                               & $[{values["ci_low"]:.4f}, \; {values["ci_high"]:.4f}]$ \\
\hline
\end{{tabular}}
\label{{tab:did}}
\end{{table}}
""".strip()

with open('output/tables/did_table.tex', 'w', encoding='utf-8') as f:
    f.write(latex_content)
