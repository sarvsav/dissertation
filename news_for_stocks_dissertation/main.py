import pprint
from datetime import date, timedelta

from bs4 import BeautifulSoup
import typing

from truck.truck import Truck

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


if __name__ == '__main__':
    stime = 44927
    start_date = date(2023, 1, 1)
    end_date = date(2023, 1, 5)  # yyyy-mm-dd
    for single_date in daterange(start_date, end_date):
        year, month, day = single_date.strftime("%Y-%#m-%#d").split("-")
        truck = Truck(year=year, month=month, stime=stime)
        truck.dumps()
        result = get_headlines(f"data/{year}_{month}_{stime}.html")
        news_date = f"{day}/{month}/{year}"
        truck.dump_to_csv(result, news_date)
        stime += 1
        break