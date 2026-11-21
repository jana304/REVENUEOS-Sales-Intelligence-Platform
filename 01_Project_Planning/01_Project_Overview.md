# REVENUEOS — Sales Intelligence & Decision Platform

## 1. Project Introduction

**REVENUEOS** is a Python-based Sales Intelligence and Decision Support Platform developed as part of the **SalesPulse AI** project.

The platform integrates data analytics, machine learning, interactive reporting, live sales data integration, and desktop automation to help businesses monitor sales performance, identify revenue opportunities, assess deal risks, and support data-driven sales decisions.

The primary output is an interactive **Streamlit web application**, supported by Google Forms, Google Sheets, Looker Studio, and Power Automate Desktop.

## 2. Problem Statement

Sales teams often face challenges such as:

- Difficulty tracking sales opportunities across multiple stages.
- Limited visibility into high-risk deals and potential revenue.
- Delayed follow-ups and inconsistent customer engagement.
- Manual monitoring of sales activities.
- Lack of centralized, actionable sales intelligence.

These challenges can reduce operational efficiency and make sales decision-making more difficult.

REVENUEOS aims to address these problems through an integrated analytics and decision-support platform.

## 3. Project Objectives

The main objectives are to:

1. Analyze historical sales data and identify important business patterns.
2. Use machine learning to estimate deal win probabilities and support risk assessment.
3. Generate revenue forecasts and data-driven sales recommendations.
4. Provide an interactive Streamlit application for exploring sales intelligence.
5. Capture sales opportunity data using Google Forms and Google Sheets.
6. Provide supporting interactive reports using Looker Studio.
7. Automate six sales monitoring checks using Python and Power Automate Desktop.
8. Maintain automation results and processed-opportunity tracking.

## 4. Key Project Components

### Data Analytics

Python and Pandas are used for data preparation, exploratory data analysis, and sales performance analysis.

### Machine Learning

Machine learning supports deal win probability prediction, risk identification, and revenue forecasting.

### REVENUEOS Streamlit Application

The Streamlit application provides the primary interface for accessing sales intelligence, analytics, and decision-support features.

### Live Sales Data Integration

Google Forms captures sales opportunities, while Google Sheets stores and organizes the submitted records.

### Looker Studio Reporting

Interactive reports provide additional sales data exploration using filters, tables, and visualizations.

### Sales Automation

One Power Automate Desktop master flow executes a Python script that performs six checks:

1. New Opportunity Detection
2. High-Priority Sales Detection
3. Upcoming Follow-up Monitoring
4. Overdue Follow-up Monitoring
5. Customer Engagement Monitoring
6. Sales Pipeline Summary Generation

The desktop automation is manually initiated in the current implementation.

## 5. Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Application Development | Streamlit |
| Live Data Collection | Google Forms |
| Data Storage | Google Sheets |
| Interactive Reporting | Looker Studio |
| Desktop Automation | Power Automate Desktop |
| Development Environment | VS Code |
| Version Control | Git, GitHub |

## 6. Expected Business Benefits

REVENUEOS is designed to support:

- Improved visibility into sales opportunities.
- Earlier identification of potentially risky deals.
- More consistent sales follow-up monitoring.
- Better understanding of customer engagement.
- Data-driven revenue planning.
- Reduced manual effort when reviewing sales conditions.
- Centralized access to sales intelligence.

These are intended benefits of the platform, not independently measured business outcomes.

## 7. Project Deliverables

The project deliverables include:

- Historical sales analysis and supporting outputs.
- Machine learning models and prediction results.
- REVENUEOS Streamlit application.
- Google Forms and Google Sheets integration.
- Looker Studio interactive reports.
- Power Automate Desktop master automation.
- Automation test results.
- Project documentation.
- GitHub portfolio repository.

## 8. Project Limitations

- The current desktop automation runs when manually started; it is not an always-on Google Forms trigger.
- Forecasts and predictions depend on the quality and representativeness of the underlying data.
- Google Sheets integration requires valid credentials and network connectivity.
- The current automation uses rule-based checks rather than autonomous AI decision-making.
- Historical or synthetic demonstration data should not be presented as verified real-world business performance.

