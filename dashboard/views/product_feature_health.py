import streamlit as st
import pandas as pd
import plotly.express as px
import os

def product_feature_health_view():
    st.title("🧩 Feature Health Matrix")

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "full_behavior_data.csv"))
    df.columns = df.columns.str.lower().str.strip()

    feature_health = (
        df.groupby("feature_name")
        .agg(
            adoption=("account_id", "nunique"),
            avg_usage=("usage_duration_min", "mean"),
            avg_errors=("error_sum", "mean"),
            avg_satisfaction=("satisfaction_avg", "mean")
        )
    )

    feature_health_norm = (
        feature_health - feature_health.min()
    ) / (feature_health.max() - feature_health.min())
    
    st.warning(
        "Pink = fragile features · Purple = neutral · Blue = healthy core"
    )
    
    fig = px.imshow(
        feature_health_norm,
        color_continuous_scale=[
            "#2b0f4d", "#5b2d8b", "#a855f7", "#ff8fab"
        ],
        aspect="auto"
    )

    fig.update_layout(
        plot_bgcolor="#1b102f",
        paper_bgcolor="#1b102f",
        font=dict(color="#f5f3ff"),
    )

    st.plotly_chart(fig, use_container_width=True)

    
    st.info("""
**Not all popular features are healthy**  
High adoption combined with low satisfaction indicates expectation gaps.
""")

    st.warning("""
**Errors only hurt when unresolved**  
Features with high errors but stable satisfaction show tolerance —
once satisfaction drops, churn risk spikes.
""")

    st.success("""
**Hidden gems exist**  
Low-adoption, high-satisfaction features represent expansion opportunities.
""")

    
    # -----------------------------
    # BACK
    # -----------------------------
    if st.button("⬅ Back to Product Breakdown", key="health_heatmap"):
        st.session_state.view = "product_breakdown"