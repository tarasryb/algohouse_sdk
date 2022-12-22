import urllib.request
import pandas as pd
import urllib.request
import ah_settings as ahs

def get_fetcher(line):
    result = None
    words = line.split(' ')
    if len(words) > 1:
        result = words[1]
    return result


def get_reference_data(exchanges: list = None) -> pd.DataFrame:
    query = f"/info"
    url = f"{ahs.DOMAIN}{query}"
    contents = urllib.request.urlopen(url).read()
    lines = str(contents).split('\\n')
    result = []
    result_rec = {'exchange': None, 'instruments': []}
    fetcher = None
    for line in lines:
        if 'fetcher:' in line:

            if not result_rec['exchange'] is None:
                if exchanges is None:
                    result.append(result_rec)
                    result_rec = dict()
                else:
                    if result_rec['exchange'] in exchanges:
                        result.append(result_rec)
                        result_rec = dict()

            fetcher = get_fetcher(line)
            result_rec['exchange'] = fetcher
            result_rec['instruments'] = []
            continue

        if not fetcher is None:
            instruments = line.split(' ')
            instruments = list(filter(None, instruments))
            result_rec['instruments'] = result_rec['instruments'] + instruments

    return pd.DataFrame.from_records(result)


def filter_by_instrument(df, instrument):
    if instrument is None:
        return df

    result = []
    for index, row in df.iterrows():
        instruments = row['instruments']
        matching = [s for s in instruments if instrument.upper() in s.upper()]
        if matching:
            result.append({'exchange': row['exchange'],
                           'instruments': matching})
    return pd.DataFrame.from_records(result)


def get_reference_data_v2(exchange: str = None,
                          instrument: str = None,
                          instrument2: str = None) -> pd.DataFrame:
    res = get_reference_data()
    if res.empty:
        return pd.DataFrame()

    if exchange is None:
        return filter_by_instrument(res, instrument)

    exchanges = res[res['exchange'].str.contains(exchange)]
    if len(exchanges) == 0:
        return pd.DataFrame()

    instrument_filtered = filter_by_instrument(exchanges, instrument)
    instrument_filtered = filter_by_instrument(instrument_filtered, instrument2)

    return instrument_filtered
