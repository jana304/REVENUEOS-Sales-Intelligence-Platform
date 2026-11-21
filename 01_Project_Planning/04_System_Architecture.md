# REVENUEOS — System Architecture

## 1. Architecture Overview

**Project:** SalesPulse AI — REVENUEOS  
**Primary Application:** Streamlit  
**Architecture Type:** Modular, Python-Based Sales Intelligence and Decision-Support System

REVENUEOS integrates historical sales analytics, machine learning, live sales data collection, interactive business intelligence reporting, and desktop automation.

The system consists of four main architectural layers:

1. Data Collection and Storage
2. Data Processing and Machine Learning
3. Application and Reporting
4. Sales Automation and Decision Support

## 2. High-Level System Architecture

```text
                  REVENUEOS PLATFORM

             HISTORICAL SALES DATA
                       |
                       v
             PYTHON DATA PROCESSING
                       |
              +--------+--------+
              |                 |
              v                 v
       SALES ANALYTICS     MACHINE LEARNING
              |                 |
              +--------+--------+
                       |
                       v
             STREAMLIT APPLICATION
                       |
                       v
           SALES DECISION INTELLIGENCE


                LIVE SALES PIPELINE

                  GOOGLE FORMS
                       |
                       v
                  GOOGLE SHEETS
                       |
              +--------+--------+
              |                 |
              v                 v
       STREAMLIT LIVE      PYTHON MASTER
       SALES OPERATIONS      AUTOMATION
                                |
                                v
                         POWER AUTOMATE
                            DESKTOP
                                |
                                v
                        CONSOLIDATED
                        RESULTS POPUP


              SUPPORTING REPORTING

                 SALES DATA
                     |
                     v
                LOOKER STUDIO
                     |
                     v
             INTERACTIVE REPORTS
```

The historical analytics workflow and live sales workflow operate as separate but complementary components of the platform.

## 3. Data Collection and Storage Layer

### 3.1 Historical Sales Data

Historical sales datasets provide the foundation for exploratory data analysis, predictive modeling, and revenue intelligence.

Data preparation includes:

- Data loading and inspection.
- Missing-value handling.
- Data cleaning and transformation.
- Feature preparation.
- Analytical dataset generation.

### 3.2 Live Sales Data Collection

Google Forms captures new sales opportunity records.

The submitted records are stored in the Google Sheets workbook:

**SalesPulse AI — Live Sales Database**

The workbook contains two relevant worksheets:

- `Live_Sales_Responses` — Original form response records.
- `Sales_Analytics` — Structured sales records consumed by Python.

The `Sales_Analytics` worksheet is formula-generated, so source records should be edited in `Live_Sales_Responses`.

## 4. Data Processing Layer

Python provides the core processing functionality.

Pandas is used to:

- Load structured datasets.
- Clean and transform sales records.
- Perform date calculations.
- Analyze sales opportunities.
- Prepare model inputs.
- Generate sales monitoring results.

NumPy supports numerical operations where required.

## 5. Machine Learning Layer

The machine learning component uses Scikit-learn to support predictive sales intelligence.

Its responsibilities include:

- Deal win probability estimation.
- Sales opportunity risk assessment.
- Revenue forecasting support.
- Predictive decision-support outputs.

Predictions provide analytical guidance rather than guaranteed business outcomes.

## 6. Application Layer

### 6.1 REVENUEOS Streamlit Application

The main application entry point is:

`Streamlit_App/app.py`

The application provides an interactive interface for exploring sales analytics and decision-support information.

Its functionality includes:

- Historical sales intelligence.
- Machine learning predictions.
- Revenue-related analytics.
- Sales opportunity analysis.
- Live sales operations.
- Interactive data exploration.

The application contains eight navigation pages.

### 6.2 Google Sheets Connection

The live data integration module is:

`Streamlit_App/google_sheets_connection.py`

This module provides the `load_live_sales_data()` function.

It retrieves Google Sheets records and makes them available as a Pandas DataFrame.

The same connection is reused by the master sales automation script.

## 7. Business Intelligence Reporting Layer

Looker Studio provides supporting interactive reporting.

Its role includes:

- Sales performance exploration.
- Opportunity-level reporting.
- Interactive filters.
- Detailed tables.
- Conditional formatting.
- Supporting charts and visualizations.

Looker Studio is a supplementary reporting component. The primary project deliverable remains the Streamlit application.

## 8. Sales Automation Layer

### 8.1 Master Automation Architecture

The Power Automate Desktop flow is named:

`SalesPulse_AI_Master_Automation`

The flow uses three actions:

1. **Run application:** Execute the Python master automation script.
2. **Read text from file:** Load the generated automation results.
3. **Display message:** Show the consolidated report.

### 8.2 Python Automation Script

The master automation script is:

`07_Power_Automate/master_sales_automation.py`

It retrieves live sales records and executes six monitoring checks.

| Automation | Detection Logic |
|---|---|
| New Opportunity | Identify opportunity IDs not previously processed |
| High Priority | Identify opportunities marked High and track newly detected high-priority IDs |
| Upcoming Follow-up | Find follow-up dates between today and the next three days |
| Overdue Follow-up | Find follow-up dates earlier than today |
| Customer Engagement | Identify low interactions, missing responses, or inactivity |
| Sales Summary | Calculate opportunity totals, pipeline value, and won-deal metrics |

### 8.3 Automation State Management

Automation tracking files are stored inside:

`07_Power_Automate/automation_state/`

Important files include:

- `master_automation_state.json` — Tracks processed opportunity IDs.
- `master_automation_results.txt` — Stores the consolidated report.

These files support repeated execution and reduce duplicate new-opportunity notifications.

The state directory contains local operational data and should not be published to GitHub.

### 8.4 Automation Execution Model

The current automation runs when manually launched through Power Automate Desktop.

It does not continuously monitor Google Sheets or automatically trigger immediately after Google Form submission.

## 9. End-to-End Data Flow

### Historical Sales Intelligence

1. Historical sales data is loaded into Python.
2. Data preparation and analysis are performed.
3. Machine learning components generate predictive outputs.
4. Streamlit displays the results.
5. Users explore analytics and decision-support information.

### Live Sales Operations

1. A user submits an opportunity through Google Forms.
2. Google Sheets stores the response.
3. The `Sales_Analytics` worksheet makes the structured record available.
4. Python retrieves the latest records.
5. Streamlit displays live sales information.

### Sales Automation

1. The user starts the master Power Automate Desktop flow.
2. Power Automate executes `master_sales_automation.py`.
3. Python retrieves current Google Sheets records.
4. Six automation checks are evaluated.
5. Python writes the consolidated report to a text file.
6. Power Automate reads the report.
7. A popup displays the automation results.

## 10. Security Architecture

The project uses Google service-account authentication for accessing Google Sheets.

Credentials are stored locally in:

`Streamlit_App/secrets/google_credentials.json`

Security requirements include:

- Do not commit service-account credentials to GitHub.
- Exclude secrets and local automation state files using `.gitignore`.
- Keep Python virtual environments outside version control.
- Avoid publishing private customer information.
- Use synthetic or appropriately anonymized demonstration records.

## 11. Error Handling and Reliability

The system includes basic reliability measures:

- Python exception handling for automation execution.
- Validation of required Google Sheets columns.
- Date conversion with invalid-value handling.
- Processed-opportunity tracking.
- Python exit codes for detecting execution failures.

The existing desktop flow displays the generated report after launching Python. A future improvement would be to add explicit Power Automate checks for nonzero Python exit codes before displaying results, preventing stale reports from being mistaken for successful runs.

## 12. Deployment Architecture

The current project runs locally.

**Development Environment:** Visual Studio Code  
**Application Runtime:** Python virtual environment  
**Web Application:** Streamlit  
**Live Data Storage:** Google Sheets  
**Reporting:** Looker Studio  
**Automation:** Power Automate Desktop

The application and desktop automation are separate interfaces that share the same live Google Sheets data source.

## 13. Architecture Limitations

- The system is designed primarily for demonstration and portfolio use.
- Desktop automation requires manual execution.
- Google Sheets availability depends on network connectivity and authentication.
- Machine learning results depend on training data quality.
- The current implementation does not provide enterprise-level authentication or centralized cloud orchestration.
- The daily sales summary currently describes the overall sales pipeline, rather than only records created on the execution date.

## 14. Future Architecture Enhancements

Potential enhancements include:

- Cloud-hosted Streamlit deployment.
- Secure cloud-based secrets management.
- Event-driven automation.
- CRM integrations.
- Scheduled monitoring and notifications.
- Centralized logging and monitoring.
- Model performance monitoring.
- Role-based access control.

