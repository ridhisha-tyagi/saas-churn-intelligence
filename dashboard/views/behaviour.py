import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# -----------------------------
# THEME COLORS (CONSISTENT)
# -----------------------------
BG_COLOR = "#2b124c"        # dark purple
GRID_COLOR = "rgba(255,255,255,0.15)"
CHURN_COLOR = "#ff9ad5"     # baby pink
RETAIN_COLOR = "#7fd7ff"    # sky blue

# -----------------------------
# DATA LOADING
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

CHURN_PATH = os.path.join(DATA_DIR, "churn.csv")
RETAIN_PATH = os.path.join(DATA_DIR, "retained.csv")

def load_data():
    churn = pd.read_csv(CHURN_PATH)
    retained = pd.read_csv(RETAIN_PATH)

    churn["months"] = churn["months_before_churn"]
    retained["months"] = retained["months_before_reference"]

    return churn, retained

# -----------------------------
# MONTHLY AGGREGATION
# -----------------------------
def monthly_error_avg(df, error_col):
    return (
        df.groupby("months")
          .agg(avg_errors=(error_col, "mean"))
          .reset_index()
          .sort_values("months")
    )

# -----------------------------
# PLOTTING
# -----------------------------
def line_plot(x, y, label, color):
    return go.Scatter(
        x=x,
        y=y,
        mode="lines+markers",
        name=label,
        line=dict(color=color, width=3),
        marker=dict(size=7)
    )

def base_layout(title, y_label):
    return dict(
        title=title,
        plot_bgcolor=BG_COLOR,
        paper_bgcolor=BG_COLOR,
        font=dict(color="white"),
        xaxis=dict(
            title="Months Relative to Event",
            gridcolor=GRID_COLOR,
            zeroline=False
        ),
        yaxis=dict(
            title=y_label,
            gridcolor=GRID_COLOR,
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

# -----------------------------
# MAIN VIEW
# -----------------------------
def behavior_errors_view():
    st.title("🚨 Error Behavior Analysis")

    churn, retained = load_data()

    churn_monthly = monthly_error_avg(churn, "error_count_x")
    retained_monthly = monthly_error_avg(retained, "error_count")

    # -----------------------------
    # CHURNED ONLY
    # -----------------------------
    fig_churn = go.Figure()
    fig_churn.add_trace(
        line_plot(
            churn_monthly["months"],
            churn_monthly["avg_errors"],
            "Churned Users",
            CHURN_COLOR
        )
    )
    fig_churn.update_layout(
        **base_layout(
            "Monthly Error Trend — Churned Users",
            "Avg Errors per User"
        )
    )
    st.plotly_chart(fig_churn, use_container_width=True)

    # -----------------------------
    # RETAINED ONLY
    # -----------------------------
    fig_retained = go.Figure()
    fig_retained.add_trace(
        line_plot(
            retained_monthly["months"],
            retained_monthly["avg_errors"],
            "Retained Users",
            RETAIN_COLOR
        )
    )
    fig_retained.update_layout(
        **base_layout(
            "Monthly Error Trend — Retained Users",
            "Avg Errors per User"
        )
    )
    st.plotly_chart(fig_retained, use_container_width=True)

    # -----------------------------
    # COMPARISON
    # -----------------------------
    fig_compare = go.Figure()
    fig_compare.add_trace(
        line_plot(
            churn_monthly["months"],
            churn_monthly["avg_errors"],
            "Churned Users",
            CHURN_COLOR
        )
    )
    fig_compare.add_trace(
        line_plot(
            retained_monthly["months"],
            retained_monthly["avg_errors"],
            "Retained Users",
            RETAIN_COLOR
        )
    )
    fig_compare.update_layout(
        **base_layout(
            "Error Behavior — Churned vs Retained",
            "Avg Errors per User"
        )
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    # -----------------------------
    # BACK BUTTON
    # -----------------------------
    if st.button("⬅ Back to Behavior Analysis", key="back_from_errors"):
        st.session_state.view = "behavior_analysis"
