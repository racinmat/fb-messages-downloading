import os
from datetime import datetime

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import pandas as pd


if __name__ == '__main__':
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    template = env.get_template('two-column-template.html')

    df = pd.read_csv('Anime world _2018_09_23 20_18.csv')
    data = []
    print('loaded data')
    for index, row in df.iterrows():
        # date = datetime.strptime(row['Date'], '%Y-%m-%d %I:%M %p').strftime("%#d.%#m.,%H:%M")     # not working now, probably changed format
        date = datetime.strptime(row['Date'] + ' ' + row['Time'], '%Y-%m-%d %H:%M:%S').strftime("%#d.%#m.,%H:%M")
        data.append((date, row['UserName'], row['MessageBody']))
    print('data converted')
    template.stream(rows=data).dump('animeworld.html')


    # print(datetime.strptime('2018-03-14 11:47 AM', '%Y-%m-%d %I:%M %p').strftime("%d.%#m.,%I:%M"))