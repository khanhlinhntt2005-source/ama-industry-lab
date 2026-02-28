import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random
import pandas as pd

st.set_page_config(layout="wide", page_title="AMA Industry Simulation v2", initial_sidebar_state="expanded")

# ============================================
# GENRE DATABASE WITH DEMOGRAPHICS
# ============================================

GENRES = {
    "Indie Chill": {
        "description": "Aesthetic, lyric-driven, authenticity-sensitive audience.",
        "segments": {
            "Urban Gen Z": {"size": 50000, "ctr": 0.06, "retention": 0.65, "auth_sensitivity": 0.9},
            "Millennials": {"size": 40000, "ctr": 0.04, "retention": 0.6, "auth_sensitivity": 0.7},
            "Art Niche": {"size": 20000, "ctr": 0.05, "retention": 0.75, "auth_sensitivity": 0.95}
        }
    },
    "Rap Underground": {
        "description": "Identity-driven, authenticity-critical audience.",
        "segments": {
            "Street Core": {"size": 45000, "ctr": 0.07, "retention": 0.7, "auth_sensitivity": 0.95},
            "Youth Culture": {"size": 60000, "ctr": 0.05, "retention": 0.6, "auth_sensitivity": 0.8},
            "Casual Listeners": {"size": 30000, "ctr": 0.03, "retention": 0.5, "auth_sensitivity": 0.6}
        }
    }
}

FAME_LEVELS = {"Unknown": 0.1, "Local Buzz": 0.3, "Regional": 0.6}
TARGET_GOAL = 120_000_000

# ============================================
# INIT
# ============================================

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.round = 1
    st.session_state.cash = 100_000_000
    
    st.session_state.genre = random.choice(list(GENRES.keys()))
    st.session_state.fame_label = random.choice(list(FAME_LEVELS.keys()))
    st.session_state.fame = FAME_LEVELS[st.session_state.fame_label]
    
    st.session_state.trust = 0.3
    st.session_state.history = []
    st.session_state.feedback = []

# ============================================
# INTRO SCREEN
# ============================================

st.title("🎬 AMA Creative Industry Simulation")

st.subheader("🎲 Your Assigned Simulation Profile")

st.write(f"**Genre:** {st.session_state.genre}")
st.write(f"**Starting Fame:** {st.session_state.fame_label}")
st.write(f"**Audience Insight:** {GENRES[st.session_state.genre]['description']}")
st.write("🎯 Goal: Grow your capital from 100,000,000 VND to 120,000,000 VND.")

st.divider()

colA, colB = st.columns(2)
colA.metric("Cash", f"{int(st.session_state.cash):,} VND")
colB.metric("Algorithm Trust", round(st.session_state.trust,2))

st.divider()

# ============================================
# CONSULTING OPTION
# ============================================

if st.button("📊 Consult Market Expert (3M VND)"):
    if st.session_state.cash >= 3_000_000:
        st.session_state.cash -= 3_000_000
        st.success("Detailed Audience Insights Unlocked")

        for seg, data in GENRES[st.session_state.genre]["segments"].items():
            st.write(f"{seg}: Size {data['size']}, CTR {data['ctr']}, Retention {data['retention']}")
    else:
        st.error("Not enough cash")

st.divider()

# ============================================
# DECISION PHASE
# ============================================

st.header(f"📊 Round {st.session_state.round} – Decision")

production = st.slider("Production Investment", 0, 40_000_000, 10_000_000, 5_000_000)
auth_focus = st.slider("Authenticity Focus", 0.0, 1.0, 0.5)
ads = st.slider("Ads Investment", 0, 30_000_000, 5_000_000, 5_000_000)

total_cost = production + ads

st.metric("Total Investment This Round", f"{int(total_cost):,} VND")

# ============================================
# RUN ROUND
# ============================================

if st.button("🔒 Lock & Simulate Market"):

    if total_cost > st.session_state.cash:
        st.error("Not enough capital")
    else:
        st.session_state.cash -= total_cost
        
        total_views = 0
        total_revenue = 0
        
        feedback_report = []

        for seg, data in GENRES[st.session_state.genre]["segments"].items():
            
            impressions = data["size"] * st.session_state.trust
            ctr = data["ctr"] + (auth_focus * data["auth_sensitivity"] * 0.02)
            retention = data["retention"] + (production / 40_000_000) * 0.1
            
            views = impressions * ctr
            revenue = views * 500
            
            total_views += views
            total_revenue += revenue
            
            feedback_report.append({
                "Segment": seg,
                "Views": int(views),
                "Retention": round(retention,2)
            })

        st.session_state.cash += total_revenue
        st.session_state.trust += 0.02
        st.session_state.round += 1

        st.session_state.history.append({
            "views": total_views,
            "revenue": total_revenue,
            "cash": st.session_state.cash
        })

        st.session_state.feedback = feedback_report

        st.success("Round Completed!")

# ============================================
# PERFORMANCE DASHBOARD
# ============================================

if len(st.session_state.history) > 0:

    df = pd.DataFrame(st.session_state.history)
    st.subheader("📈 Financial & Growth Overview")

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df["views"], mode="lines+markers", name="Views"))
    fig.add_trace(go.Scatter(y=df["revenue"], mode="lines+markers", name="Revenue"))
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Segment Feedback")

    for f in st.session_state.feedback:
        st.write(f)

    if st.session_state.cash >= TARGET_GOAL:
        st.success("🎉 Target Achieved! Simulation Completed.")

# ============================================
# RESET
# ============================================

if st.button("Reset Simulation"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
