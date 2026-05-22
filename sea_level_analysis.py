"""
sea_level_analysis.py
Core analysis module: loads data, computes regressions, saves plot.
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os


def load_data(filepath: str = "data/epa-sea-level.csv") -> pd.DataFrame:
    """Load and validate the sea level CSV dataset."""
    df = pd.read_csv(filepath)
    required_cols = {"Year", "CSIRO Adjusted Sea Level"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")
    df = df.dropna(subset=["Year", "CSIRO Adjusted Sea Level"])
    df["Year"] = df["Year"].astype(int)
    return df


def compute_regression(df: pd.DataFrame, start_year: int = None):
    """
    Compute linear regression on sea level data.
    Optionally filter to years >= start_year.
    Returns: slope, intercept, r_squared
    """
    if start_year:
        df = df[df["Year"] >= start_year]
    result = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])
    return result.slope, result.intercept, result.rvalue ** 2


def project_sea_level(slope: float, intercept: float, years) -> pd.Series:
    """Project sea level for a range of years using regression parameters."""
    return pd.Series([intercept + slope * y for y in years], index=years)


def draw_plot(filepath: str = "data/epa-sea-level.csv",
              save_path: str = "output/sea_level_plot.png"):
    """
    Full pipeline: load data, run regressions, draw and save the plot.
    Returns the matplotlib Axes object (for testing compatibility).
    """
    df = load_data(filepath)

    slope1, intercept1, r2_all = compute_regression(df)
    slope2, intercept2, r2_recent = compute_regression(df, start_year=2000)

    years_full = range(1880, 2051)
    years_recent = range(2000, 2051)

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("#f9f9f9")
    ax.set_facecolor("#f9f9f9")

    # Scatter: historical data
    ax.scatter(
        df["Year"], df["CSIRO Adjusted Sea Level"],
        color="#378ADD", alpha=0.6, s=25, label="Observed data", zorder=3
    )

    # Regression line 1: all data
    ax.plot(
        list(years_full),
        [intercept1 + slope1 * y for y in years_full],
        color="#E24B4A", linewidth=2,
        label=f"Regression (all data)  R²={r2_all:.3f}"
    )

    # Regression line 2: post-2000
    ax.plot(
        list(years_recent),
        [intercept2 + slope2 * y for y in years_recent],
        color="#1D9E75", linewidth=2, linestyle="--",
        label=f"Regression (2000–present)  R²={r2_recent:.3f}"
    )

    # Vertical marker at 2014 (end of data)
    ax.axvline(x=2014, color="#888780", linewidth=1, linestyle=":", alpha=0.7)
    ax.text(2015, ax.get_ylim()[0] + 0.1, "Data ends\n2014",
            fontsize=9, color="#888780")

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Sea Level (inches)", fontsize=12)
    ax.set_title("Rise in Sea Level (1880–2050 projection)", fontsize=14, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)

    return ax


if __name__ == "__main__":
    ax = draw_plot()
    print("Plot saved to output/sea_level_plot.png")
    plt.show()
