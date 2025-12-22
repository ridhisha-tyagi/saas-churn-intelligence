import streamlit as st
import pandas as pd
import os


def generate_product_action(row, dominant_theme, top_reason, df):
    actions = []  # ✅ FIXED: no recursion
    # -----------------------------
    # LOAD DATA
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(BASE_DIR, "data", "full_behavior_data.csv")

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.lower().str.strip()

    if row["avg_errors"] > df["error_sum"].median():
        actions.append("Stabilize feature reliability and reduce errors")

    if row["avg_satisfaction"] < df["satisfaction_score"].median():
        actions.append("Improve UX and address usability friction")

    if top_reason in ["pricing", "budget"]:
        actions.append("Re-evaluate value perception and pricing communication")

    if dominant_theme == "mixed":
        actions.append("Improve support responsiveness for this feature")

    if row["avg_usage"] < df["usage_avg_min"].median():
        actions.append("Improve onboarding and feature discoverability")

    if not actions:
        actions.append("Monitor closely; no immediate intervention required")

    return actions


def product_final_insights_view():
    st.title("🧠 Final Product Insights")

    st.markdown(
        "Feature-level diagnosis based on **real churn behavior**, "
        "**user complaints**, and **usage patterns**."
    )

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(BASE_DIR, "data", "full_behavior_data.csv")

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.lower().str.strip()

    required_cols = [
        "feature_name", "account_id", "churn_flag_y",
        "usage_duration_min", "error_count", "satisfaction_score"
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        return

    total_accounts = df["account_id"].nunique()

    # -----------------------------
    # FEATURE METRICS
    # -----------------------------
    feat = (
        df.groupby("feature_name")
        .agg(
            adoption=("account_id", "nunique"),
            avg_usage=("usage_duration_min", "mean"),
            avg_errors=("error_count", "mean"),
            avg_satisfaction=("satisfaction_score", "mean"),
            churned_users=("churn_flag_y", "sum")
        )
        .reset_index()
    )

    feat["adoption_rate"] = feat["adoption"] / total_accounts
    feat["churn_risk"] = feat["churned_users"] / feat["adoption"]
    feat = feat.fillna(0)

    feat["risk_score"] = (
        0.6 * feat["churn_risk"] +
        0.2 * feat["avg_errors"].rank(pct=True) +
        0.2 * (1 - feat["avg_satisfaction"].rank(pct=True))
    )

    critical = feat.sort_values("risk_score", ascending=False).head(10)

    retention = (
        feat.sort_values(
            ["churn_risk", "avg_satisfaction"],
            ascending=[True, False]
        )
        .head(10)
    )

    tab1, tab2 = st.tabs([
        "🔴 Critical Risk Features",
        "🟢 Retention Anchors"
    ])

    # =============================
    # 🔴 TAB 1 — CHURN
    # =============================
    with tab1:
        st.subheader("Features Driving Churn")

        for _, row in critical.iterrows():
            feature = row["feature_name"]

            churn_df = df[
                (df["feature_name"] == feature) &
                (df["churn_flag_y"] == True)
            ]

            top_reason = (
                churn_df["reason_code"].value_counts().idxmax()
                if "reason_code" in churn_df and not churn_df.empty
                else "unknown"
            )

            st.error(f"### 🔴 {feature}")

            st.markdown(f"""
**Signals**
- Adoption: **{row['adoption_rate']*100:.1f}%**
- Churn risk: **{row['churn_risk']*100:.1f}%**
- Avg satisfaction: **{row['avg_satisfaction']:.2f}**
- Avg errors: **{row['avg_errors']:.2f}**


""")

            dominant_theme = "mixed"
            actions = generate_product_action(row, dominant_theme, top_reason, df)

            st.markdown("**Recommended Product Actions**")
            for act in actions:
                st.write(f"- {act}")

    # =============================
    # 🟢 TAB 2 — RETENTION
    # =============================
    with tab2:
        st.subheader("Features That Retain Users")

        for _, row in retention.iterrows():
            feature = row["feature_name"]

            st.success(f"### 🟢 {feature}")

            st.markdown(f"""
**Why this retains users**
- Adoption: **{row['adoption_rate']*100:.1f}%**
- Churn risk: **{row['churn_risk']*100:.1f}%**
- Avg satisfaction: **{row['avg_satisfaction']:.2f}**
- Avg usage: **{row['avg_usage']:.1f} mins**
""")

            dominant_theme = "mixed"
            top_reason = "retention"
            actions = generate_product_action(row, dominant_theme, top_reason, df)

            st.markdown("**Recommended Product Actions**")
            for act in actions:
                st.write(f"- {act}")

    if st.button("⬅ Back to Product Breakdown"):
        st.session_state.view = "product_breakdown"
