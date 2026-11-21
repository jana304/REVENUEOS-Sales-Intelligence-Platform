
from pathlib import Path

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

BASE_DIR = Path(__file__).resolve().parent

KEY_FILE = BASE_DIR / "secrets" / "google_credentials.json"

SPREADSHEET_ID = "16AAA5yWns7qVMgjBAzZmdmDQAVF1vphGzfMbwSORP1g"

WORKSHEET_NAME = "Sales_Analytics"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]


def load_live_sales_data():
    """Read live sales records from Google Sheets."""

    credentials = Credentials.from_service_account_file(
        str(KEY_FILE),
        scopes=SCOPES
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

    records = worksheet.get_all_records()

    return pd.DataFrame(records)
