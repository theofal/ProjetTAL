# This page is in regard of the Google Sheet. Our dictionaries will be stored there and updated
# automatically.
# Link to the Google sheet :
# https://docs.google.com/spreadsheets/d/1UR3POVh4q2Qr6kkQJfjFEOTbYE55BPWbU_eLBULXDh0/edit?usp=sharing


from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'GdocData.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1UR3POVh4q2Qr6kkQJfjFEOTbYE55BPWbU_eLBULXDh0'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()


def getDataGdoc():
    # Gets data from a Google Sheet and returns a list of lists
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="ITA!A:B").execute()
    values = result.get('values', [])
    return values


def updateGdoc(list1):
    # Needs a list of lists and the name of the Google tab as string
    # Update the Google Sheet with a list of lists
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                          range="Accuracy!R16", valueInputOption="RAW", body={"values": list1}).execute()

# request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                                  range="ITA!A1", valueInputOption="RAW",
#                                                  insertDataOption="OVERWRITE", body={"majorDimension":list1})
# request.execute()
