# SaaS Churn Intelligence System

This project is an end-to-end churn analysis and product insight system built to investigate churn drivers, retention signals, and feature-level health in a SaaS product.

The goal was not only to predict churn, but to explain *why* churn happens and translate data signals into actionable product decisions and leverage observed patterns to build a churn prediction model.

## Problem Statement

SaaS companies often face churn without clear visibility into:
- which features drive churn
- which behaviors signal early risk
- which product areas deserve intervention versus monitoring

Traditional churn models provide probabilities, but fail to connect predictions to product actions.

This project addresses that gap by combining:
- behavioral analysis
- feature-level diagnostics
- churn risk scoring
- explainable product recommendations

## Data & Scope

The analysis uses a simulated SaaS behavioral dataset containing:
- feature usage metrics
- error and support signals
- satisfaction indicators
- churn outcomes
- customer Behavior patterns
- retention indicators
- account information based on subscription data

The dataset is structured to resemble real-world SaaS telemetry rather than clean academic datasets.

## System Architecture

The system is structured into three major layers:

1. Analysis:
   Behavior analysis:  
   - Usage, satisfaction, support, and error patterns
   - Comparison of churned vs retained users
   Feature analysis: 
   - Feature health and risk scoring based on churn and retention signals
   - Risk score system(Signals considered:):
        high churned accounts 🟥 → rank high 
        high error count 🟥 → rank high 
        high ticket count 🟥 → rank high 
		high Usage duration 🟩 → rank low (positive metric)
        high satisfaction 🟩 → rank low (positive metric)
   - Risk score system(Signals considered:):
        high Retained accounts 🟩 → rank low (positive metric) 
        high error count 🟥 → rank high 
        high ticket count 🟥 → rank high 
        high Usage duration 🟩 → rank low (positive metric) 
        high satisfaction 🟩 → rank low (positive metric)  
   - Final feature ranking is derived from combined risk and health scores
   Industry analysis:
   - Analysis based on the churned accounts of every industry , based on the reasons and feedback given before churning.    
	
2. Product Breakdown
   - Feature Usage and churn relation
   - Identification of churn-driving and retention-anchor features
   - Final product insights giving insights that can be used as actionable instructions.

3. Churn Risk Prediction  
   - ML-based churn probability estimation made using the Analysis results. 
   - Risk segmentation (Low / Medium / High)
   - Explainable drivers behind each prediction

An interactive Streamlit dashboard ties these layers together.

## Key Insights

- Churn is rarely driven by a single factor; it emerges from combinations of low usage, declining satisfaction, and recurring friction.
- Some features act as retention anchors even when overall churn risk is high.
- High churn risk does not always require immediate action; some features warrant monitoring rather than intervention.
- Translating analytics into product actions is as important as prediction accuracy.

## Product Actions & Decision Framework

Instead of static insights, the system generates product recommendations based on:
- churn risk levels
- satisfaction benchmarks
- error and support signals
- dominant churn themes

Actions are categorized into:
- Stabilize & Fix
- Improve Onboarding & Discoverability
- Monitor & Maintain
- Pricing / Value Communication Review

## Dashboard Walkthrough

The Streamlit dashboard allows users to:
- explore churn and retention patterns
- diagnose feature-level health
- identify critical risk areas
- filter and prioritize high-risk accounts
- understand churn drivers through explainable outputs

## Limitations & Future Work

- The dataset is simulated and does not represent a single real SaaS product.
- Churn prediction models are context-dependent and require retraining per product.
- Future extensions could include:
  - time-based survival analysis
  - real-time churn monitoring
  - tighter integration with customer feedback NLP

## Conclusion

This project demonstrates how churn analytics can move beyond dashboards and predictions into structured product decision-making.

It reflects how analytics, product thinking, and explainability intersect in real SaaS environments.
