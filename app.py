import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide", page_title="AMA Decision Lab")

# ==========================
# INITIAL STATE
# ==========================

if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.cash = 100_000_000
    
    st.session_state.competence = {
        "Narrative": 0.5,
        "Visual": 0.5,
        "Emotion": 0.5,
        "Technical": 0.5,
        "Strategy": 0.5,
        "Originality": 0.5
    }

# ==========================
# FORMAT
# ==========================

def vnd(x):
    return f"{int(x):,} VND"

st.title("🎬 AMA Creative Decision Lab")

st.subheader("💰 Capital Status")
st.metric("Remaining Budget", vnd(st.session_state.cash))

st.divider()

# ==========================
# ACTION PANELS
# ==========================

st.subheader("🛠 Strategic Actions")

col1, col2, col3 = st.columns(3)

# PRODUCTION
with col1:
    st.markdown("### 🎥 Production Upgrade")
    prod = st.slider("Investment", 0, 40_000_000, 0, 5_000_000)
    if st.button("Apply Production"):
        if prod <= st.session_state.cash:
            st.session_state.cash -= prod
            factor = np.sqrt(prod / 10_000_000)
            st.session_state.competence["Technical"] += 0.08 * factor
            st.session_state.competence["Visual"] += 0.06 * factor

# MENTOR
with col2:
    st.markdown("### 🧠 Hire Mentor (15M)")
    if st.button("Hire Mentor"):
        if 15_000_000 <= st.session_state.cash:
            st.session_state.cash -= 15_000_000
            st.session_state.competence["Narrative"] += 0.1
            st.session_state.competence["Strategy"] += 0.08
            st.session_state.competence["Originality"] -= 0.05

# MARKETING
with col3:
    st.markdown("### 📢 Marketing Push")
    mkt = st.slider("Ad Budget", 0, 40_000_000, 0, 5_000_000)
    if st.button("Run Ads"):
        if mkt <= st.session_state.cash:
            st.session_state.cash -= mkt
            st.session_state.competence["Strategy"] += 0.05 * np.log1p(mkt/10_000_000)

st.divider()

# ==========================
# VISUALIZATION
# ==========================

st.subheader("📊 Competence Projection")

categories = list(st.session_state.competence.keys())
values = list(st.session_state.competence.values())

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Current Competence'
))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0,1])),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================
# JUDGE INPUT
# ==========================

st.subheader("🏁 Final Evaluation (Judge Input)")

judge_scores = {}

for key in categories:
    judge_scores[key] = st.slider(f"{key} Score", 0.0, 1.0, 0.5)

if st.button("Compute Outcome"):

    avg_score = np.mean(list(judge_scores.values()))
    capital_efficiency = avg_score / (100_000_000 - st.session_state.cash + 1)

    st.metric("Final Creative Score", round(avg_score,2))
    st.metric("Capital Efficiency", round(capital_efficiency,6))

    growth = avg_score - np.mean(values)
    st.metric("Competence Growth vs Projection", round(growth,2))

st.divider()

if st.button("Reset"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
