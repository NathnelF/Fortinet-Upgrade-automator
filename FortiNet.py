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

sheet_id = "13NdjvOwLP41l_ICs_-cqOMOV7LfNemSZqouJqLN_PM8"
MasterSheet = client.open_by_key(sheet_id)
master_url = MasterSheet.url

fortinet_url = 'https://community.fortinet.com/t5/FortiGate/Technical-Tip-Recommended-Release-for-FortiOS/ta-p/227178'

worksheet = MasterSheet.sheet1
models = worksheet.col_values(3)[1:]

def process_model(models):
    updated_models = []
    for model in models:
        split = model.split(" ")
        proper = split[1:]
        if (len(proper) == 2):
            check_for_vm = proper[1].split(" ")
            check_for_vm = list(check_for_vm[0])
            if ('V' in check_for_vm):
                finished = "FortiGate-VM64    -        all versions"
            else:
                finished = "-".join(proper)
            updated_models.append(finished)
        else:
            finished = "Unknown"
            updated_models.append(finished)
    return updated_models

models = process_model(models)
print(models)

Fortinet = pd.read_csv('results.csv', header=None)
devices = Fortinet[0]
versions = Fortinet[1]


def lookup(model, devices, versions):
    version = "Device not found"
    for index, device in enumerate(devices):
        if device.lower() == model.lower():
            version = versions[index]
    return version
    
cells = []
for index, model in enumerate(models):
    print(index, model)
    version = lookup(model, devices, versions)
    print(version)
    cells.append(Cell(index+2, 9, version))
worksheet.update_cells(cells, value_input_option='USER_ENTERED')


