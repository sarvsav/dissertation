import csv

import requests

class Truck():

    year = 2023
    #stime = 44927 # 1 January, 2023 - 36892 - 1 Jan, 2001
    stime = 45006
    month = 1
    url = f'https://economictimes.indiatimes.com/archivelist/year-{year},month-{month},starttime-{stime}.cms'
    html_output = f'data/{year}_{month}_{stime}.html'

    def __init__(self, year, month, stime):
        self.year = year
        self.stime = stime  # 1 January, 2023 - 36892 - 1 Jan, 2001
        self.month = month
        self.url = f'https://economictimes.indiatimes.com/archivelist/year-{year},month-{month},starttime-{stime}.cms'
        self.html_output = f'data/{year}_{month}_{stime}.html'

    def dumps(self):
        req = requests.get(self.url,
                       'html.parser',
                       headers={
                           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
                       })
        with open(self.html_output, 'w', encoding='utf-8') as f:
            f.write(req.text)

    def dump_to_csv(self, result, news_date):
        print(news_date)
        row = [news_date]
        for data in result[3:-1]:
            row.append(data.get_text())
        with open("out/data.csv", "a", encoding="utf-8") as fp:
            wr = csv.writer(fp, dialect="excel")
            wr.writerow(row)