import pandas as pd
import streamlit as st

def feature_detail_view():
    st.title("📌 Feature Health Card")

    df = pd.read_csv("data/feature_insights.csv")
    df.columns = df.columns.str.strip().str.lower()

    insight = st.session_state.get("selected_insight")

    if insight is None:
        st.warning("No insight selected.")
        if st.button("⬅ Back"):
            st.session_state.view = "feature_analysis"
        return

    subset = df[df["final_insights"] == insight]

    st.subheader(f"Insight: {insight}")

    for _, row in subset.iterrows():
        with st.expander(f"🧩 {row['feature_name']}"):
            st.write(f"**Risk Rank:** {row['risk_rank']} ({row['risk_bucket']})")
            st.write(f"**Health Rank:** {row['health_rank']} ({row['health_bucket']})")
            st.write(f"**Final Rank:** {row['final_rank']} ({row['final_bucket']})")

    if st.button("⬅ Back to Feature Insights", key="back_to_feature_analysis"):
        st.session_state.view = "feature_analysis"
