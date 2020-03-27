import time
from datetime import date, timedelta, datetime
import pandas as pd
from collections import defaultdict


class COVIDData:
    def __init__(self, data_file):
        self.df = None
        self.data_country = defaultdict(dict)
        self.__data_file = data_file
        self.end_time = date.today().strftime('%Y-%m-%d')

    def read_data(self):
        self.df = pd.read_json(self.__data_file)

        self.df['updateTime'] = self.df['updateTime'].apply(lambda item: time.strftime('%Y-%m-%d', time.localtime(item // 1000)))
        self.df.drop_duplicates(subset=['provinceShortName', 'updateTime'], keep='last', inplace=True)

    def add_time_data(self, country_name, current_time, last_count):
        if country_name in self.data_country:
            if current_time in self.data_country[country_name]:
                self.data_country[country_name][current_time] += last_count
            else:
                self.data_country[country_name].setdefault(current_time, last_count)
        else:
            self.data_country[country_name].setdefault(current_time, last_count)

    def fill_time_data(self, current_time, endtime, last_count, country_name):
        time_delta = 0
        start_time = datetime.strptime(current_time, '%Y-%m-%d')
        while current_time < endtime:
            self.add_time_data(country_name, current_time, last_count)
            time_delta += 1
            current_time = (start_time + timedelta(days=time_delta)).strftime('%Y-%m-%d')

    def parse_data(self):
        for province_name, items in self.df.groupby(by=['provinceName']):
            if province_name == '中国':
                continue

            start_time = date(year=2020, month=1, day=22)
            current_time = start_time.strftime('%Y-%m-%d')
            last_count = 0
            country_name = items['countryName'].values[0]
            for update_time, item in items.groupby(by=['updateTime']):
                now = (datetime.strptime(current_time, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                if now < update_time:
                    self.fill_time_data(now, update_time, last_count, country_name)

                last_count = item['confirmedCount'].values[0]
                current_time = update_time
                self.add_time_data(country_name, current_time, last_count)

            now = (datetime.strptime(current_time, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            if now < self.end_time:
                self.fill_time_data(now, self.end_time, last_count, country_name)


    def save_data_file(self):
        fp = open('data.csv', 'w')
        fp.write('name,value,date\n')
        for country_name, values in self.data_country.items():
            if country_name == '中国':
                continue

            for t, v in values.items():
                fp.write('{},{},{}\n'.format(country_name, v, t))
        fp.close()


if __name__ == '__main__':
    covid = COVIDData('json/DXYArea-TimeSeries.json')
    covid.read_data()
    covid.parse_data()
    covid.save_data_file()