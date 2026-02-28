import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide", page_title="AMA Industry Simulation")

# ===============================
# INITIALIZATION
# ===============================

if "round" not in st.session_state:
    st.session_state.round = 1
    st.session_state.cash = 100_000_000
    st.session_state.fame = 0.0
    st.session_state.trust = 0.2
    st.session_state.brand = 0.1
    st.session_state.history = []

# ===============================
# HEADER
# ===============================

st.title("🎬 AMA Creative Economy Simulation")
st.subheader(f"Round {st.session_state.round}")

col1, col2, col3 = st.columns(3)
col1.metric("Cash", f"{int(st.session_state.cash):,} VND")
col2.metric("Fame", round(st.session_state.fame,2))
col3.metric("Algorithm Trust", round(st.session_state.trust,2))

st.divider()

# ===============================
# DECISION PHASE
# ===============================

st.header("📊 Decision Phase")

colA, colB, colC = st.columns(3)

with colA:
    st.subheader("Creative")
    production = st.selectbox("Production Level",
                               ["Low (10M)", "Medium (25M)", "High (40M)"])
    mentor = st.checkbox("Hire Mentor (15M)")
    direction = st.selectbox("Artistic Direction",
                             ["Indie", "Structured", "Commercial"])

with colB:
    st.subheader("Marketing")
    ads = st.selectbox("Ads Budget",
                       ["Low (5M)", "Medium (15M)", "High (30M)"])
    influencer = st.checkbox("Influencer Campaign (20M)")

with colC:
    st.subheader("Financial")
    reserve = st.slider("Reserve Cash (%)", 0, 50, 10)

# ===============================
# LOCK DECISION
# ===============================

if st.button("🔒 Lock Decision & Run Market"):

    # -----------------------
    # CAPITAL COST
    # -----------------------

    cost_map = {
        "Low (10M)": 10_000_000,
        "Medium (25M)": 25_000_000,
        "High (40M)": 40_000_000
    }

    ad_map = {
        "Low (5M)": 5_000_000,
        "Medium (15M)": 15_000_000,
        "High (30M)": 30_000_000
    }

    total_cost = cost_map[production] + ad_map[ads]

    if mentor:
        total_cost += 15_000_000
    if influencer:
        total_cost += 20_000_000

    if total_cost > st.session_state.cash:
        st.error("Not enough capital.")
    else:

        st.session_state.cash -= total_cost

        # -----------------------
        # CREATIVE IMPACT
        # -----------------------

        quality = 0.5
        originality = 0.5

        if production == "High (40M)":
            quality += 0.2
        elif production == "Medium (25M)":
            quality += 0.1

        if direction == "Indie":
            originality += 0.2
        elif direction == "Commercial":
            originality -= 0.1
            quality += 0.1

        if mentor:
            quality += 0.1
            originality -= 0.05

        # -----------------------
        # MARKET ENGINE
        # -----------------------

        attention_pool = 100_000

        ctr = 0.03 + 0.04 * originality + 0.02 * st.session_state.fame
        watch = 0.4 + 0.4 * quality

        impressions = attention_pool * st.session_state.trust
        impressions += ad_map[ads] / 1000

        views = impressions * ctr

        performance = ctr * watch

        # Algorithm update
        st.session_state.trust += 0.1 * (performance - 0.05)
        st.session_state.trust = max(0.05, min(1.0, st.session_state.trust))

        # Fame growth
        if performance > 0.06:
            st.session_state.fame += 0.02

        revenue = views * 500
        st.session_state.cash += revenue

        # Brand update
        st.session_state.brand += 0.02 * quality

        # Save history
        st.session_state.history.append({
            "views": views,
            "revenue": revenue,
            "trust": st.session_state.trust,
            "fame": st.session_state.fame
        })

        st.success("Round Complete!")

        st.session_state.round += 1

# ===============================
# PERFORMANCE DASHBOARD
# ===============================

if len(st.session_state.history) > 0:

    st.header("📈 Performance Dashboard")

    views_history = [h["views"] for h in st.session_state.history]
    revenue_history = [h["revenue"] for h in st.session_state.history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=views_history, mode='lines+markers', name='Views'))
    fig.add_trace(go.Scatter(y=revenue_history, mode='lines+markers', name='Revenue'))
    fig.update_layout(title="Performance Over Rounds")
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# RESET
# ===============================

if st.button("Reset Simulation"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
