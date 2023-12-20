from definitions import DATA_DIR, XML_FILE

from bs4 import BeautifulSoup
import pandas as pd


import traceback


with open(DATA_DIR / XML_FILE, 'r', encoding='utf8') as f:
    file = f.read()

soup = BeautifulSoup(file, 'lxml')
