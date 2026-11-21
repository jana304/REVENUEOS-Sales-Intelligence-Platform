# REVENUEOS — Project Workflow

## 1. Project Overview

**Project Name:** SalesPulse AI — REVENUEOS

**Project Title:** REVENUEOS — Sales Intelligence & Decision Platform

**Project Category:** End-to-End Data Analytics, Machine Learning, Business Intelligence, and Sales Automation

**Primary Output:** Python Streamlit Application

REVENUEOS follows an end-to-end workflow that combines historical sales analysis, predictive intelligence, live opportunity monitoring, interactive reporting, and desktop automation.

The project is organized into five major workflows:

1. Historical Sales Data Analytics
2. Machine Learning and Decision Intelligence
3. Streamlit Application Development
4. Live Sales Data and Business Intelligence Reporting
5. Sales Automation and Monitoring

## 2. Overall Project Workflow

```text
                 REVENUEOS
       Sales Intelligence Platform
                    |
         Historical Sales Data
                    |
                    v
          Data Cleaning and EDA
                    |
                    v
           Machine Learning
                    |
                    v
        Sales Decision Intelligence
                    |
                    v
        REVENUEOS Streamlit App
                    |
                    v
         Interactive User Interface


            LIVE SALES WORKFLOW

               Google Forms
                    |
                    v
               Google Sheets
                    |
           +--------+--------+
           |                 |
           v                 v
    Streamlit Live       Python Master
    Sales Operations      Automation
                             |
                             v
                     Power Automate
                         Desktop
                             |
                             v
                      Results Popup


         SUPPORTING REPORTING

             Sales Data
                 |
                 v
            Looker Studio
                 |
                 v
          Interactive Reports
```

## 3. Phase 1 — Historical Data Collection

### Objective

Prepare historical sales data for analysis and predictive modeling.

### Activities

1. Collect or prepare the historical sales dataset.
2. Inspect the dataset structure and available columns.
3. Identify missing values and inconsistent records.
4. Validate important sales-related fields.
5. Organize raw and processed datasets into appropriate project folders.

### Expected Output

A structured historical sales dataset ready for exploratory analysis and machine learning.

## 4. Phase 2 — Data Cleaning and Preparation

### Objective

Improve data quality and prepare datasets for analysis.

### Activities

1. Load the dataset using Pandas.
2. Check data types and missing values.
3. Handle duplicate or invalid records where appropriate.
4. Standardize relevant sales fields.
5. Prepare numerical and categorical features.
6. Save cleaned datasets for downstream processing.

### Expected Output

A cleaned dataset suitable for analytical and predictive workflows.

## 5. Phase 3 — Exploratory Data Analysis

### Objective

Understand sales patterns, opportunity characteristics, and revenue-related trends.

### Activities

1. Analyze sales opportunity distributions.
2. Explore deal stages and pipeline values.
3. Examine sales performance patterns.
4. Identify potential business risks.
5. Generate charts and analytical summaries.
6. Document important findings.

### Expected Output

EDA results, supporting visualizations, and sales insights.

## 6. Phase 4 — Machine Learning

### Objective

Generate predictive insights that support sales decision-making.

### Activities

1. Select relevant features and target variables.
2. Prepare training and testing datasets.
3. Train machine learning models using Scikit-learn.
4. Evaluate model performance.
5. Generate deal win probability predictions.
6. Support sales risk assessment and revenue forecasting.
7. Save required models and prediction outputs.

### Expected Output

Machine learning models, evaluation results, and predictive sales intelligence.

### Important Consideration

Machine learning predictions represent estimates based on available data. They do not guarantee sales outcomes.

## 7. Phase 5 — Sales Decision Intelligence

### Objective

Convert analytical and predictive outputs into actionable sales information.

### Activities

1. Identify opportunities with elevated risk.
2. Evaluate predicted deal win probabilities.
3. Support revenue forecasting.
4. Generate rule-based sales recommendations.
5. Prepare decision-support results for the application.

### Expected Output

Sales intelligence outputs that help users prioritize opportunities and understand potential risks.

## 8. Phase 6 — Streamlit Application Development

### Objective

Build the primary REVENUEOS user interface.

### Application Entry Point

`Streamlit_App/app.py`

### Activities

1. Configure the Streamlit application.
2. Develop the navigation structure.
3. Integrate historical analytics.
4. Display machine learning prediction results.
5. Present sales decision-support information.
6. Integrate live sales operations.
7. Add interactive tables, charts, and filters.
8. Validate the application interface.

### Expected Output

A working eight-page REVENUEOS Streamlit application.

### Application Execution

From the project root directory:

```powershell
.\Streamlit_App\.venv\Scripts\python.exe -m streamlit run .\Streamlit_App\app.py
```

The application opens in a browser using the local Streamlit server.

## 9. Phase 7 — Live Sales Data Collection

### Objective

Capture and monitor new sales opportunities.

### Technologies

- Google Forms
- Google Sheets
- Python
- Pandas

### Workflow

1. A user submits an opportunity through Google Forms.
2. The response is saved in `Live_Sales_Responses`.
3. The `Sales_Analytics` worksheet provides structured sales records.
4. Python retrieves the records using the Google Sheets connection.
5. Streamlit displays the live sales information.

### Google Sheets Connection

`Streamlit_App/google_sheets_connection.py`

The module provides the `load_live_sales_data()` function used by the application and automation scripts.

### Expected Output

An operational live sales data pipeline connecting Google Forms, Google Sheets, and REVENUEOS.

## 10. Phase 8 — Looker Studio Reporting

### Objective

Provide supplementary interactive business intelligence reporting.

### Activities

1. Connect relevant sales data to Looker Studio.
2. Prepare interactive report pages.
3. Add detailed sales tables.
4. Configure filters and conditional formatting.
5. Include supporting charts where useful.
6. Validate report interactions.

### Expected Output

Interactive Looker Studio reports that complement the primary Streamlit application.

## 11. Phase 9 — Sales Automation

### Objective

Automate the evaluation of six sales monitoring conditions through one desktop workflow.

### Master Python Script

`07_Power_Automate/master_sales_automation.py`

### Power Automate Desktop Flow

`SalesPulse_AI_Master_Automation`

### Automation Checks

| No. | Automation | Workflow |
|---|---|---|
| 1 | New Opportunity | Compare opportunity IDs against processed records |
| 2 | High Priority | Identify High-priority opportunities and newly detected High-priority IDs |
| 3 | Upcoming Follow-up | Identify follow-ups due within the next three days |
| 4 | Overdue Follow-up | Identify follow-up dates earlier than the current date |
| 5 | Customer Engagement | Identify low interaction, no response, or inactivity |
| 6 | Sales Summary | Generate opportunity counts, pipeline value, and won-deal totals |

### Automation Execution Workflow

1. Open Power Automate Desktop.
2. Open `SalesPulse_AI_Master_Automation`.
3. Click Run.
4. Power Automate launches the master Python script.
5. Python loads live sales data from Google Sheets.
6. All six automation checks execute.
7. Python generates the consolidated report.
8. Power Automate reads the report file.
9. The results appear in one popup.

### Automation Output Files

`07_Power_Automate/automation_state/master_automation_results.txt`

`07_Power_Automate/automation_state/master_automation_state.json`

The results file stores the latest consolidated report.

The state file tracks processed opportunity IDs to reduce duplicate alerts.

### Execution Limitation

The current automation runs when manually started in Power Automate Desktop. It is not an automatically triggered cloud flow.

## 12. Phase 10 — Integration Testing

### Objective

Verify that the individual project components work together.

### Testing Activities

- Confirm that the Streamlit application launches.
- Validate navigation and application pages.
- Verify historical analytics and prediction outputs.
- Test Google Sheets connectivity.
- Confirm live sales records appear correctly.
- Run the master Power Automate Desktop flow.
- Verify all six automation sections appear.
- Test overdue follow-up detection.
- Test customer engagement detection.
- Verify high-priority monitoring.
- Check that automation state tracking prevents repeated new-opportunity alerts.

### Expected Output

A documented set of integration test results and supporting screenshots.

## 13. Phase 11 — Project Documentation

### Objective

Prepare clear technical and portfolio documentation.

### Documentation Includes

- Project overview.
- Project scope.
- Technology stack.
- System architecture.
- Project workflow.
- Setup and execution instructions.
- Testing evidence.
- Project screenshots.
- GitHub README.

### Expected Output

A documented project that can be understood and demonstrated by other developers, recruiters, and reviewers.

## 14. Phase 12 — GitHub Preparation

### Objective

Prepare a secure, organized portfolio repository.

### Activities

1. Review the final project folder structure.
2. Remove unnecessary temporary files.
3. Create or verify `.gitignore`.
4. Exclude virtual environments and local state files.
5. Exclude Google service-account credentials.
6. Prepare dependency requirements.
7. Create a professional README.
8. Add relevant project screenshots.
9. Review the files before publishing.
10. Upload the repository to GitHub.

### Security Requirements

Do not upload:

- Google service-account JSON credentials.
- Private keys.
- API secrets.
- Local virtual environments.
- Private customer records.
- Sensitive automation state files.

## 15. Final Project Deliverables

The intended final deliverables are:

1. Historical sales analytics outputs.
2. Machine learning models and prediction results.
3. REVENUEOS Streamlit application.
4. Google Forms and Google Sheets integration.
5. Looker Studio interactive reports.
6. Power Automate Desktop master automation.
7. Integration testing evidence.
8. Project planning and technical documentation.
9. GitHub repository.
10. Portfolio presentation materials.

## 16. Project Completion Criteria

REVENUEOS will be considered ready for final portfolio delivery when:

- The application runs successfully.
- Core analytical features are validated.
- Machine learning outputs are accessible.
- Live sales data integration works.
- The six automation checks execute successfully.
- The master automation popup displays the expected results.
- Test records are restored after validation.
- Documentation is complete.
- Sensitive files are excluded from the repository.
- The project is ready for demonstration.
