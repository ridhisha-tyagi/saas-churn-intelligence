import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def behavior_satisfaction_view():
    st.title("😊 Satisfaction Behavior")

    churn = pd.read_csv("data/churn.csv")
    retained = pd.read_csv("data/retained.csv")

    # Clean column names
    churn.columns = churn.columns.str.lower().str.strip()
    retained.columns = retained.columns.str.lower().str.strip()

    view = st.radio(
        "Select View",
        ["Churned Only", "Retained Only", "Comparison"],
        horizontal=True
    )

    months = list(range(-12, 1))

    if view == "Churned Only":
        df = (
            churn.groupby("months_before_churn")["satisfaction_score_y"]
            .mean()
            .reindex(months)
            .interpolate()
        )

        title = "Satisfaction Decline Before Churn"
        color = "#7FDBFF"  # sky blue

    elif view == "Retained Only":
        df = (
            retained.groupby("months_before_reference")["satisfaction_score"]
            .mean()
            .reindex(months)
            .interpolate()
        )

        title = "Stable Satisfaction in Retained Customers"
        color = "#FFB6C1"  # baby pink

    else:
        churn_df = (
            churn.groupby("months_before_churn")["satisfaction_score_y"]
            .mean()
            .reindex(months)
            .interpolate()
        )

        retained_df = (
            retained.groupby("months_before_reference")["satisfaction_score"]
            .mean()
            .reindex(months)
            .interpolate()
        )

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#1b102f")
    ax.set_facecolor("#1b102f")

    if view == "Comparison":
        ax.plot(months, churn_df, label="Churned", color="#7FDBFF", linewidth=3)
        ax.plot(months, retained_df, label="Retained", color="#FFB6C1", linewidth=3)
        ax.legend(facecolor="#1b102f", labelcolor="white")
    else:
        ax.plot(months, df, color=color, linewidth=3)

    ax.set_xlabel("Months Before Event", color="white")
    ax.set_ylabel("Avg Satisfaction Score", color="white")
    
    title = "divergence between churned and retained behavior"
    
    ax.set_title(title, color="white")
    ax.tick_params(colors="white")
    ax.grid(alpha=0.2)

    st.pyplot(fig)

    # INSIGHTS
    st.markdown("### 🔍 Insights")
    if view == "Churned Only":
        st.write("- Satisfaction steadily declines months before churn.")
        st.write("- Sharp drops often occur in the final 3 months.")
    elif view == "Retained Only":
        st.write("- Satisfaction remains stable or improves over time.")
    else:
        st.write("- Clear divergence between churned and retained behavior.")
        st.write("- Early satisfaction decline is a strong churn signal.")

    # -----------------------------
    # BACK BUTTON
    # -----------------------------
    if st.button("⬅ Back to Behavior Analysis", key="back_from_sat"):
        st.session_state.view = "behavior_analysis"
