
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

# Project paths
BASE_DIR = Path(__file__).resolve().parent
KEY_FILE = BASE_DIR / "secrets" / "google_credentials.json"

# Google Sheets read-only permission
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

# Authenticate
credentials = Credentials.from_service_account_file(
    str(KEY_FILE),
    scopes=SCOPES
)

client = gspread.authorize(credentials)

# Existing SalesPulse AI spreadsheet
SPREADSHEET_ID = "16AAA5yWns7qVMgjBAzZmdmDQAVF1vphGzfMbwSORP1g"


spreadsheet = client.open_by_key(SPREADSHEET_ID)
worksheet = spreadsheet.worksheet("Sales_Analytics")

# Read sales records
records = worksheet.get_all_records()

print("Google Sheets connection successful!")
print("Total sales records:", len(records))

for record in records[:2]:
    print(record)
