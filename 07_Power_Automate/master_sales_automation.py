
from pathlib import Path
from datetime import datetime, timedelta
import json
import sys

import pandas as pd


# 1. PROJECT CONFIGURATION

PROJECT_DIR = Path(__file__).resolve().parent.parent
APP_DIR = PROJECT_DIR / "Streamlit_App"
AUTOMATION_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(APP_DIR))

from google_sheets_connection import load_live_sales_data

STATE_DIR = AUTOMATION_DIR / "automation_state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = STATE_DIR / "master_automation_results.txt"
STATE_FILE = STATE_DIR / "master_automation_state.json"

TODAY = datetime.now().date()


# 2. HELPER FUNCTIONS

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    return {
        "processed_opportunities": [],
        "processed_high_priority": []
    }


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=4)


def get_dates(df, column):
    return pd.to_datetime(
        df[column],
        errors="coerce"
    ).dt.date


def get_text_column(df, column):
    return (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )


# 3. NEW OPPORTUNITY ALERT

def check_new_opportunities(df, state):
    existing = set(
        state.get("processed_opportunities", [])
    )

    ids = (
        df["Opportunity ID"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    valid = ids.ne("")

    new_df = df[
        valid & ~ids.isin(existing)
    ].copy()

    state["processed_opportunities"] = sorted(
        existing | set(ids[valid])
    )

    return new_df


# 4. HIGH-PRIORITY SALES ALERT

def check_high_priority(df, state):
    priority = get_text_column(
        df, "Sales Priority"
    )

    high_df = df[
        priority == "high"
    ].copy()

    existing = set(
        state.get("processed_high_priority", [])
    )

    ids = (
        high_df["Opportunity ID"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    new_high = high_df[
        ids.ne("") & ~ids.isin(existing)
    ].copy()

    state["processed_high_priority"] = sorted(
        existing | set(ids[ids.ne("")])
    )

    return high_df, new_high


# 5. UPCOMING FOLLOW-UP REMINDER

def check_upcoming_followups(df):
    dates = get_dates(
        df, "Next Follow-up Date"
    )

    upcoming = df[
        dates.apply(
            lambda value:
                pd.notna(value)
                and TODAY <= value <= TODAY + timedelta(days=3)
        )
    ].copy()

    return upcoming


# 6. OVERDUE FOLLOW-UP ALERT

def check_overdue_followups(df):
    dates = get_dates(
        df, "Next Follow-up Date"
    )

    overdue = df[
        dates.apply(
            lambda value:
                pd.notna(value)
                and value < TODAY
        )
    ].copy()

    return overdue


# 7. CUSTOMER ENGAGEMENT ALERT

def check_customer_engagement(df):
    interactions = pd.to_numeric(
        df["Customer Interaction Count"],
        errors="coerce"
    ).fillna(0)

    response = get_text_column(
        df, "Customer Response Status"
    )

    last_activity = get_dates(
        df, "Last Activity Date"
    )

    inactive = last_activity.apply(
        lambda value:
            pd.notna(value)
            and value < TODAY - timedelta(days=7)
    )

    low_interactions = interactions <= 1

    no_response = response.isin([
        "no response",
        "not responded",
        "unresponsive",
        "pending"
    ])

    engagement_df = df[
        inactive | low_interactions | no_response
    ].copy()

    return engagement_df


# 8. DAILY SALES SUMMARY

def generate_daily_summary(df):
    values = pd.to_numeric(
        df["Deal Value"],
        errors="coerce"
    ).fillna(0)

    stages = get_text_column(
        df, "Deal Stage"
    )

    total_opportunities = len(df)
    total_pipeline_value = values.sum()

    won_mask = stages.isin([
        "won",
        "closed won",
        "closed-won"
    ])

    won_deals = int(won_mask.sum())
    won_value = values[won_mask].sum()

    return {
        "total_opportunities": total_opportunities,
        "total_pipeline_value": total_pipeline_value,
        "won_deals": won_deals,
        "won_value": won_value
    }


# 9. MASTER AUTOMATION EXECUTION

def main():
    print("REVENUEOS - MASTER SALES AUTOMATION")

    df = load_live_sales_data()

    if df is None:
        raise ValueError(
            "Google Sheets returned no dataset."
        )

    required_columns = [
        "Opportunity ID",
        "Sales Priority",
        "Next Follow-up Date",
        "Customer Interaction Count",
        "Customer Response Status",
        "Last Activity Date",
        "Deal Value",
        "Deal Stage"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing Google Sheets columns: "
            + ", ".join(missing)
        )

    print("Google Sheets connection: SUCCESS")
    print("Total opportunities:", len(df))

    state = load_state()

    # Execute all six automation checks

    new_opportunities = check_new_opportunities(
        df, state
    )

    high_priority, new_high_priority = (
        check_high_priority(df, state)
    )

    upcoming = check_upcoming_followups(df)

    overdue = check_overdue_followups(df)

    engagement = check_customer_engagement(df)

    summary = generate_daily_summary(df)

    # 10. CLEAN POPUP REPORT DESIGN

    report = [
        "REVENUEOS",
        "Sales Automation Control Center",
        "",
        f"Executed: {datetime.now():%d %b %Y, %I:%M %p}",
        "Status: Completed Successfully",
        "",
        "01  NEW OPPORTUNITIES",
        f"    New Alerts: {len(new_opportunities)}",
        "",
        "02  HIGH PRIORITY SALES",
        f"    New Alerts: {len(new_high_priority)}",
        f"    Total High Priority: {len(high_priority)}",
        "",
        "03  UPCOMING FOLLOW-UPS",
        f"    Due Within 3 Days: {len(upcoming)}",
        "",
        "04  OVERDUE FOLLOW-UPS",
        f"    Overdue: {len(overdue)}",
        "",
        "05  CUSTOMER ENGAGEMENT",
        f"    Requires Attention: {len(engagement)}",
        "",
        "06  DAILY SALES SUMMARY",
        f"    Total Opportunities: {summary['total_opportunities']}",
        f"    Total Pipeline Value: {summary['total_pipeline_value']:,.2f}",
        f"    Won Deals: {summary['won_deals']}",
        f"    Won Deal Value: {summary['won_value']:,.2f}",
        "",
        "All 6 automation checks completed."
    ]

    report_text = "\n".join(report)

    # Save report for Power Automate Desktop

    OUTPUT_FILE.write_text(
        report_text,
        encoding="utf-8"
    )

    # Save processed opportunity IDs

    save_state(state)

    print(report_text)

    print(
        "\nMASTER AUTOMATION COMPLETED SUCCESSFULLY"
    )

    print("Results saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        print("MASTER AUTOMATION ERROR:", error)
        sys.exit(1)
