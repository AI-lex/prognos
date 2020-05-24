
import pandas as pd
from scraper import Yahoo_Finscraper


yfs = Yahoo_Finscraper("AAPL", "Apple", "15.03.2020", "22.05.2020")


yfs.show_description()

print(yfs.request_url)

print(yfs.get_dividend())

print(yfs.get_share_values())

yfs.show_visualizations()

#print(int(data["Adj Close**"]) - int(data["Close*"]))

#data = data.set_index("Date")

#print(data.to_string())