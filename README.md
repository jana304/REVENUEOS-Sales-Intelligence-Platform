# REVENUEOS — Sales Intelligence & Decision Platform

### Sales Analytics, Machine Learning, Revenue Forecasting & Automated Decision Intelligence

REVENUEOS is an end-to-end sales analytics project that combines historical sales analysis, machine learning, live opportunity tracking, interactive reporting, and desktop automation to support data-driven sales decisions.

The project integrates **Python, Scikit-learn, Streamlit, Google Forms, Google Sheets, Looker Studio, and Power Automate Desktop** into a unified sales intelligence platform.

**Project Status:** Python | Machine Learning | Streamlit | Looker Studio | Power Automate

---

## 🎯 Project Overview

REVENUEOS helps analyze sales performance, predict deal outcomes, identify potential risks, and monitor sales opportunities through an interactive decision-support application.

### Key Features

- **Sales Analytics:** Analyze historical sales performance, pipeline values, and deal stages.
- **Win Probability Prediction:** Estimate deal success probabilities using machine learning.
- **Deal Risk Intelligence:** Identify opportunities requiring attention.
- **Revenue Forecasting:** Support revenue planning through predictive insights.
- **Sales Recommendations:** Generate rule-based decision-support recommendations.
- **Streamlit Application:** Eight-page interactive sales intelligence platform.
- **Live Sales Tracking:** Capture opportunities through Google Forms and Google Sheets.
- **Customer Engagement:** Monitor low-interaction and inactive opportunities.
- **Follow-up Monitoring:** Identify upcoming and overdue follow-ups.
- **Looker Studio:** Interactive sales reports, filters, and detailed tables.
- **Power Automate:** Execute six monitoring checks through one desktop workflow.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Application | Streamlit |
| Data Collection | Google Forms |
| Live Database | Google Sheets |
| Data Integration | Google Sheets API |
| Business Intelligence | Looker Studio |
| Automation | Power Automate Desktop |
| Development | VS Code, Git, GitHub |

## 📊 Dataset

REVENUEOS uses historical sales datasets for analytics and machine learning.

| Dataset | Records |
|---|---:|
| sales_pipeline.csv | 8,800 |
| accounts.csv | 85 |
| products.csv | 7 |
| sales_teams.csv | 35 |
| data_dictionary.csv | 21 |
| master_sales_cleaned.csv | 8,800 |

The cleaned dataset supports analytical and predictive workflows.

Live sales opportunities are collected separately through Google Forms and stored in Google Sheets.

## 🧠 Machine Learning & Decision Intelligence

The machine learning component supports:

- Deal win probability estimation.
- Sales opportunity risk assessment.
- Revenue forecasting.
- Sales prioritization.
- Rule-based recommendations.

Predictions are estimates based on available data and do not guarantee future sales outcomes.

## 💻 Streamlit Application

**Main Application:** `Streamlit_App/app.py`

The eight-page REVENUEOS application provides interactive sales analytics, predictive intelligence, opportunity analysis, and live sales monitoring.

It combines historical analysis and live sales information in one interface.

## 📋 Live Sales Tracking

**Google Form:** Sales Opportunity Tracker

**Google Sheets Workbook:** SalesPulse AI — Live Sales Database

| Worksheet | Purpose |
|---|---|
| Live_Sales_Responses | Original form submissions |
| Sales_Analytics | Structured sales records |

**Workflow:**

Google Forms → Google Sheets → Python → Streamlit

The application retrieves live data using `google_sheets_connection.py`.

A static Excel backup is available in `02_Dataset/Live_Sales_Data/`.

## 📈 Looker Studio Reporting

Looker Studio provides supporting interactive reports featuring:

- Sales opportunity tables.
- Interactive filters.
- Conditional formatting.
- Sales performance analysis.
- Supporting visualizations.

**Saved PDF:** `05_Looker_Studio/REVENUEOS_Looker_Studio_Report.pdf`

The original interactive reports remain hosted online.

## ⚙️ Power Automate — Sales Automation

**Master Flow:** `SalesPulse_AI_Master_Automation`

**Python Script:** `07_Power_Automate/master_sales_automation.py`

### Six Automation Checks

| Automation | Purpose |
|---|---|
| New Opportunity | Detect newly recorded opportunities |
| High Priority | Identify high-priority opportunities |
| Upcoming Follow-up | Detect follow-ups due within three days |
| Overdue Follow-up | Identify missed follow-ups |
| Customer Engagement | Detect low engagement or inactivity |
| Sales Summary | Summarize pipeline value and opportunity counts |

**Workflow:**

Google Sheets → Python Automation → Power Automate Desktop → Results Popup

The desktop flow is manually executed and displays all six results in one consolidated popup.

## 🔄 System Architecture

```text
Historical Sales Data
        |
        v
Python Data Processing
        |
        v
Machine Learning & Analytics
        |
        v
REVENUEOS Streamlit Application

Google Forms
        |
        v
Google Sheets
        |
        +----> Streamlit Live Sales
        |
        +----> Python Master Automation
                        |
                        v
                Power Automate Desktop
                        |
                        v
                 Results Popup

Sales Data ---> Looker Studio Reports
```

## 📁 Project Structure

```text
SALESPULSE_AI/
├── 01_Project_Planning/
├── 02_Dataset/
│   ├── Raw_Data/
│   ├── Cleaned_Data/
│   └── Live_Sales_Data/
├── 03_Python_Analysis/
├── 04_Machine_Learning/
├── 05_Looker_Studio/
├── 06_Sales_Tracking/
├── 07_Power_Automate/
├── 08_Testing_Documentation/
├── Streamlit_App/
│   ├── app.py
│   ├── google_sheets_connection.py
│   └── live_sales_intelligence.py
├── .gitignore
└── README.md
```

## ▶️ Getting Started

### Prerequisites

Python, Git, Streamlit, required Python libraries, and Google Sheets credentials for live features.

### 1. Clone Repository

```bash
git clone https://github.com/jana304/SALESPULSE_AI.git
cd SALESPULSE_AI
```

*Replace the repository URL if the final GitHub repository name differs.*

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The requirements file must be generated before using this command.

### 4. Run Streamlit

```bash
python -m streamlit run Streamlit_App/app.py
```

Configure authorized Google Sheets credentials locally to enable live data functionality.

## 🎯 Project Objectives

- Analyze historical sales performance.
- Predict deal outcomes and identify sales risks.
- Support revenue forecasting and prioritization.
- Build an interactive sales intelligence application.
- Integrate live opportunity tracking.
- Provide business intelligence reporting.
- Automate repetitive sales monitoring tasks.

## 🔐 Data Security

- Exclude Google service-account credentials.
- Protect private customer information.
- Exclude virtual environments and automation state files.
- Use synthetic or anonymized data for public demonstrations.
- Treat predictions and risk scores as estimates.

## 🚀 Future Enhancements

- Cloud deployment.
- Scheduled sales monitoring.
- CRM integration.
- Automated notifications.
- Advanced forecasting.
- Generative AI sales assistance.

## 👨‍💻 Project Information

**Project:** REVENUEOS — Sales Intelligence & Decision Platform

**Domain:** Sales Analytics & Revenue Intelligence

**Programming:** Python

**Machine Learning:** Scikit-learn

**Application:** Streamlit

**Business Intelligence:** Looker Studio

**Automation:** Power Automate Desktop

**Author:** Jana M.

**Year:** 2026

## ⚠️ Disclaimer

REVENUEOS is an educational and portfolio project. Predictions, forecasts, and risk indicators are estimates and do not guarantee business outcomes.

---

**Built with Python, Machine Learning, Streamlit, Google Sheets, Looker Studio, and Power Automate Desktop.**