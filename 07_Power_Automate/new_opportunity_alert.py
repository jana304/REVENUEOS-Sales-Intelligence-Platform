
from pathlib import Path
import json
import sys

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
APP_DIR = PROJECT_DIR / "Streamlit_App"

sys.path.insert(0, str(APP_DIR))

from google_sheets_connection import load_live_sales_data

# Automation state folder
STATE_DIR = Path(__file__).resolve().parent / "automation_state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = STATE_DIR / "processed_opportunities.json"
ALERT_FILE = STATE_DIR / "new_opportunity_alert.txt"


def check_new_opportunities():

    # Reset alert status for every run
    ALERT_FILE.write_text(
        "NO_NEW_OPPORTUNITY",
        encoding="utf-8"
    )

    # Load live Google Sheets data
    df = load_live_sales_data()

    if "Opportunity ID" not in df.columns:
        print("ERROR: Opportunity ID column not found.")
        return

    # Get current opportunity IDs
    current_ids = set(
        df["Opportunity ID"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    current_ids.discard("")

    # First execution: create baseline
    if not STATE_FILE.exists():

        STATE_FILE.write_text(
            json.dumps(sorted(current_ids), indent=2),
            encoding="utf-8"
        )

        print("BASELINE CREATED")
        print("Existing opportunities:", len(current_ids))
        return

    # Load previously processed IDs
    processed_ids = set(
        json.loads(
            STATE_FILE.read_text(encoding="utf-8")
        )
    )

    # Identify new opportunities
    new_ids = current_ids - processed_ids

    if not new_ids:
        print("NO NEW OPPORTUNITIES")
        return

    # New opportunities detected
    print("NEW SALES OPPORTUNITIES DETECTED")
    print("Total new opportunities:", len(new_ids))

    for opportunity_id in sorted(new_ids):

        record = df[
            df["Opportunity ID"]
            .astype(str)
            .str.strip() == opportunity_id
        ].iloc[0]

        print("-" * 40)
        print("NEW SALES OPPORTUNITY DETECTED")
        print("Opportunity ID:", opportunity_id)
        print("Sales Agent:", record.get("Sales Agent", "Unknown"))
        print("Customer:", record.get("Customer Account", "Unknown"))
        print("Deal Value:", record.get("Deal Value", 0))
        print("Priority:", record.get("Sales Priority", "Unknown"))

    # Save processed opportunities
    STATE_FILE.write_text(
        json.dumps(
            sorted(current_ids | processed_ids),
            indent=2
        ),
        encoding="utf-8"
    )

    # Create alert signal after saving processed IDs
    ALERT_FILE.write_text(
        "NEW_OPPORTUNITY",
        encoding="utf-8"
    )

    print("-" * 40)
    print("ALERT STATUS: NEW_OPPORTUNITY")


if __name__ == "__main__":
    try:
        check_new_opportunities()
    except Exception as error:
        print("AUTOMATION ERROR:", error)
        sys.exit(1)
