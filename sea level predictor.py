import pandas as pd 
import matplotlib.pyplot as plt 
from scipy.stats import linregress 
df=pd.read_csv('sea_level_data_csv')
plt.figure(figsize=(10,6))
plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], color='blue', alpha=0.6, label='Data')
slope1, intercept1, r_value, p_value, std_err = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
years_extended = pd.Series(range(1880, 2051))
best_fit_line1 = intercept1 + slope1 * years_extended
plt.plot(years_extended, best_fit_line1, color='red', label='Best Fit: All Data')
df_recent = df[df['Year'] >= 2000]
slope2, intercept2, r_value, p_value, std_err = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
years_recent = pd.Series(range(2000, 2051))
best_fit_line2 = intercept2 + slope2 * years_recent
plt.plot(years_recent, best_fit_line2, color='green', label='Best Fit: 2000–Present')
plt.xlabel("Year")
plt.ylabel("Sea Level (inches)")
plt.title("Rise in Sea Level")
plt.legend()
plt.grid(True)
plt.savefig("sea_level_plot.png")
return plt.gca()