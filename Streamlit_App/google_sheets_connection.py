from pathlib import Path

import gspread
import pandas as pd
import streamlit as st
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

    # Local environment authentication
    if KEY_FILE.exists():
        credentials = Credentials.from_service_account_file(
            str(KEY_FILE),
            scopes=SCOPES
        )

    # Streamlit Cloud authentication
    else:
        credentials = Credentials.from_service_account_info(
            dict(st.secrets["gcp_service_account"]),
            scopes=SCOPES
        )

    # Authorize Google Sheets connection
    client = gspread.authorize(credentials)

    # Open spreadsheet
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # Select worksheet
    worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

    # Retrieve sales records
    records = worksheet.get_all_records()

    # Convert records into DataFrame
    return pd.DataFrame(records)
