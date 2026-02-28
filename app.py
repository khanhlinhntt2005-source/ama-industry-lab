import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

st.set_page_config(layout="wide")
st.title("🎬 AMA Industry Lab Simulation")

BENCHMARK = {
    "story": 7,
    "narrative": 8,
    "visual": 8,
    "editing": 7,
    "emotion": 8,
    "originality": 7,
    "technical": 8
}

WEIGHTS = {
    "story": 0.15,
    "narrative": 0.20,
    "visual": 0.15,
    "editing": 0.10,
    "emotion": 0.15,
    "originality": 0.15,
    "technical": 0.10
}

BASE_VIEWS = 60000
REVENUE_PER_VIEW = 500

st.header("🎨 Artistic Profile")

cols = st.columns(4)
inputs = {}

for i, key in enumerate(BENCHMARK):
    inputs[key] = cols[i % 4].slider(
        key.capitalize(), 1, 10, 7
    )

st.header("Investment Strategy")

production_cost = st.slider(
    "Production Budget", 5_000_000, 80_000_000, 30_000_000, 5_000_000
)

marketing_cost = st.slider(
    "Marketing Budget", 0, 80_000_000, 20_000_000, 5_000_000
)

commercial_push = st.slider(
    "Commercial Push Level", 1, 10, 6
)

investor_equity = st.slider(
    "Investor Equity %", 0.0, 0.5, 0.0, 0.05
)

def artistic_score(student):
    score = 0
    for k in student:
        diff = student[k] - BENCHMARK[k]
        adjusted = 10 - (diff**2)/4
        score += adjusted * WEIGHTS[k]
    return score

def simulate(student):
    art_score = artistic_score(student)

    alignment = abs(student["narrative"] - student["emotion"])
    integrity = max(0, 10 - alignment)

    trend = np.random.normal(1, 0.05)
    market_fit = (art_score / 10) * trend

    marketing_effect = math.log1p(marketing_cost / 10_000_000)
    production_effect = math.sqrt(production_cost / 10_000_000)

    backlash = 0.85 if commercial_push > student["originality"] else 1.0

    views = BASE_VIEWS
    views *= (1 + market_fit)
    views *= (1 + marketing_effect)
    views *= (1 + production_effect)
    views *= backlash
    views *= np.random.normal(1, 0.05)
    views = max(10000, views)

    retention = 0.4 + (integrity / 20)

    streaming_revenue = views * retention * REVENUE_PER_VIEW

    parent_rating = (student["emotion"] / 2) + np.random.normal(1.5, 0.2)
    ticket_revenue = parent_rating * 8_000_000

    vote_bonus = views * 0.02

    total_revenue = streaming_revenue + ticket_revenue + vote_bonus
    net_revenue = total_revenue * (1 - investor_equity)

    total_cost = production_cost + marketing_cost
    roi = net_revenue / max(1, total_cost)

    return roi, views, net_revenue

if st.button("🚀 Run 1000 Simulations"):

    runs = 1000
    rois = []
    views_list = []
    revenues = []

    for _ in range(runs):
        roi, views, revenue = simulate(inputs)
        rois.append(roi)
        views_list.append(views)
        revenues.append(revenue)

    st.subheader("📊 Industry Report")

    col1, col2, col3 = st.columns(3)

    col1.metric("Expected ROI", round(np.mean(rois), 2))
    col2.metric("Expected Views", int(np.mean(views_list)))
    col3.metric("Expected Net Revenue", int(np.mean(revenues)))

    fig, axs = plt.subplots(1, 2, figsize=(14, 5))

    sns.histplot(rois, bins=30, kde=True, ax=axs[0])
    axs[0].set_title("ROI Distribution")

    axs[1].bar(
        ["Cost", "Expected Revenue"],
        [production_cost + marketing_cost, np.mean(revenues)]
    )
    axs[1].set_title("Financial Comparison")

    st.pyplot(fig)
