import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_loader import load_data


def behavior_errors_view():
    st.title("🚨 Error Behavior")

    # ======================
    # LOAD DATA
    # ======================
    churn = load_data("churn.csv")
    retained = load_data("retained.csv"))

    # Normalize columns
    churn.columns = churn.columns.str.lower().str.strip()
    retained.columns = retained.columns.str.lower().str.strip()

    # ======================
    # MODE SELECTOR
    # ======================
    view = st.radio(
        "Select View",
        ["Churned Only", "Retained Only", "Comparison"],
        horizontal=True
    )

    months = list(range(-12, 1))

    # ======================
    # DATA PREP
    # ======================
    if view == "Churned Only":
        df = (
            churn.groupby("months_before_churn")["error_count_y"]
            .mean()
            .reindex(months)
            .interpolate()
        )

        title = "Error Escalation Before Churn"
        color = "#7FDBFF"  # sky blue

    elif view == "Retained Only":
        df = (
            retained.groupby("months_before_reference")["error_count"]
            .mean()
            .reindex(months)
            .interpolate()
        )

        title = "Stable Error Patterns in Retained Customers"
        color = "#FFB6C1"  # baby pink

    else:
        churn_df = (
            churn.groupby("months_before_churn")["error_count_y"]
            .mean()
            .reindex(months)
            .interpolate()
        )

        retained_df = (
            retained.groupby("months_before_reference")["error_count"]
            .mean()
            .reindex(months)
            .interpolate()
        )

    # ======================
    # PLOT
    # ======================
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#1b102f")
    ax.set_facecolor("#1b102f")

    if view == "Comparison":
        ax.plot(
            months,
            churn_df,
            label="Churned",
            color="#7FDBFF",
            linewidth=3
        )
        ax.plot(
            months,
            retained_df,
            label="Retained",
            color="#FFB6C1",
            linewidth=3
        )
        ax.legend(facecolor="#1b102f", labelcolor="white")

    else:
        ax.plot(months, df, color=color, linewidth=3)

    ax.set_xlabel("Months Before Event", color="white")
    ax.set_ylabel("Avg Errors per User", color="white")
    ax.set_title("Divergence in Error Behavior Over Time", color="white")
    ax.tick_params(colors="white")
    ax.grid(alpha=0.25)

    st.pyplot(fig)

    # ======================
    # INSIGHTS
    # ======================
    st.markdown("### 🔍 Insights")

    if view == "Churned Only":
        st.write("• Error rates fluctuate sharply before churn.")
        st.write("• Peaks appear 4–6 months prior to churn events.")
        st.write("• Volatility indicates unresolved technical friction.")

    elif view == "Retained Only":
        st.write("• Errors occur but remain controlled and predictable.")
        st.write("• Stable error handling supports long-term retention.")

    else:
        st.write("• Churned users show erratic error spikes.")
        st.write("• Retained users maintain consistent error patterns.")
        st.write("• Instability—not volume—is the dominant churn signal.")

    # -----------------------------
    # BACK BUTTON
    # -----------------------------
    if st.button("⬅ Back to Behavior Analysis", key="back_from_errors"):
        st.session_state.view = "behavior_analysis"
