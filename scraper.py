
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
import requests


def to_datetime(date_string):

    date_string_list = date_string.split(".")
    day = int(date_string_list[0])
    month = int(date_string_list[1])
    year = int(date_string_list[2])

    return datetime(year, month, day)


class Yahoo_Finscraper:
    def __init__(self, share_name_short, share_name_long, period_start, period_end):
        self.share_name_short = share_name_short
        self.share_name_long = share_name_long
        self.period_start = to_datetime(period_start)
        self.period_end = to_datetime(period_end)
        self.timespan = self.period_end - self.period_start

        base_url = "https://query1.finance.yahoo.com/v7/finance/download/"



        self.request_url = self.build_request_url(base_url)

        ## fetch share values and dividend payment
        self.share_values, self.dividend = self.fetch_data(self.request_url)





    def show_description(self):

        descr_dict = {"share_name_short": self.share_name_short,
                      "share_name_long": self.share_name_long,
                      "period_start": self.period_start,
                      "period_end": self.period_end,
                      }
        print(descr_dict)

    def build_request_url(self, base_url):
        # examples
        ## download url: https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=345427200&period2=1590883200&interval=1d&events=history
        # rest url: https://finance.yahoo.com/quote/AAPL/history?period1=1521068400&period2=1590098400&interval=1d&filter=history&frequency=1d


        request_url = base_url + "{sname}?period1" \
                       "={p_start}&period2={p_end}&interval=1d".format(
                sname=self.share_name_short,
                p_start=int(self.period_start.timestamp()),
                p_end=int(self.period_end.timestamp()))

        return request_url

    def get_dividend(self):

        return self.dividend

    def get_share_values(self):

        return self.share_values

    def show_visualizations(self):

        self.share_values["Open"].plot()
        plt.show()

    def fetch_data(self, request_url):

        url_shares = request_url + "&events=history"
        url_div = request_url + "&events=div"

        response_shares = requests.get(url_shares, allow_redirects=False)
        response_div = requests.get(url_div, allow_redirects=False)

        byte_data_shares = BytesIO(response_shares.content)
        byte_data_div = BytesIO(response_div.content)

        data_shares = pd.read_csv(byte_data_shares)
        data_div = pd.read_csv(byte_data_div)

        # set index col
        data_shares["Date"] = pd.to_datetime(data_shares["Date"])
        # rename col
        mapper = {"Adj Close": "Adj_Close"}
        data_shares = data_shares.rename(columns=mapper)

        # set index col
        data_div["Date"] = pd.to_datetime(data_div["Date"])
        data_div = data_div.set_index("Date")

        return data_shares, data_div
