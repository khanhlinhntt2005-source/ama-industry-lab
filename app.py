import streamlit as st
import numpy as np
import math
import random
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🎬 AMA YouTube Interactive Simulation")

# =========================
# FORMAT FUNCTION
# =========================

def format_vnd(x):
    return f"{int(x):,} VND"

# =========================
# INITIALIZE STATE
# =========================

if "day" not in st.session_state:
    st.session_state.day = 0
    st.session_state.views = 10000
    st.session_state.subs = 0
    st.session_state.revenue = 0
    st.session_state.sentiment = 0.5

# =========================
# INITIAL INPUT (ONLY DAY 0)
# =========================

if st.session_state.day == 0:
    st.header("🎨 Initial Creative Setup")

    st.session_state.story = st.slider("Story",1,10,7)
    st.session_state.narrative = st.slider("Narrative",1,10,8)
    st.session_state.visual = st.slider("Visual",1,10,8)
    st.session_state.emotion = st.slider("Emotion",1,10,8)
    st.session_state.originality = st.slider("Originality",1,10,7)

    st.session_state.production = st.slider("Production Budget",5_000_000,80_000_000,30_000_000,5_000_000)
    st.session_state.marketing = st.slider("Marketing Budget",0,80_000_000,20_000_000,5_000_000)
    st.session_state.equity = st.slider("Investor Equity %",0.0,0.5,0.0,0.05)

    if st.button("🚀 Launch Video"):
        st.session_state.day = 1

# =========================
# DAILY SIMULATION
# =========================

if st.session_state.day > 0:

    st.header(f"📅 Day {st.session_state.day}")

    st.subheader("🛠 Daily Intervention")

    boost_ads = st.checkbox("Run Extra Ads Today (+Growth, -Sentiment)")
    drop_content = st.checkbox("Drop Behind-the-Scenes (+Engagement)")
    influencer = st.checkbox("Pay Influencer Boost")

    # Core quality
    quality = (
        0.25*st.session_state.narrative +
        0.2*st.session_state.emotion +
        0.2*st.session_state.visual +
        0.2*st.session_state.originality +
        0.15*st.session_state.story
    ) / 10

    retention = (st.session_state.narrative + st.session_state.emotion)/20

    # Organic growth
    growth = st.session_state.views * (0.05 * retention)

    # Algorithm boost
    algo = st.session_state.views * (0.03 * quality)

    # Decay
    decay = st.session_state.views * 0.08

    # Interventions
    if boost_ads:
        growth *= 1.5
        st.session_state.sentiment -= 0.05

    if drop_content:
        retention *= 1.2
        st.session_state.sentiment += 0.03

    if influencer:
        growth *= 1.3

    # Sentiment bounds
    st.session_state.sentiment = max(0, min(1, st.session_state.sentiment))

    noise = np.random.normal(0, st.session_state.views * 0.02)

    new_views = max(
        1000,
        st.session_state.views + growth + algo - decay + noise
    )

    new_subs = new_views * 0.01 * retention

    daily_revenue = new_views * 500

    # Update state
    st.session_state.views = new_views
    st.session_state.subs += new_subs
    st.session_state.revenue += daily_revenue

    # Display metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("Views Today", f"{int(new_views):,}")
    col2.metric("Total Subscribers", f"{int(st.session_state.subs):,}")
    col3.metric("Total Revenue", format_vnd(st.session_state.revenue))

    st.progress(st.session_state.sentiment)

    if st.button("➡ Next Day"):
        st.session_state.day += 1

    if st.button("🔄 Reset Simulation"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
