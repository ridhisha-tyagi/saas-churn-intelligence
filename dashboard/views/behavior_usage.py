import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def behavior_usage_view():
    st.title("📊 Usage Behavior")

    # Load data
    churn = pd.read_csv("data/churn.csv")
    retained = pd.read_csv("data/retained.csv")

    # Normalize columns
    churn.columns = churn.columns.str.lower().str.strip()
    retained.columns = retained.columns.str.lower().str.strip()

    # Mode selector
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
            churn.groupby("months_before_churn")["usage_duration_min_y"]
            .mean()
            .reindex(months)
            .interpolate()
        )

        title = "Usage Decline Before Churn"
        color = "#7FDBFF"  # sky blue

    elif view == "Retained Only":
        df = (
            retained.groupby("months_before_reference")["usage_duration_min"]
            .mean()
            .reindex(months)
            .interpolate()
        )

        title = "Stable Usage in Retained Customers"
        color = "#FFB6C1"  # baby pink

    else:
        churn_df = (
            churn.groupby("months_before_churn")["usage_duration_min_y"]
            .mean()
            .reindex(months)
            .interpolate()
        )

        retained_df = (
            retained.groupby("months_before_reference")["usage_duration_min"]
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
    ax.set_ylabel("Avg Usage (Minutes)", color="white")
    title = "divergence between churned and retained behaviour"
    ax.set_title(title, color="white")
    ax.tick_params(colors="white")
    ax.grid(alpha=0.25)

    st.pyplot(fig)

    # ======================
    # INSIGHTS
    # ======================
    st.markdown("### 🔍 Insights")

    if view == "Churned Only":
        st.write("• Usage steadily declines in the months leading up to churn.")
        st.write("• Drop-offs often accelerate in the final 2–3 months.")
        st.write("• Early disengagement is a strong churn warning signal.")

    elif view == "Retained Only":
        st.write("• Usage remains stable or gradually increases.")
        st.write("• Consistent engagement correlates strongly with retention.")

    else:
        st.write("• Clear divergence between churned and retained users.")
        st.write("• Usage decline precedes churn well before the churn date.")
        st.write("• Monitoring usage drops enables proactive intervention.")

    # -----------------------------
    # BACK BUTTON
    # -----------------------------
    if st.button("⬅ Back to Behavior Analysis", key="back_from_usage"):
        st.session_state.view = "behavior_analysis"