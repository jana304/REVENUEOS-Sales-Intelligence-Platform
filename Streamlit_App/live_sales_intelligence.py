
import pandas as pd


def analyze_followups(df):
    """Classify live sales opportunities by follow-up date."""

    result = df.copy()

    if "Next Follow-up Date" not in result.columns:
        result["Follow-up Status"] = "Date Missing"
        return result

    today = pd.Timestamp.today().normalize()

    followup_dates = pd.to_datetime(
        result["Next Follow-up Date"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    days_remaining = (followup_dates - today).dt.days

    result["Days Until Follow-up"] = days_remaining.astype("Int64")

    def classify_followup(days):
        if pd.isna(days):
            return "Date Missing"
        elif days < 0:
            return "Overdue"
        elif days == 0:
            return "Due Today"
        elif days <= 7:
            return "Upcoming"
        else:
            return "Scheduled Later"

    result["Follow-up Status"] = days_remaining.apply(
        classify_followup
    )

    return result

def analyze_customer_engagement(df):
    """Classify customer engagement using simple business rules."""

    result = df.copy()

    required_columns = [
        "Customer Interaction Count",
        "Customer Response Status"
    ]

    if not all(col in result.columns for col in required_columns):
        result["Engagement Status"] = "Data Missing"
        return result

    interactions = pd.to_numeric(
        result["Customer Interaction Count"],
        errors="coerce"
    )

    responses = (
        result["Customer Response Status"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    def classify_engagement(count, response):
        if pd.isna(count) or not response:
            return "Data Missing"

        if response in [
            "not interested",
            "no response",
            "unresponsive"
        ]:
            return "Needs Attention"

        if count < 2:
            return "Low Engagement"

        if count < 5:
            return "Active Engagement"

        return "Strong Engagement"

    result["Engagement Status"] = [
        classify_engagement(count, response)
        for count, response in zip(interactions, responses)
    ]

    return result
