import streamlit as st
import numpy as np
import math
import random
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="AMA Creative Economy Lab")

# =========================
# FORMAT
# =========================

def format_vnd(x):
    return f"{int(x):,} VND"

# =========================
# INIT STATE
# =========================

if "initialized" not in st.session_state:

    st.session_state.initialized = True
    st.session_state.day = 0

    # Capital
    st.session_state.cash = 100_000_000
    st.session_state.initial_budget = 100_000_000

    # Competence
    st.session_state.narrative = 0.5
    st.session_state.visual = 0.5
    st.session_state.emotion = 0.5
    st.session_state.technical = 0.5
    st.session_state.strategy = 0.5

    # Market state
    st.session_state.fame = 0.0
    st.session_state.trust = 0.2
    st.session_state.sentiment = 0.5
    st.session_state.subs = 0
    st.session_state.total_views = 0
    st.session_state.total_revenue = 0

    st.session_state.history_views = []
    st.session_state.history_competence = []

# =========================
# HEADER
# =========================

st.title("🎬 AMA Creative Economy Simulation")

st.subheader("💰 Capital")

col1, col2 = st.columns(2)

col1.metric("Remaining Cash", format_vnd(st.session_state.cash))
col2.metric("Total Revenue", format_vnd(st.session_state.total_revenue))

st.divider()

# =========================
# CAPITAL ALLOCATION
# =========================

st.subheader("📊 Investment Decisions")

production = st.slider("Production Investment", 0, 50_000_000, 10_000_000, 5_000_000)
marketing = st.slider("Marketing Investment", 0, 50_000_000, 5_000_000, 5_000_000)
mentor = st.checkbox("Hire Mentor (15,000,000 VND)")

total_spent = production + marketing + (15_000_000 if mentor else 0)

if total_spent > st.session_state.cash:
    st.error("Not enough cash.")
else:
    if st.button("Invest & Launch"):

        st.session_state.cash -= total_spent

        # Competence Growth
        prod_factor = math.sqrt(production / 10_000_000) if production > 0 else 0

        st.session_state.technical += 0.05 * prod_factor
        st.session_state.visual += 0.04 * prod_factor
        st.session_state.narrative += 0.03 * prod_factor

        if mentor:
            st.session_state.narrative += 0.07
            st.session_state.strategy += 0.05
            st.session_state.emotion += 0.03
            st.session_state.visual -= 0.02  # originality pressure

        # Marketing diminishing return
        marketing_boost = math.log1p(marketing / 10_000_000)

        # --------------------------
        # MARKET SIMULATION
        # --------------------------

        base_impressions = 2000 + 8000 * st.session_state.trust
        impressions = base_impressions + 3000 * marketing_boost

        ctr = 0.03 + 0.04 * st.session_state.visual + 0.02 * st.session_state.fame
        watch = 0.3 + 0.5 * st.session_state.narrative

        views = impressions * ctr

        performance_ratio = (ctr * watch) / (0.03 * 0.5)

        st.session_state.trust += 0.05 * (performance_ratio - 1)
        st.session_state.trust = max(0.05, min(1, st.session_state.trust))

        if performance_ratio > 1.1:
            st.session_state.fame += 0.01

        revenue = views * 500
        st.session_state.cash += revenue
        st.session_state.total_revenue += revenue
        st.session_state.total_views += views

        new_subs = views * 0.01 * st.session_state.sentiment
        st.session_state.subs += new_subs

        # Competence history
        avg_comp = (
            st.session_state.narrative +
            st.session_state.visual +
            st.session_state.emotion +
            st.session_state.technical +
            st.session_state.strategy
        ) / 5

        st.session_state.history_views.append(views)
        st.session_state.history_competence.append(avg_comp)

        st.session_state.day += 1

# =========================
# METRICS
# =========================

st.subheader("📈 Current Performance")

col3, col4, col5 = st.columns(3)

col3.metric("Total Views", f"{int(st.session_state.total_views):,}")
col4.metric("Subscribers", f"{int(st.session_state.subs):,}")
col5.metric("Algorithm Trust", round(st.session_state.trust,2))

st.divider()

# =========================
# COMPETENCE PANEL
# =========================

st.subheader("🎓 Competence Growth")

competence_dict = {
    "Narrative": st.session_state.narrative,
    "Visual": st.session_state.visual,
    "Emotion": st.session_state.emotion,
    "Technical": st.session_state.technical,
    "Strategy": st.session_state.strategy
}

fig1, ax1 = plt.subplots()
ax1.bar(competence_dict.keys(), competence_dict.values())
ax1.set_ylim(0,1)
ax1.set_title("Competence Profile")
st.pyplot(fig1)

# =========================
# HISTORY
# =========================

if len(st.session_state.history_views) > 0:

    st.subheader("📊 Evolution")

    fig2, ax2 = plt.subplots(1,2, figsize=(12,4))

    ax2[0].plot(st.session_state.history_views)
    ax2[0].set_title("Views Over Time")

    ax2[1].plot(st.session_state.history_competence)
    ax2[1].set_title("Competence Growth")

    st.pyplot(fig2)

st.divider()

if st.button("Reset Simulation"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
