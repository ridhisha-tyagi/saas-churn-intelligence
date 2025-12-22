import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


def product_feature_usage_view():
    st.title("🧩 Feature Usage vs Churn")

    st.markdown(
        "Understand which product features drive retention and which signal friction."
    )

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(BASE_DIR, "data", "full_behavior_data.csv")

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.lower().str.strip()

    # Safety check
    if "feature_name" not in df.columns or "usage_duration_min" not in df.columns:
        st.error("Required feature usage columns not found.")
        return

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
        .groupby("feature_name", as_index=False)["usage_duration_min"]
        .mean()
        .sort_values("usage_duration_min", ascending=True)
        .head(15)
    )

    retained_feat = (
        retained
        .groupby("feature_name", as_index=False)["usage_duration_min"]
        .mean()
        .sort_values("usage_duration_min", ascending=True)
        .head(15)
    )
    
    st.markdown("""
📌 **Product Implication**  
Features with **high churned usage + low retained usage** are **liability features**.
They absorb user effort without delivering outcomes and should be:
• simplified  
• fixed  
• or deprecated  
""")
    
    # -----------------------------
    # PLOT
    # -----------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#1b102f")
    ax.set_facecolor("#1b102f")

    if view == "Churned Only":
        ax.barh(
            churn_feat["feature_name"],
            churn_feat["usage_duration_min"],
            color="#FFB6C1"
        )
        title = "Top Features Used by Churned Customers"

    elif view == "Retained Only":
        ax.barh(
            retained_feat["feature_name"],
            retained_feat["usage_duration_min"],
            color="#7FDBFF"
        )
        title = "Top Features Used by Retained Customers"

    else:
        ax.barh(
            churn_feat["feature_name"],
            churn_feat["usage_duration_min"],
            color="#FFB6C1",
            alpha=0.7,
            label="Churned"
        )
        ax.barh(
            retained_feat["feature_name"],
            retained_feat["usage_duration_min"],
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
        "High feature usage among churned users often signals friction, "
        "instability, or unmet expectations — not lack of engagement."
    )
    st.markdown("### 🧠 Key Insights")

    st.error("""
**High Usage ≠ Retention**  
Several features (e.g., feature_27, feature_9, feature_37) show **higher average usage among churned users** than retained ones.
This indicates **friction-heavy engagement** — users are trying harder, not succeeding.
""")

    st.warning("""
**Overused but Underperforming Features**  
Features with strong churned usage but weaker retained usage likely suffer from:
• usability gaps  
• performance instability  
• unclear outcomes  

These features demand **product redesign, not promotion**.
""")

    st.info("""
**Retention Is Driven by Fewer, Stronger Features**  
Retained users concentrate usage around a **smaller set of high-impact features** (top blue bars),
suggesting clarity, efficiency, and value delivery.
""")

    st.success("""
**Feature Focus Beats Feature Breadth**  
Retained customers do not rely on many features —
they rely on the *right* ones.
This reinforces a **depth-over-breadth** product strategy.
""")

    st.warning("""
**Churned Users Exhibit Exploratory Behavior**  
Higher spread and volatility in churned feature usage
suggest customers are **searching for value**, not receiving it.
""")
 
    # -----------------------------
    # BACK
    # -----------------------------
    if st.button("⬅ Back to Product Breakdown", key="back_product_usage"):
        st.session_state.view = "product_breakdown"

