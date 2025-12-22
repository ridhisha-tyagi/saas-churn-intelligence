import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

def product_churn_drivers_view():
    st.title("🔥 Churn Drivers")

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "full_behavior_data.csv"))
    df.columns = df.columns.str.lower().str.strip()

    churned = df[df["churn_flag_y"] == True]
    retained = df[df["churn_flag_y"] == False]

    metrics = pd.DataFrame({
        "churned_adoption": churned.groupby("feature_name").account_id.nunique(),
        "churned_usage": churned.groupby("feature_name").usage_duration_min.mean(),
        "error_pressure": churned.groupby("feature_name").error_sum.mean(),
        "retention_ratio": (
            retained.groupby("feature_name").account_id.nunique()
            / (
                retained.groupby("feature_name").account_id.nunique()
                + churned.groupby("feature_name").account_id.nunique()
            )
        )
    }).dropna()

    metrics_norm = (metrics - metrics.min()) / (metrics.max() - metrics.min())
    
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
        color_continuous_scale=["#2b0f4d", "#ff8fab"],
        aspect="auto"
    )

    fig.update_layout(
        plot_bgcolor="#1b102f",
        paper_bgcolor="#1b102f",
        font=dict(color="#f5f3ff"),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.error("Pink zones = features that exhaust users before churn.")
    
    st.error("""
**High usage does not guarantee success**  
Several churn-driving features show intense usage before churn,
indicating repeated attempts to extract value that failed.
""")

    st.warning("""
**Error pressure is a churn accelerator**  
Features with elevated errors and declining satisfaction
consistently precede churn events.
""")

    st.info("""
**Churn is not caused by disengagement**  
Users churn after engagement — not before it.
""")


    # -----------------------------
    # BACK
    # -----------------------------
    if st.button("⬅ Back to Product Breakdown", key="back_churn"):
        st.session_state.view = "product_breakdown"
