# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Insider Trade Suspicion Scorer", layout="centered")

st.markdown("<div style='position: absolute; top: 10px; left: 10px; font-size: 12px; color: gray;'>Created by Mishil Trivedi and Junhan Chen</div>", unsafe_allow_html=True)

st.title("📊 Insider Trade Suspicion Scorer")
st.markdown("Enter trade details below to get a suspicion score and classification.")

# User input fields
trade_size = st.number_input("💰 Trade Value (in USD)", min_value=0.0, step=1000.0)
reporting_delay = st.number_input("⏱ Days between Trade and Publication", min_value=0, step=1)
is_high_level = st.selectbox("🏢 Is High-Level Executive?", ["No", "Yes"])
used_10b5_1 = st.selectbox("📝 Was 10b5-1 Plan Used?", ["Yes", "No"])
past_trade_avg = st.number_input("📈 Avg Past Trade Value (by this Insider)", min_value=0.0, step=1000.0)

if st.button("🔍 Classify Trade"):
    # --- Normalize components ---
    size_pct = min(trade_size / 1_000_000, 1)  # Cap at $1M
    speed_score = 1 - min(reporting_delay / 10, 1)  # Anything >10 days = 0
    high_level_score = 1 if is_high_level == "Yes" else 0
    plan_flag_score = 0 if used_10b5_1 == "Yes" else 1
    past_avg_score = min(past_trade_avg / 1_000_000, 1)

    # --- Final score calculation ---
    score = round((
        0.30 * size_pct +
        0.25 * speed_score +
        0.15 * high_level_score +
        0.10 * plan_flag_score +
        0.20 * past_avg_score
    ), 2)

    # --- Classification ---
    if score < 0.4:
        level = "✅ Routine"
    elif score < 0.7:
        level = "⚠️ Moderate"
    else:
        level = "🚨 Suspicious"

    # --- Display results ---
    st.markdown(f"### 🎯 Suspicion Score: **{score}**")
    st.markdown(f"### Classification: **{level}**")
    st.progress(score)

    # --- Score breakdown ---
    st.markdown("---")
    st.markdown("#### 🔍 Explanation of Components")
    st.markdown(f"""
    - **Trade Size Percentile**: {size_pct:.2f}
    - **Reporting Speed Score**: {speed_score:.2f}
    - **Executive Level**: {high_level_score}
    - **10b5-1 Plan Used**: {0 if plan_flag_score == 0 else 1}
    - **Past Trade Behavior Score**: {past_avg_score:.2f}
    """)

    # --- Radar chart ---
    labels = ['Trade Size', 'Reporting Speed', 'Exec Level', '10b5-1 Plan', 'Past Behavior']
    values = [size_pct, speed_score, high_level_score, plan_flag_score, past_avg_score]
    values += values[:1]  # Loop back to start

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

   # Setup figure and axis
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#f9f9f9')  # Light background

   # Plot
    ax.plot(angles, values, color='#FF4B4B', linewidth=2.5, linestyle='-', marker='o', markersize=6)
    ax.fill(angles, values, color='#FF4B4B', alpha=0.3)
 
   # Style axes
    ax.set_facecolor('#ffffff')  # White background
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12, fontweight='bold')
    ax.set_yticklabels([])
    ax.grid(color='gray', linestyle='dashed', alpha=0.4)
    ax.spines['polar'].set_visible(False)

   # Title
    ax.set_title("Component Breakdown Radar", y=1.1, fontsize=16, fontweight='bold', color='#333333')

    st.pyplot(fig)
