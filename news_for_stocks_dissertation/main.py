#  Copyright (c) 2023.
#  BITS Pilani, Dissertation
#  Student Name: Sarvsav Sharma
#  Student Id: 2020sc04239

import pprint
import sys
import os
from datetime import date, timedelta
import warnings
warnings.filterwarnings("ignore")

from bs4 import BeautifulSoup
from nsetools import Nse
import typing

from app import app
from truck.truck import Truck
#nsebuyprice = 1578.25

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_headlines(file_name: str) -> typing.List:
    with open(file_name, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, features="html.parser")
        result = soup.find_all("a", attrs={'target': None,
                                            'title': None,
                                            'data-ga-onclick': None,
                                            'class': None,
                                            'style': None})
        return result

def get_nse_data():
    nse = Nse()
    print(nse)
    q = nse.get_quote('hdfcbank')
    #q['buyPrice'] = nsebuyprice
    stock_num_data = {
        'prev close': q['previousClose'],
        'open': q['open'],
        'high': q['dayHigh'],
        'low': q['dayLow'],
        'last': q['lastPrice'],
        'max_sell_price': q['sellPrice1'],
        #'max_buy_price': q['averagePrice']
        'max_buy_price': q['buyPrice1']
    }
    #pprint.pprint(q)
    return stock_num_data
    #all_stock_codes = nse.get_stock_codes()
    #pprint.pprint(all_stock_codes)

if __name__ == '__main__':
    stime = 44927
    stime = 45015
    start_date = date(2023, 3, 30)
    end_date = date(2023, 3, 31)  # yyyy-mm-dd
    for single_date in daterange(start_date, end_date):
        year, month, day = single_date.strftime("%Y-%#m-%#d").split("-")
        truck = Truck(year=year, month=month, stime=stime)
        truck.dumps()
        result = get_headlines(f"data/{year}_{month}_{stime}.html")
        news_date = f"{day}/{month}/{year}"
        truck.dump_to_csv(result, news_date)
        stime += 1


    stock_stats_today = get_nse_data()
    pprint.pprint(stock_stats_today)
    app.run(stock_stats_today)
    os.remove("out/data.csv")
