import os
from datetime import datetime

import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import pandas as pd
from matplotlib import cm


def select_name(x):
    if len(x) > 1:
        return x[~x.str.match('Removed user')]
    return x


def next_same_user(df): return df.shift(-1)['UserID'] == df['UserID']


def prev_same_user(df): return df.shift(1)['UserID'] == df['UserID']


def is_smiley(df): return (df['MessageBody'].str.len() == 2) & (df['MessageBody'].str.startswith(':'))


if __name__ == '__main__':
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    template = env.get_template('two-column-template.jinja2')

    # df = pd.read_csv('data/Wongwahmeni-total.csv')
    # df = pd.read_csv(r'data/Klub Kouzelniku_2019_07_01 01_43-total.csv', encoding='utf-8')
    df = pd.read_csv(r'data/Die Ta_2019_10_25 00_17.csv', encoding='utf-8')
    # df = pd.read_csv('data/example.csv')
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['MessageBody'] = df['MessageBody'].fillna('').str.replace('&', '&amp;', regex=False)
    df['MessageBody'] = df['MessageBody'].fillna('').str.replace('>', '&gt;', regex=False)
    df['MessageBody'] = df['MessageBody'].fillna('').str.replace('<', '&lt;', regex=False)
    df['MessageBody'] = df['MessageBody'].str.replace('[\?#]utm_.*', '')
    df['MessageBody'] = df['MessageBody'].fillna('').str.replace('\\n', '<br/>', regex=False)
    df = df.set_index('DateTime', drop=False)

    # colors for individual users
    user_colors = cm.tab20(range(len(df['UserID'].unique())))
    user_colors[:, 3] = 0.2
    user_colors[:, :3] *= 255
    user_colors[:, :3] //= 1
    # ptají se na kolik tramvají má DP, naprgat fibbonaciho posloupnost, binární strom, databáz. struktura konzultant, projekty, hodin. sazby, jak spočítám ziskovost DP?
    user_to_color = {user_id: [str(i) for i in user_colors[i]] for i, user_id in enumerate(df['UserID'].unique())}

    # if user was missing for some time, he has Removed User XYZ instead of his name. This is fixed here.
    id_and_name = df.groupby(['UserID', 'UserName']).count().index.to_frame().reset_index(drop=True)
    id_to_name = id_and_name.groupby('UserID').agg(select_name)

    # I can not pair images to text, so I exclude empty messages
    df = df[df['MessageBody'] != '']

    # lots of messages is one char long, and they are after another message from same user, merging them
    one_char_suffix = (df.shift(-1)['MessageBody'].str.len() == 1) & next_same_user(df)
    one_char_suffix_next = (df['MessageBody'].str.len() == 1) & prev_same_user(df)
    df.loc[one_char_suffix, 'MessageBody'] += ' ' + df.shift(-1)[one_char_suffix]['MessageBody']
    df = df[~one_char_suffix_next]

    # also lots of 2char emoji faces appears as individual message, appending them
    smiley_suffix = is_smiley(df.shift(-1)) & next_same_user(df)
    smiley_suffix_next = is_smiley(df) & prev_same_user(df)
    df.loc[smiley_suffix, 'MessageBody'] += ' ' + df.shift(-1)[smiley_suffix]['MessageBody']
    df = df[~smiley_suffix_next]

    # df = df[:1000]
    data = []
    print('loaded data')
    # assume sorted
    # date_window = df.iloc[0]['DateTime'].replace(minute=df.iloc[0]['DateTime'].minute // 10 * 10, second=0)
    # timeslot = []
    # prev_row = None
    # for index, row in df.iterrows():
    #     # 10 minute windows
    #     if (row['DateTime'] - date_window).seconds > (10 * 60):
    #         data.append((date_window.strftime("%#d.%#m.%#Y, %H:%M"), timeslot))
    #         date_window = row['DateTime'].replace(minute=row['DateTime'].minute // 10 * 10, second=0)
    #         timeslot = []
    #         prev_row = None
    #         if len(data) % 1000 == 0:
    #             print(date_window)
    #
    #     # merging messages from same person
    #     if prev_row is not None and row['UserID'] == prev_row['UserID'] and (
    #             row['DateTime'] - prev_row['DateTime']).seconds <= 60:
    #         prev_data = timeslot[-1]
    #         timeslot[-1] = (prev_data[0], prev_data[1] + '<br/>' + row['MessageBody'])
    #     else:
    #         timeslot.append((row['UserName'], row['MessageBody']))
    #     prev_row = row
    # data.append((date_window.strftime("%#d.%#m.%#Y, %H:%M"), timeslot))

    # this is not so terribly slow, todo: benchmark

    for name, group in df.groupby(pd.Grouper(freq='10Min')):
        if len(group) == 0:
            continue
        timeslot = []
        prev_row = None
        for index, row in group.iterrows():
            # merging messages from same person
            if prev_row is not None and row['UserID'] == prev_row['UserID'] and (
                    row['DateTime'] - prev_row['DateTime']).seconds <= 60:
                prev_data = timeslot[-1]
                timeslot[-1] = (prev_data[0], prev_data[1] + '<br/>' + row['MessageBody'], prev_data[2])
            else:
                timeslot.append(
                    (id_to_name.loc[row['UserID']]['UserName'], row['MessageBody'], user_to_color[row['UserID']]))
            prev_row = row
        data.append((name.strftime("%#d.%#m.%#Y, %H:%M"), timeslot))
        if len(data) % 1000 == 0:
            print(name)

    print('data converted')
    # template.stream(rows=data).dump('data/Wongwahmeni-total.html')
    # template.stream(rows=data).dump('data/Klub Kouzelniku_2019_07_01 01_43-total.html')
    template.stream(rows=data).dump('data/Die Ta_2019_10_25 00_17.html')

    # chrome_exe = '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"'
    # pdf_file = f'{THIS_DIR}\data\Wongwahmeni-total.pdf'
    # os.system(f'{chrome_exe} --headless --disable-gpu --no-sandbox --print-to-pdf={pdf_file} {THIS_DIR}\data\Wongwahmeni-total.html')

    # print(datetime.strptime('2018-03-14 11:47 AM', '%Y-%m-%d %I:%M %p').strftime("%d.%#m.,%I:%M"))
