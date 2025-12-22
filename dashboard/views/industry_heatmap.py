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
    churn_path = os.path.join(BASE_DIR, "data", "behavior_data.csv")

    df = pd.read_csv(churn_path)
    df.columns = df.columns.str.lower().str.strip()

    # Keep only churned users
    df = df[df["churn_flag_y"] == True]

    # -----------------------------
    # PREP HEATMAP DATA
    # -----------------------------
    heatmap_df = (
        df.groupby(["industry", "reason_code"])
        .account_id
        .nunique()
        .reset_index(name="churned_accounts")
    )

    pivot_df = heatmap_df.pivot_table(
        index="industry",
        columns="reason_code",
        values="churned_accounts",
        fill_value=0
    )

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
        aspect="auto",
        color_continuous_scale=[
            "#2b0f4d",   # deep purple
            "#5b2d8b",
            "#a855f7",
            "#ff8fab"    # pink highlight
        ],
    )

    fig.update_layout(
        plot_bgcolor="#1b102f",
        paper_bgcolor="#1b102f",
        font=dict(color="#f5f3ff"),
        xaxis_title="Churn Reason",
        yaxis_title="Industry",
        coloraxis_colorbar=dict(title="Churned Accounts"),
    )

    fig.update_xaxes(side="top")

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # NEXT STEP PROMPT
    # -----------------------------
    st.markdown(
        "🧭 **Next:** Click an industry to explore reason codes, feedback, and feature impact."
    )
     
    # -----------------------------
    # INSIGHTS
    # -----------------------------
    st.markdown("### 🧠 Key Industry Insights")

    st.error("""
    **DevTools Is the Highest-Risk Industry**  
    Churn is heavily concentrated around **budget and pricing** rather than competitors.
    This indicates dissatisfaction with value perception, not product replacement.
    """)

    st.warning("""
    **HealthTech Churn Is Cost-Sensitive but Multi-Factor**  
    Budget remains the primary driver, with secondary pressure from pricing and support.
    Product fit appears strong, but affordability and service quality need attention.
    """)

    st.info("""
    **Cybersecurity Churn Is Support-Driven**  
    Churn volume is relatively low, but support-related issues dominate.
    Reliability and response quality are critical retention levers in this industry.
    """)

    st.info("""
    **FinTech Churn Reflects Pricing and Support Friction**  
    Churn reasons are distributed across budget, pricing, and support,
    suggesting optimization opportunities rather than structural product gaps.
    """)

    st.success("""
    **EdTech Shows the Healthiest Retention Profile**  
    Lowest churn across all categories, minimal pricing pressure,
    and manageable support-related exits.
    This industry represents a strong retention benchmark.
    """)

    st.markdown("""
    ⚠️ **Competitor-Driven Churn Is Universally Low**  
    Across industries, customers are **not leaving for better tools** —
    they are leaving due to **cost, support experience, or perceived value gaps**.
    """)

 
