import pandas as pd
import streamlit as st

def feature_analysis_view():
    st.title("🔍 Feature Insights")

    df = pd.read_csv("data/feature_insights.csv")

    df.columns = (
        df.columns
        .str.replace("\ufeff", "", regex=False)
        .str.replace("\xa0", "", regex=False)
        .str.strip()
        .str.lower()
    )

    if "selected_insight" not in st.session_state:
        st.session_state.selected_insight = None

    insight_counts = df["final_insights"].value_counts()

    st.subheader("Select an Insight Bucket")

    st.subheader("Insight Buckets")

    cols = st.columns(len(insight_counts))

    for col, (insight, count) in zip(cols, insight_counts.items()):
        with col:
            if st.button(
                f"{insight}\n({count})",
                key=f"insight_{insight}"
                ):
                    st.session_state.selected_insight = insight
                    st.session_state.view = "feature_detail"


    st.divider()

    if st.button("⬅ Back to Analysis", key="back_from_feature_analysis"):
        st.session_state.view = "analysis"
