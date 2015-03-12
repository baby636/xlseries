import pandas as pd
from openpyxl import load_workbook


def infer_freq(av_seconds):

    if av_seconds < 60:
        freq = 'S'
    elif av_seconds < 3600:  # 60*60
        freq = 'T'
    elif av_seconds < 86400:  # 1*24*60*60
        freq = 'H'
    elif av_seconds < 604800:  # 7*24*60*60
        freq = 'D'
    elif av_seconds < 2419200:  # 28*24*60*60
        freq = 'W'
    elif av_seconds < 7776000:  # 90*24*60*60
        freq = 'M'
    elif av_seconds < 15552000:  # 180*24*60*60
        freq = 'Q'
    elif av_seconds < 31536000:  # 365*24*60*60
        freq = Exception("Can't handle semesters!")
    else:
        freq = 'Y'

    return freq


def get_data_frames(xl_file):

    dfs = []

    wb = load_workbook(filename=xl_file, use_iterators=True)
    ws_names = wb.get_sheet_names()

    for ws_name in ws_names:
        df = get_data_frame(xl_file, sheetname=ws_name)
        dfs.append(df)

    return dfs


def get_data_frame(xl_file, sheetname=0):

    df = pd.read_excel(xl_file, sheetname)

    # adopt a datetime index (first excel col)
    df = df.set_index(df.columns[0])

    time_delta = (df.index[-1] - df.index[0]) / df.index.size
    av_seconds = time_delta.total_seconds()
    period_range = pd.period_range(df.index[0],
                                   df.index[-1],
                                   freq=infer_freq(av_seconds))

    # rebuild data frame using a period range with frequency
    df = pd.DataFrame(data=df.values,
                      index=period_range,
                      columns=df.columns)

    return df
