

from scraper import Yahoo_Finscraper


yfs = Yahoo_Finscraper("AAPL", "Apple", "15.04.2020", "22.05.2020")



print(yfs.get_dividend())

print(yfs.get_share_values())

#print(yfs.request_url)
#yfs.show_visualizations()

