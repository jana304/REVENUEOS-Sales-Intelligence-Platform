# REVENUEOS — Technology Stack

## 1. Project Overview

**Project Name:** SalesPulse AI — REVENUEOS

**Project Title:** REVENUEOS — Sales Intelligence & Decision Platform

**Project Category:** Data Analytics, Machine Learning, Business Intelligence, and Sales Automation

**Primary Application:** Python Streamlit

REVENUEOS combines multiple technologies to deliver an integrated sales analytics and decision-support platform.

## 2. Technology Stack Summary

| Category | Technology | Purpose |
|---|---|---|
| Programming Language | Python | Core application and analytics development |
| Data Manipulation | Pandas | Data cleaning, transformation, and analysis |
| Numerical Computing | NumPy | Numerical operations and calculations |
| Machine Learning | Scikit-learn | Predictive modeling and deal analysis |
| Application Framework | Streamlit | Interactive REVENUEOS web application |
| Data Collection | Google Forms | Capture new sales opportunities |
| Live Data Storage | Google Sheets | Maintain sales opportunity records |
| Google Sheets Integration | Google APIs and service-account authentication | Retrieve live sales data |
| Business Intelligence | Looker Studio | Interactive reporting and data exploration |
| Desktop Automation | Power Automate Desktop | Execute and display automation results |
| Development Environment | Visual Studio Code | Code development and debugging |
| Version Control | Git | Track source code changes |
| Code Hosting | GitHub | Portfolio repository and documentation |
| Project Documentation | Markdown | Technical and project documentation |

## 3. Python

Python is the primary programming language used throughout REVENUEOS.

Its responsibilities include:

- Loading and processing sales datasets.
- Performing exploratory data analysis.
- Preparing machine learning features.
- Generating predictions and decision-support outputs.
- Connecting to Google Sheets.
- Executing sales monitoring rules.
- Producing automation reports.

Python also provides the backend logic for the Streamlit application.

## 4. Pandas and NumPy

### Pandas

Pandas supports:

- Data loading and inspection.
- Missing-value handling.
- Data transformation.
- Sales performance calculations.
- Date-based follow-up monitoring.
- Customer engagement analysis.
- Preparation of machine learning datasets.

### NumPy

NumPy supports numerical calculations and array-based operations used in analytics and machine learning workflows.

## 5. Scikit-learn

Scikit-learn provides the machine learning capabilities used in the project.

The machine learning component focuses on:

- Deal win probability prediction.
- Sales opportunity risk assessment.
- Model training and evaluation.
- Supporting revenue forecasting.

Model outputs are intended to support sales decisions rather than guarantee business outcomes.

## 6. Streamlit

Streamlit is used to build the primary REVENUEOS application.

The application provides:

- Interactive sales analytics.
- Multiple navigation pages.
- Data tables and visualizations.
- Machine learning prediction results.
- Sales decision-support features.
- Live sales operations using Google Sheets.

Streamlit allows Python-based analytical functionality to be presented through a browser interface.

## 7. Google Forms

Google Forms is used to capture sales opportunity information.

The form collects details such as:

- Opportunity ID.
- Sales Agent.
- Customer Account.
- Product.
- Deal Stage.
- Deal Value.
- Regional Office.
- Engagement and follow-up dates.
- Customer interaction details.
- Sales Priority.
- Sales Notes.

Submitted records are stored in a connected Google Sheets workbook.

## 8. Google Sheets

Google Sheets acts as the live sales data source.

**Workbook:** SalesPulse AI — Live Sales Database

**Worksheets:**

- `Live_Sales_Responses` — Source records collected through Google Forms.
- `Sales_Analytics` — Structured sales data used for analysis and automation.

The Python application accesses the `Sales_Analytics` worksheet through the existing Google Sheets connection.

## 9. Google Sheets API Integration

The project uses a Python connection module:

`Streamlit_App/google_sheets_connection.py`

Its responsibilities include:

- Authenticating with Google services.
- Retrieving live sales records.
- Converting retrieved data into a Pandas DataFrame.
- Providing data to the Streamlit application and automation scripts.

Service-account credentials are stored separately from public source code.

**Security requirement:** Never commit Google service-account JSON files, private keys, or other credentials to GitHub.

## 10. Looker Studio

Looker Studio is used for supporting business intelligence reports.

Its reporting capabilities include:

- Interactive sales tables.
- Filtering and data exploration.
- Conditional formatting.
- Sales performance visualizations.
- Opportunity-level analysis.

Looker Studio complements the Streamlit application but does not replace it as the project's primary output.

## 11. Power Automate Desktop

Power Automate Desktop provides the desktop automation interface.

**Master Flow:** `SalesPulse_AI_Master_Automation`

The master flow uses three primary actions:

1. Run application — Execute the Python automation script.
2. Read text from file — Retrieve the generated automation report.
3. Display message — Present the results in one popup.

The Python script executes six checks:

| Check | Function |
|---|---|
| New Opportunity | Detect previously unseen opportunity IDs |
| High Priority | Identify high-priority sales opportunities |
| Upcoming Follow-up | Find follow-ups due within three days |
| Overdue Follow-up | Identify past-due follow-up dates |
| Customer Engagement | Identify opportunities requiring attention |
| Sales Summary | Summarize opportunity counts and pipeline values |

The current implementation runs when the user manually starts the desktop flow. It is not an automatically triggered cloud workflow.

## 12. Visual Studio Code

Visual Studio Code is the primary development environment.

It is used for:

- Writing Python scripts.
- Managing project folders.
- Running terminal commands.
- Debugging application errors.
- Editing Markdown documentation.
- Preparing source code for GitHub.

A Python virtual environment (`.venv`) is used to isolate project dependencies.

## 13. Git and GitHub

Git is used for source code version control.

GitHub is intended to host the completed project as a portfolio repository.

The repository should contain:

- Project source code.
- Dependency requirements.
- Setup instructions.
- Architecture documentation.
- Screenshots and demonstration materials.
- Testing documentation.

The repository must exclude:

- Virtual environments.
- Google service-account credentials.
- Private API keys.
- Local automation state files.
- Sensitive logs and configuration values.

## 14. Technology Integration Architecture

The project uses two main data workflows.

### Historical Sales Intelligence

Historical Sales Data → Python Data Processing → Machine Learning and Analytics → REVENUEOS Streamlit Application

### Live Sales Operations

Google Forms → Google Sheets → Python Google Sheets Connection → REVENUEOS Live Sales Operations

The automation workflow operates alongside the application:

Google Sheets → Python Master Automation → Power Automate Desktop → Consolidated Results Popup

Looker Studio provides an additional interactive reporting layer.

## 15. Technology Selection Rationale

| Technology | Reason for Selection |
|---|---|
| Python | Flexible language for analytics, ML, and automation |
| Pandas | Efficient tabular data processing |
| Scikit-learn | Accessible machine learning development |
| Streamlit | Rapid development of interactive Python applications |
| Google Forms | Simple sales data collection |
| Google Sheets | Accessible cloud-based data storage |
| Looker Studio | Interactive business reporting |
| Power Automate Desktop | Desktop workflow orchestration |
| VS Code | Integrated development and debugging |
| GitHub | Source code sharing and portfolio presentation |
