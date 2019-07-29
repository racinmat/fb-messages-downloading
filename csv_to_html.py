import os
from datetime import datetime

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import pandas as pd

if __name__ == '__main__':
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    template = env.get_template('two-column-template.html')

    # df = pd.read_csv('data/Wongwahmeni-total.csv')
    df = pd.read_csv('data/example.csv')
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

    data = []
    print('loaded data')
    prev_row = None
    for index, row in df.iterrows():
        # date = datetime.strptime(row['Date'], '%Y-%m-%d %I:%M %p').strftime("%#d.%#m.,%H:%M")     # not working now, probably changed format
        date = row['DateTime'].strftime("%#d.%#m.,%H:%M")
        # merging messages from same person
        if prev_row is not None and row['UserID'] == prev_row['UserID'] and (
                row['DateTime'] - prev_row['DateTime']).seconds <= 60:
            data[-1] = (data[-1][0], data[-1][1], data[-1][2] + '<br/>' + row['MessageBody'])
        else:
            data.append((date, row['UserName'], row['MessageBody']))
        prev_row = row
    print('data converted')
    # template.stream(rows=data).dump('data/Wongwahmeni-total.html')
    template.stream(rows=data).dump('data/example.html')

    # print(datetime.strptime('2018-03-14 11:47 AM', '%Y-%m-%d %I:%M %p').strftime("%d.%#m.,%I:%M"))
