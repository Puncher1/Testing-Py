import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
import time
load_dotenv()

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
essayTicketLog_key = "1pB5xpsBGKIES5vmEY4hjluFg7-FYolOmN_w3s20yzr0"
sa_creds = json.loads(os.getenv("GSPREADSJSON"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(sa_creds, scope)
gspread_client = gspread.authorize(creds)

sheet = gspread_client.open_by_key(essayTicketLog_key).sheet1
values_list = sheet.col_values(1)
for value in values_list:
    if not value == "":
        count = values_list.count(value)
        if count > 1:
            cell = sheet.find(value)
            sheet.update_cell(cell.row, cell.col, "")
            values_list.remove(value)
            time.sleep(0.75)
