import streamlit as st
import pandas as pd
import os


def churn_prediction_view():
    st.title("🔮 Churn Risk Prediction")

    st.markdown(
        "Customer-level churn risk based on behavioral signals. "
        "Predictions are intended for prioritization and proactive intervention."
    )

    # -----------------------------
    # LOAD PREDICTION RESULTS
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(
        BASE_DIR,
        "outputs",
        "final_churn_insights_table.csv"  # <-- internal dataset (MAIN)
    )

    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        st.error("Churn prediction file not found. Please generate predictions first.")
        return
        
    #----------------------------
    risk_options = df["risk_level"].unique().tolist()

    selected_risks = st.multiselect(
    "Filter by risk level",
    options=risk_options,
    default=risk_options
)
    filtered_df = df[df["risk_level"].isin(selected_risks)]

    # -----------------------------
    # HIGH-LEVEL METRICS
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric(
    "High Risk Customers",
    (filtered_df["risk_level"] == "High Risk").sum()
)

    col2.metric(
    "Medium Risk Customers",
    (filtered_df["risk_level"] == "Medium Risk").sum()
)

    col3.metric(
    "Average Churn Risk",
    f"{filtered_df['churn_probability'].mean() * 100:.1f}%"
    if len(filtered_df) > 0 else "—"
)


    st.divider()
    
    with st.expander("ℹ️ How to interpret churn risk"):
        st.markdown("""
- **Risk level** indicates the urgency of intervention.
- **Risk drivers** highlight factors increasing churn likelihood.
- **Retention signals** indicate behaviors stabilizing the customer.
- Predictions are probabilistic and intended for prioritization, not certainty.
""")
   


    # -----------------------------
    # DISPLAY TABLE
    # -----------------------------
    display_cols = [
        "account_id",
        "risk_level",
        "churn_probability_percent",
        "risk_drivers",
        "retention_protectors"
    ]

    st.subheader("Customer Churn Risk Overview")

    st.dataframe(
    filtered_df[display_cols]
        .sort_values("churn_probability_percent", ascending=False),
    use_container_width=True
)

    
    st.markdown("### 🧭 Recommended Next Actions")

    st.markdown("""
- **High Risk**: Immediate outreach, product or support intervention.
- **Medium Risk**: Monitor closely and reinforce value communication.
- **Low Risk**: Maintain experience and identify expansion opportunities.
""")


    st.caption(
    "Use the filter to focus on specific churn risk segments for targeted action."
)


    # -----------------------------
    # NAVIGATION
    # -----------------------------
    if st.button("⬅ Back to Home"):
        st.session_state.view = "home"
