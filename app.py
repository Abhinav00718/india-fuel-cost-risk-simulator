
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="India Fuel Cost Risk Simulator",
    page_icon="⛽",
    layout="wide"
)

st.title("India Fuel Cost Risk Simulator")
st.caption(
    "Explore how crude-oil price shocks and INR/USD movements "
    "change the estimated rupee cost of crude."
)

st.sidebar.header("Market assumptions")

oil_price = st.sidebar.number_input(
    "WTI crude price (USD/barrel)",
    min_value=1.0, value=98.35, step=1.0
)

exchange_rate = st.sidebar.number_input(
    "INR per USD",
    min_value=1.0, value=96.52, step=0.5
)

oil_shock = st.sidebar.slider(
    "Oil-price shock (%)", -50, 100, 10
)

rupee_shock = st.sidebar.slider(
    "Rupee depreciation (%)", -30, 50, 5
)

baseline_cost = oil_price * exchange_rate

new_oil = oil_price * (1 + oil_shock / 100)
new_fx = exchange_rate * (1 + rupee_shock / 100)
new_cost = new_oil * new_fx

cost_change = (new_cost / baseline_cost - 1) * 100

st.subheader("Estimated crude cost")

c1, c2, c3 = st.columns(3)

c1.metric("Baseline cost", f"₹{baseline_cost:,.2f}/barrel")
c2.metric("Stressed cost", f"₹{new_cost:,.2f}/barrel",
          delta=f"{cost_change:+.2f}%")
c3.metric("Absolute change", f"₹{new_cost - baseline_cost:,.2f}/barrel")

st.info(
    "This is a benchmark-based estimate using WTI and INR/USD. "
    "It is not India's actual landed crude cost or retail fuel price."
)

st.divider()
st.subheader("Scenario comparison")

scenarios = [
    ("Baseline", 0, 0),
    ("Oil rises 10%", 10, 0),
    ("Rupee depreciates 5%", 0, 5),
    ("Combined moderate shock", 10, 5),
    ("Severe shock", 25, 10),
    ("User-selected scenario", oil_shock, rupee_shock),
]

rows = []
for name, oil_s, fx_s in scenarios:
    cost = oil_price * (1 + oil_s / 100) * exchange_rate * (1 + fx_s / 100)
    rows.append({
        "Scenario": name,
        "Oil shock (%)": oil_s,
        "Rupee shock (%)": fx_s,
        "Estimated cost (₹/barrel)": round(cost, 2),
        "Cost change (%)": round((cost / baseline_cost - 1) * 100, 2)
    })

scenario_df = pd.DataFrame(rows)
st.dataframe(scenario_df, use_container_width=True, hide_index=True)

st.download_button(
    "Download scenario results (CSV)",
    data=scenario_df.to_csv(index=False).encode("utf-8"),
    file_name="fuel_cost_scenarios.csv",
    mime="text/csv"
)

st.divider()
st.subheader("Sensitivity analysis")

oil_shocks = np.arange(-30, 51, 10)
rupee_shocks = np.arange(-10, 26, 5)

heatmap_rows = []
for os in oil_shocks:
    for rs in rupee_shocks:
        cost = oil_price * (1 + os / 100) * exchange_rate * (1 + rs / 100)
        heatmap_rows.append({
            "Oil shock (%)": os,
            "Rupee shock (%)": rs,
            "Cost change (%)": (cost / baseline_cost - 1) * 100
        })

heatmap_df = pd.DataFrame(heatmap_rows)

fig = px.density_heatmap(
    heatmap_df,
    x="Rupee shock (%)",
    y="Oil shock (%)",
    z="Cost change (%)",
    histfunc="avg",
    text_auto=".1f",
    color_continuous_scale="RdYlGn_r",
    title="Change in Estimated Rupee Crude Cost (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Scenario outputs are deterministic calculations, not forecasts. "
    "WTI is a US benchmark and may differ from India's imported crude basket."
)
