import streamlit as st
import pandas as pd
import plotly.express as px
import os


def industry_reason_view():
    st.subheader("🎯 Industry × Churn Reason Breakdown")

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(BASE_DIR, "data", "behavior_data.csv")

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.lower().str.strip()

    # Only churned
    df = df[df["churn_flag_y"] == True]

    # Aggregate
    reason_df = (
        df.groupby(["industry", "reason_code"])
        .account_id
        .nunique()
        .reset_index(name="churned_accounts")
    )

    # Industry selector
    industry = st.selectbox(
        "Select Industry",
        sorted(reason_df["industry"].unique())
    )

    industry_df = reason_df[reason_df["industry"] == industry]

    # -----------------------------
    # BAR CHART
    # -----------------------------
    fig = px.bar(
        industry_df,
        x="reason_code",
        y="churned_accounts",
        color="reason_code",
        title=f"Why {industry} Customers Churn",
        color_discrete_sequence=[
            "#7FDBFF", "#FFB6C1", "#A855F7", "#FFD166", "#5EEAD4"
        ]
    )

    fig.update_layout(
        plot_bgcolor="#1b102f",
        paper_bgcolor="#1b102f",
        font=dict(color="#f5f3ff"),
        xaxis_title="Churn Reason",
        yaxis_title="Churned Accounts",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # TABLE
    # -----------------------------
    st.markdown("### 📋 Reason Code Summary")

    st.dataframe(
        industry_df.sort_values("churned_accounts", ascending=False),
        use_container_width=True
    )
