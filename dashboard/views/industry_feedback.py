import streamlit as st
import pandas as pd
import os


def industry_feedback_view():
    st.subheader("💬 Industry Feedback Insights")

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(BASE_DIR, "data", "behavior_data.csv")

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.lower().str.strip()

    # Only churned
    df = df[df["churn_flag_y"] == True]

    industry = st.selectbox(
        "Select Industry",
        sorted(df["industry"].dropna().unique())
    )

    industry_df = df[df["industry"] == industry]

    # -----------------------------
    # REASON CODE SUMMARY
    # -----------------------------
    st.markdown("### 🧠 Top Churn Drivers")

    reason_counts = (
        industry_df["reason_code"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Reason", "reason_code": "Count"})
    )

    st.dataframe(reason_counts, use_container_width=True)

    # -----------------------------
    # FEEDBACK TEXT
    # -----------------------------
    st.markdown("### 🗣️ What Customers Said")
    
    feedback_df = industry_df[["reason_code", "feedback_text"]].dropna()

    if feedback_df.empty:
        st.warning("No qualitative feedback available for this industry.")
        return

    feedback_samples = feedback_df.sample(
        n=min(10, len(feedback_df)),
         random_state=42
        )

    for _, row in feedback_samples.iterrows():
        st.markdown(
            f"""
            <div style="
                background-color:#2b0f4d;
                padding:12px;
                border-radius:8px;
                margin-bottom:10px;
                color:#f5f3ff;
            ">
            <b>Reason:</b> {row['reason_code']}<br>
            <i>{row['feedback_text']}</i>
            </div>
            """,
            unsafe_allow_html=True
        )
