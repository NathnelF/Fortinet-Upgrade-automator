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


Export = pd.read_csv('Auvik export.csv')
headers = list(Export.columns)
Devices = Export['Make & Model']
#print(Devices)

def search_list(df, target):
    list = []
    for device in df:
        if target in device:
            list.append(device)
        else:
            continue
    return list

c = search_list(Devices, "Fortinet")
c_unique = set(c)
print(c_unique)

def write_to_file(list, file_path):
    with open(file_path, "a") as file:
        for item in list:
            file.write(f"{item}\n")
    
    print("results appended to file")
    return

write_to_file(c_unique, "fortinet_models.txt")