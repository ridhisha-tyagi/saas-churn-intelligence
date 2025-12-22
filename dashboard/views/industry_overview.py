import streamlit as st
import pandas as pd
import plotly.express as px
import os


def industry_heatmap_view():
    st.title("🔥 Industry × Churn Reason Heatmap")

    st.markdown(
        "This heatmap shows **why industries churn**, not just how much they churn."
    )

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    churn_path = os.path.join(BASE_DIR, "data", "churn.csv")

    df = pd.read_csv(churn_path)

    df.columns = df.columns.str.lower().str.strip()

    # -----------------------------
    # PREP HEATMAP DATA
    # -----------------------------
    heatmap_df = (
        df.groupby(["industry", "reason_code"])
        .account_id
        .nunique()
        .reset_index(name="churned_accounts")
    )

    pivot_df = heatmap_df.pivot(
        index="industry",
        columns="reason_code",
        values="churned_accounts"
    ).fillna(0)

    # Sort industries by total churn
    pivot_df["total"] = pivot_df.sum(axis=1)
    pivot_df = pivot_df.sort_values("total", ascending=False)
    pivot_df = pivot_df.drop(columns="total")

    # -----------------------------
    # HEATMAP
    # -----------------------------
    fig = px.imshow(
        pivot_df,
        text_auto=True,
        color_continuous_scale=[
            "#2b0f4d",   # deep purple
            "#5b2d8b",
            "#a855f7",
            "#ff8fab"    # pink highlight
        ],
        aspect="auto"
    )

    fig.update_layout(
        plot_bgcolor="#1b102f",
        paper_bgcolor="#1b102f",
        font=dict(color="#f5f3ff"),
        xaxis_title="Churn Reason",
        yaxis_title="Industry",
        coloraxis_colorbar=dict(
            title="Churned Accounts"
        )
    )

    fig.update_xaxes(side="top")

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # INSIGHT PROMPT (NO INSIGHTS YET)
    # -----------------------------
    st.markdown(
        "🧭 **Click an industry next** to explore reason codes, feedback, and feature impact."
    )

    # -----------------------------
    # BACK BUTTON
    # -----------------------------
    if st.button("⬅ Back to Analysis", key="back_from_industry_heatmap"):
        st.session_state.view = "analysis"
