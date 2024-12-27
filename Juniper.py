import os
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import GSpreadException
from gspread.exceptions import APIError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from gspread import Cell
import time
import logging
import pandas as pd
import numpy as np
import time

#Connect python script to google sheets API
CLIENT_FILE = 'desktopoauthkey.json'

scope = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

sheet_id = "1O4JgY7MJS9lFCsHEWpdzJUC_PLR_kzXdGigP-mruqL4"

master_sheet = client.open_by_key(sheet_id)
worksheet = master_sheet.sheet1

Junpyer = pd.read_csv('Junyper_results.csv', header=None)
devices = Junpyer[0]
versions = Junpyer[1]

