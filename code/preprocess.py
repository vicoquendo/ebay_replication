import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('input/PaidSearch.csv')
df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y')
df['log_revenue'] = np.log(df['revenue'])

# Basic summary statistics to print
n_treated_dmas = df[df['search_stays_on'] == 0]['dma'].nunique()
n_untreated_dmas = df[df['search_stays_on'] == 1]['dma'].nunique()
min_date = df['date'].min().strftime('%Y-%m-%d')
max_date = df['date'].max().strftime('%Y-%m-%d')

print(f"Treated DMAs: {n_treated_dmas}")
print(f"Untreated DMAs: {n_untreated_dmas}")
print(f"Date range: {min_date} to {max_date}")

# Separate treated and untreated units
treated = df[df['search_stays_on'] == 0]
untreated = df[df['search_stays_on'] == 1]

# Create pivot tables for treated
treated_pivot = treated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)
treated_pivot.columns = ['log_revenue_pre', 'log_revenue_post']
treated_pivot['log_revenue_diff'] = treated_pivot['log_revenue_post'] - treated_pivot['log_revenue_pre']
treated_pivot.to_csv('temp/treated_pivot.csv')

# Create pivot tables for untreated
untreated_pivot = untreated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)
untreated_pivot.columns = ['log_revenue_pre', 'log_revenue_post']
untreated_pivot['log_revenue_diff'] = untreated_pivot['log_revenue_post'] - untreated_pivot['log_revenue_pre']
untreated_pivot.to_csv('temp/untreated_pivot.csv')

# Optional: print simple DID estimate (as in previous version)
#print("\nAverage log revenue difference (pre to post):")
#print(f"  Treated group:   {treated_pivot['log_revenue_diff'].mean():.6f}")
#print(f"  Untreated group: {untreated_pivot['log_revenue_diff'].mean():.6f}")
#print(f"  Simple DID estimate: {treated_pivot['log_revenue_diff'].mean() - untreated_pivot['log_revenue_diff'].mean():.6f}")

# Generate Figure 5.2: Average revenue over time for both groups
avg_rev = df.groupby(['date', 'search_stays_on'])['revenue'].mean().reset_index()
control_rev = avg_rev[avg_rev['search_stays_on'] == 1]
treated_rev = avg_rev[avg_rev['search_stays_on'] == 0]

plt.figure(figsize=(10, 6))
plt.plot(control_rev['date'], control_rev['revenue'], label='Control (Search Stays On)')
plt.plot(treated_rev['date'], treated_rev['revenue'], label='Treated (Search Turned Off)')
plt.axvline(pd.to_datetime('2012-05-22'), color='red', linestyle='--', label='Treatment Start')
plt.xlabel('Date')
plt.ylabel('Average Revenue')
plt.title('Average Revenue Over Time by Group')
plt.legend()
plt.savefig('output/figures/figure_5_2.png')
plt.close()

# Generate Figure 5.3: Log-scale difference over time
avg_log_rev = df.groupby(['date', 'search_stays_on'])['log_revenue'].mean().reset_index()
control_log = avg_log_rev[avg_log_rev['search_stays_on'] == 1].set_index('date')['log_revenue']
treated_log = avg_log_rev[avg_log_rev['search_stays_on'] == 0].set_index('date')['log_revenue']
log_diff = control_log - treated_log

plt.figure(figsize=(10, 6))
plt.plot(log_diff.index, log_diff, label='Control − Treated')
plt.axvline(pd.to_datetime('2012-05-22'), color='red', linestyle='--', label='Treatment Start')
plt.xlabel('Date')
plt.ylabel('Log Revenue Difference (Control - Treated)')
plt.title('Log-Scale Revenue Difference Over Time')
plt.legend()
plt.savefig('output/figures/figure_5_3.png')
plt.close()
