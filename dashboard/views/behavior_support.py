import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils.data_loader import load_data


def behavior_support_view():
    st.title("🎧 Support Behavior")

    # ======================
    # LOAD DATA
    # ======================
    churn = load_data("churn.csv")
    retained = load_data("retained.csv")

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
            churn.groupby("months_before_churn")
            .agg(
                tickets=("ticket_id", "count"),
                users=("account_id", "nunique")
            )
            .assign(avg_tickets=lambda x: x.tickets / x.users)
            .reindex(months)
        )

        series = df["avg_tickets"].interpolate()
        title = "Support Ticket Escalation Before Churn"
        color = "#7FDBFF"

    elif view == "Retained Only":
        df = (
            retained.groupby("months_before_reference")
            .agg(
                tickets=("ticket_id", "count"),
                users=("account_id", "nunique")
            )
            .assign(avg_tickets=lambda x: x.tickets / x.users)
            .reindex(months)
        )

        series = df["avg_tickets"].interpolate()
        title = "Stable Support Usage in Retained Customers"
        color = "#FFB6C1"

    else:
        churn_df = (
            churn.groupby("months_before_churn")
            .agg(
                tickets=("ticket_id", "count"),
                users=("account_id", "nunique")
            )
            .assign(avg_tickets=lambda x: x.tickets / x.users)
            .reindex(months)
        )

        retained_df = (
            retained.groupby("months_before_reference")
            .agg(
                tickets=("ticket_id", "count"),
                users=("account_id", "nunique")
            )
            .assign(avg_tickets=lambda x: x.tickets / x.users)
            .reindex(months)
        )

        churn_series = churn_df["avg_tickets"].interpolate()
        retained_series = retained_df["avg_tickets"].interpolate()

    # ======================
    # PLOT
    # ======================
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#1b102f")
    ax.set_facecolor("#1b102f")

    if view == "Comparison":
        ax.plot(
            months,
            churn_series,
            label="Churned Users",
            color="#7FDBFF",
            linewidth=3
        )
        ax.plot(
            months,
            retained_series,
            label="Retained Users",
            color="#FFB6C1",
            linewidth=3
        )
        ax.legend(facecolor="#1b102f", labelcolor="white")

    else:
        ax.plot(months, series, color=color, linewidth=3)

    ax.set_xlabel("Months Before Event", color="white")
    ax.set_ylabel("Avg Tickets per User", color="white")
    ax.set_title("Ticket behaviour Churned VS Retained Customers.", color="white")
    ax.tick_params(colors="white")
    ax.grid(alpha=0.25)

    st.pyplot(fig)

    # ======================
    # INSIGHTS (KEEP — YOU ASKED)
    # ======================
    st.markdown("### 🧠 Key Insights")

    if view == "Churned Only":
        st.write("• Ticket volume rises sharply 4–6 months before churn.")
        st.write("• Escalation reflects unresolved friction, not engagement.")
        st.write("• Support stress is an early churn warning signal.")

    elif view == "Retained Only":
        st.write("• Retained users raise tickets consistently over time.")
        st.write("• High ticket volume alone does not imply churn.")
        st.write("• Stability and resolution quality matter more than count.")

    else:
        st.write("• Churned users show volatile ticket spikes.")
        st.write("• Retained users exhibit predictable support behavior.")
        st.write("• Instability—not volume—is the differentiator.")

    # ======================
    # BACK BUTTON
    # ======================
    if st.button("⬅ Back to Behavior Analysis", key="back_from_support"):
        st.session_state.view = "behavior_analysis"
