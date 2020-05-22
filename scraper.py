
import pandas as pd
from datetime import datetime


def to_unix_time(date_string):

    date_string_list = date_string.split(".")
    day = int(date_string_list[0])
    month = int(date_string_list[1])
    year = int(date_string_list[2])

    x = datetime(year, month, day)

    return int(x.timestamp())



class Yahoo_Finscraper:
    def __init__(self, share_name_short, share_name_long, period_start, period_end):
        self.share_name_short = share_name_short
        self.share_name_long = share_name_long
        self.period_start = period_start
        self.period_end = period_end

        self.request_url = "https://finance.yahoo.com/quote/{sname}/history?period1" \
                      "={p_start}&period2={p_end}&interval=1d&filter=history&frequency=1d".format(sname=self.share_name_short,
                                                                                                  p_start=to_unix_time(self.period_start),
                                                                                                  p_end=to_unix_time(self.period_end))

    def show_description(self):

        descr_dict = {"share_name_short": self.share_name_short,
                      "share_name_long": self.share_name_long,
                      "period_start": self.period_start,
                      "period_end": self.period_end,
                      }
        print(descr_dict)


    def fetch_data(self):

        data = pd.read_html(self.request_url)[0]

        ## TODO: if multiple tables -> concat tables or specify

        return data


    def get_dividend():

        return "pandas dataframe"


    def get_value_series():

        return "pandas dataframe"