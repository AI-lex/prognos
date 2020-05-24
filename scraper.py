
import pandas as pd
import matplotlib
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

        base_url = "https://finance.yahoo.com/quote/"
        self.request_url = base_url + "{sname}/history?period1" \
                      "={p_start}&period2={p_end}&interval=1d&filter=history&frequency=1d".format(sname=self.share_name_short,
                                                                                                  p_start=to_unix_time(self.period_start),
                                                                                                   p_end=to_unix_time(self.period_end))
        ## fetch data
        ## TODO: if multiple tables -> concat tables or specify
        data = pd.read_html(self.request_url)[0]

        self.share_values, self.dividend = self.to_df(data)

    def show_description(self):

        descr_dict = {"share_name_short": self.share_name_short,
                      "share_name_long": self.share_name_long,
                      "period_start": self.period_start,
                      "period_end": self.period_end,
                      }
        print(descr_dict)


    def to_df(self, data):

        ## delete last row with additional informations
        data = data[:-1].copy()

        ## set date column with datetype
        data["Date"] = pd.to_datetime(data["Date"], format="%b %d, %Y")  # Format: May 15, 2020

        ## share value and dividend payment are on the same date
        dub = data.duplicated(subset="Date", keep="first")

        ## format dividend payments as a separat timeseries
        dividend = data[dub][["Date", "Open"]].copy()

        dividend["Dividend"] = dividend["Open"].apply(lambda x: float(x.split(" ")[0]))

        dividend = dividend.drop(columns=["Open"])

        dividend = dividend.set_index("Date")

        ## keep share_values in a df without dividend payments
        share_values = data.drop(data[dub].index)

        mapper = {"Close*": "Close", "Adj Close**": "Adj_Close"}
        share_values = share_values.rename(columns=mapper)


        share_values = share_values.set_index("Date")

        float_columns = ["Open", "High", "Low", "Close", "Adj_Close"]
        share_values[float_columns] = share_values[float_columns].astype(float)
        share_values["Volume"] = share_values["Volume"].astype(int)

        return share_values, dividend

    def get_dividend(self):

        return self.dividend

    def get_share_values(self):

        return self.share_values

    def show_visualizations(self):

        self.share_values["Open"].plot()
