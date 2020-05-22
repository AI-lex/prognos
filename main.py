

from scraper import Yahoo_Finscraper


yfs = Yahoo_Finscraper("AAPL", "Apple", "15.05.2020", "21.05.2020")


yfs.show_description()

print(yfs.request_url)

print(yfs.fetch_data()["Open"])
