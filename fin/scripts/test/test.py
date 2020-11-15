
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
#from scraper import Yahoo_Finscraper
import requests

url = "https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1587686400&period2=1592956800&interval=1d&events=history"
url_div = "https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1587686400&period2=1592956800&interval=1d&events=div"

shares_raw = requests.get(url, allow_redirects=False)
div_raw = requests.get(url_div, allow_redirects=False)

#print(BytesIO(d.content))
DATA_SHARES = BytesIO(shares_raw.content)
DATA_DIV = BytesIO(div_raw.content)



data_shares = pd.read_csv(DATA_SHARES)

data_div = pd.read_csv(DATA_DIV)

print(data_shares.head())

print(data_shares.dtypes)

print(data_div.head())

print(data_div.dtypes)

#data_shares["Date"] = pd.to_datetime(data_shares["Date"])

#print(data.dtypes)
#print(data)