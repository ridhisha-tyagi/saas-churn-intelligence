import streamlit as st
from styles.theme import apply_theme

from views.home import home_view
from views.analysis import analysis_view
from views.feature_analysis import feature_analysis_view
from views.behavior_analysis import behavior_analysis_view
from views.industry_analysis import industry_analysis_view
from views.feature_detail import feature_detail_view
from views.behavior_satisfaction import behavior_satisfaction_view
from views.behavior_usage import behavior_usage_view 
from views.behavior_support import behavior_support_view
from views.behaviour_errors import behavior_errors_view
from views.industry_heatmap import industry_heatmap_view
from views.industry_reason import industry_reason_view
from views.industry_feedback import industry_feedback_view
from views.product_breakdown import product_breakdown_view
from views.product_feature_usage import product_feature_usage_view
from views.product_feature_health import product_feature_health_view
from views.product_retention_drivers import product_retention_drivers_view
from views.product_churn_drivers import product_churn_drivers_view
from views.product_final_insights import product_final_insights_view
from views.churn_prediction import churn_prediction_view

st.set_page_config(layout="wide")
apply_theme()

# -----------------------------
# Session state initialization
# -----------------------------
if "view" not in st.session_state:
    st.session_state.view = "home"

if "selected_insight" not in st.session_state:
    st.session_state.selected_insight = None

if "selected_feature" not in st.session_state:
    st.session_state.selected_feature = None


if st.session_state.view == "home":
    home_view()

elif st.session_state.view == "analysis":
    analysis_view()

elif st.session_state.view == "feature_analysis":
    feature_analysis_view()

elif st.session_state.view == "feature_detail":
    feature_detail_view()

elif st.session_state.view == "behavior_analysis":
    behavior_analysis_view()

elif st.session_state.view == "behavior_satisfaction":
    behavior_satisfaction_view()

elif st.session_state.view == "behavior_usage":
    behavior_usage_view()
    
elif st.session_state.view == "behavior_support":
    behavior_support_view()
    
elif st.session_state.view == "behavior_errors":
    behavior_errors_view()

elif st.session_state.view == "industry_analysis":
    industry_analysis_view()

elif st.session_state.view == "industry_heatmap":
    industry_heatmap_view()    
  
elif st.session_state.view == "industry_reason":
    industry_reason_view()  

elif st.session_state.view == "industry_feedback":
    industry_feedback_view()      
    
elif st.session_state.view == "product_breakdown":
    product_breakdown_view()

elif st.session_state.view == "product_feature_usage":
    product_feature_usage_view()

elif st.session_state.view == "product_feature_health":
    product_feature_health_view()
    
elif st.session_state.view == "product_retention_drivers":
    product_retention_drivers_view()

elif st.session_state.view == "product_churn_drivers":
    product_churn_drivers_view()
    
elif st.session_state.view == "product_final_insights":
    product_final_insights_view()    
    
elif st.session_state.view == "churn_prediction":
    churn_prediction_view()


    


import os
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "feature_insights.csv"


df = pd.read_csv(DATA_PATH)
df.columns = (
    df.columns
    .str.replace("\ufeff", "", regex=False)
    .str.replace("\xa0", "", regex=False)
    .str.strip()
    .str.lower()
)

df.columns = df.columns.str.strip().str.lower()



