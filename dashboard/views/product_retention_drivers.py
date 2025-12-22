import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

def product_retention_drivers_view():
    
    st.title("🧲 Retention Driver Features")

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "full_behavior_data.csv"))
    df.columns = df.columns.str.lower().str.strip()

    retained = df[df["churn_flag_y"] == False]
    churned = df[df["churn_flag_y"] == True]

    metrics = pd.DataFrame({
        "retained_adoption": retained.groupby("feature_name").account_id.nunique(),
        "retained_usage": retained.groupby("feature_name").usage_duration_min.mean(),
        "retention_ratio": (
            retained.groupby("feature_name").account_id.nunique()
            / (
                retained.groupby("feature_name").account_id.nunique()
                + churned.groupby("feature_name").account_id.nunique()
            )
        )
    }).dropna()

    metrics_norm = (metrics - metrics.min()) / (metrics.max() - metrics.min())
     
     # -----------------------------
    # EXPLANATION (BEFORE GRAPH)
    # -----------------------------
    st.markdown("""
    ### 📌 What this shows
    This heatmap highlights **features that actively contribute to user retention**.

    **How to read it:**
    - **Brighter cells** = stronger retention signal
    - **Adoption** → how many retained users use the feature  
    - **Usage** → how deeply they use it  
    - **Retention Ratio** → how strongly it correlates with staying  

    👉 Features that are bright across columns are **core retention drivers**.
    """) 
     
     
    fig = px.imshow(
        metrics_norm,
        color_continuous_scale=["#2b0f4d", "#5b2d8b", "#7FDBFF"],
        aspect="auto"
    )

    fig.update_layout(
        plot_bgcolor="#1b102f",
        paper_bgcolor="#1b102f",
        font=dict(color="#f5f3ff"),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success("Features glowing blue here are your retention backbone.")
    
    # -----------------------------
    # INSIGHTS (AFTER GRAPH)
    # -----------------------------
    st.markdown("### 🧠 Key Insights")

    st.success("""
    **Retention is driven by depth, not surface-level usage**  
    Features with high retained usage consistently show stronger retention impact,
    even when adoption is not universal.
    """)

    st.info("""
    **Some features act as silent anchors**  
    Moderate adoption but high retention ratio indicates workflow-level dependency,
    not novelty-based engagement.
    """)

    st.warning("""
    **Low-usage retention drivers are fragile**  
    These features must be protected from breaking changes or UX regressions.
    """)

    
# -----------------------------
    # BACK
    # -----------------------------
    if st.button("⬅ Back to Product Breakdown", key="back_retain"):
        st.session_state.view = "product_breakdown"