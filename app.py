"""
app.py  —  Sea Level Rise Dashboard
Run with:  streamlit run dashboard/app.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import linregress

from src.sea_level_analysis import load_data, compute_regression

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sea Level Rise Dashboard",
    page_icon="🌊",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .metric-label { font-size: 13px !important; }
    h1 { font-weight: 500 !important; }
    .stMetric { background: #f5f5f4; border-radius: 10px; padding: 0.75rem 1rem; }
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data("data/epa-sea-level.csv")


df = get_data()

# ── Sidebar controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Controls")
    forecast_year = st.slider("Forecast to year", 2025, 2100, 2050, step=5)
    recent_cutoff = st.slider("Recent trend: start year", 1990, 2010, 2000, step=1)
    show_scatter = st.checkbox("Show data points", value=True)
    show_line1 = st.checkbox("Show all-data regression", value=True)
    show_line2 = st.checkbox("Show recent regression", value=True)
    st.divider()
    st.caption("Data: CSIRO adjusted sea level measurements (EPA)")

# ── Regressions ───────────────────────────────────────────────────────────────
slope1, intercept1, r2_all = compute_regression(df)
slope2, intercept2, r2_recent = compute_regression(df, start_year=recent_cutoff)

proj_all = intercept1 + slope1 * forecast_year
proj_recent = intercept2 + slope2 * forecast_year
acceleration = ((slope2 - slope1) / slope1) * 100

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🌊 Sea Level Rise Predictor")
st.markdown(
    f"Analyzing CSIRO adjusted sea level records **1880–2014** "
    f"with linear regression forecasts to **{forecast_year}**."
)

# ── Key metrics ───────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Years of data", f"{df['Year'].max() - df['Year'].min()}")
c2.metric("All-data slope", f"{slope1:.4f} in/yr")
c3.metric(f"Post-{recent_cutoff} slope", f"{slope2:.4f} in/yr",
          delta=f"{acceleration:+.1f}% vs full period")
c4.metric(f"All-data → {forecast_year}", f"{proj_all:.2f} in")
c5.metric(f"Recent → {forecast_year}", f"{proj_recent:.2f} in")

st.divider()

# ── Chart ─────────────────────────────────────────────────────────────────────
years_full = list(range(1880, forecast_year + 1))
years_recent = list(range(recent_cutoff, forecast_year + 1))

fig = go.Figure()

if show_scatter:
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["CSIRO Adjusted Sea Level"].round(3),
        mode="markers",
        name="Observed data",
        marker=dict(color="#378ADD", opacity=0.6, size=6),
    ))

if show_line1:
    fig.add_trace(go.Scatter(
        x=years_full,
        y=[round(intercept1 + slope1 * y, 3) for y in years_full],
        mode="lines",
        name=f"All-data regression (R²={r2_all:.3f})",
        line=dict(color="#E24B4A", width=2),
    ))

if show_line2:
    fig.add_trace(go.Scatter(
        x=years_recent,
        y=[round(intercept2 + slope2 * y, 3) for y in years_recent],
        mode="lines",
        name=f"Post-{recent_cutoff} regression (R²={r2_recent:.3f})",
        line=dict(color="#1D9E75", width=2, dash="dash"),
    ))

# Vertical line at end of data
fig.add_vline(
    x=2014, line_dash="dot", line_color="#aaaaaa",
    annotation_text="Data ends (2014)", annotation_position="top right",
    annotation_font_size=11,
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Sea Level (inches)",
    legend=dict(orientation="h", y=-0.15, x=0),
    margin=dict(t=20, b=60),
    plot_bgcolor="#f9f9f9",
    paper_bgcolor="white",
    height=480,
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

# ── Findings ──────────────────────────────────────────────────────────────────
with st.expander("📊 Key findings", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
**Full-period trend (1880–2014)**
- Rate: **{slope1:.4f} inches/year**
- R²: {r2_all:.3f} (strong linear fit)
- Projected level by {forecast_year}: **{proj_all:.2f} inches**
        """)
    with col_b:
        st.markdown(f"""
**Accelerating trend (post-{recent_cutoff})**
- Rate: **{slope2:.4f} inches/year**
- R²: {r2_recent:.3f}
- **{acceleration:.1f}% faster** than the historical average
- Projected level by {forecast_year}: **{proj_recent:.2f} inches**
        """)

# ── Raw data table ────────────────────────────────────────────────────────────
with st.expander("📋 Raw data"):
    st.dataframe(
        df[["Year", "CSIRO Adjusted Sea Level"]].rename(columns={
            "CSIRO Adjusted Sea Level": "Sea Level (inches)"
        }).reset_index(drop=True),
        use_container_width=True,
        height=300,
    )

st.caption("Built with Streamlit · Data source: EPA / CSIRO")
