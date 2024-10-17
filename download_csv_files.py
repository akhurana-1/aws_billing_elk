import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import re

# Function to download all sheets in a Google Sheets file
def download_sheets(spreadsheet_url, folder_path, json_keyfile_name):
    # Extract the spreadsheet ID from the URL
    match = re.search(r'/d/([^/]+)', spreadsheet_url)
    if not match:
        print("Invalid Google Sheets URL.")
        return
    spreadsheet_id = match.group(1)

    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Authenticate using the service account
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_name, scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet
    spreadsheet = client.open_by_key(spreadsheet_id)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Download each sheet
    for worksheet in spreadsheet.worksheets():
        sheet_name = worksheet.title
        data = worksheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])  # Skip header
        csv_file_path = os.path.join(folder_path, f"{sheet_name}.csv")
        df.to_csv(csv_file_path, index=False)
        print(f"Downloaded {sheet_name} to {csv_file_path}")

# Usage
if __name__ == "__main__":
    # Prompt for the Google Sheets URL
    spreadsheet_url = input("Enter the Google Sheets URL: ")
    FOLDER_PATH = 'input'  # Replace with your desired folder path
    JSON_KEYFILE_NAME = 'google-sheets-key.json'  # Replace with your JSON key file path

    download_sheets(spreadsheet_url, FOLDER_PATH, JSON_KEYFILE_NAME)