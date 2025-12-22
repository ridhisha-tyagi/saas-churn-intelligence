import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

def product_feature_usage_view():
    st.title("🧩 Feature Usage vs Churn")

    st.markdown(
        "Understand which product features drive retention and which fail users."
    )

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(BASE_DIR, "data", "behavior_data.csv")

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.lower().str.strip()

    churned = df[df["churn_flag_y"] == True]
    retained = df[df["churn_flag_y"] == False]

    # -----------------------------
    # VIEW SELECTOR
    # -----------------------------
    view = st.radio(
        "Select View",
        ["Churned Only", "Retained Only", "Comparison"],
        horizontal=True
    )

    # -----------------------------
    # AGGREGATION
    # -----------------------------
    churn_feat = (
        churned
        .groupby("feature_name")["usage_duration_min"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
    )

    retained_feat = (
        retained
        .groupby("feature_name")["usage_duration_min"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
    )

    # -----------------------------
    # PLOT
    # -----------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#1b102f")
    ax.set_facecolor("#1b102f")

    if view == "Churned Only":
        churn_feat.plot(
            kind="barh",
            ax=ax,
            color="#FFB6C1"
        )
        title = "Top Features Used by Churned Customers"

    elif view == "Retained Only":
        retained_feat.plot(
            kind="barh",
            ax=ax,
            color="#7FDBFF"
        )
        title = "Top Features Used by Retained Customers"

    else:
        churn_feat.plot(
            kind="barh",
            ax=ax,
            color="#FFB6C1",
            alpha=0.7,
            label="Churned"
        )
        retained_feat.plot(
            kind="barh",
            ax=ax,
            color="#7FDBFF",
            alpha=0.7,
            label="Retained"
        )
        ax.legend(facecolor="#1b102f", labelcolor="white")
        title = "Feature Usage: Churned vs Retained"

    ax.set_title(title, color="white")
    ax.set_xlabel("Average Usage (Minutes)", color="white")
    ax.set_ylabel("Feature", color="white")
    ax.tick_params(colors="white")
    ax.grid(alpha=0.25)

    st.pyplot(fig)

    # -----------------------------
    # INSIGHT PLACEHOLDER
    # -----------------------------
    st.markdown("### 🧠 What This Reveals")
    st.info(
        "Features heavily used by churned users may indicate friction, instability, "
        "or unmet expectations — not lack of engagement."
    )

    # -----------------------------
    # BACK
    # -----------------------------
    if st.button("⬅ Back to Home", key="back_product_usage"):
        st.session_state.view = "home"
