## Churn Prediction System

This module builds a calibrated churn prediction system for a SaaS platform,
designed to support proactive retention and risk prioritization.

### Modeling Strategy
- Feature selection using XGBoost importance
- Ensemble of XGBoost + CatBoost
- Probability calibration via Logistic Regression
- Threshold tuning optimized for F1-score

### Why calibration?
Raw model probabilities tend to be overconfident.
Calibration ensures probabilities can be interpreted as true churn risk.

### Outputs
- Churn probability per account
- Binary churn prediction
- Risk tiers for intervention prioritization

### Evaluation Summary
- ROC-AUC: ~0.67
- Focus: Recall–Precision balance, not raw accuracy
- Threshold chosen to maximize F1 while controlling false positives
