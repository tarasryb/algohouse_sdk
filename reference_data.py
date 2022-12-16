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
    """

    :param exchanges: optional list of exchanges, in None, the function will return all of them
    :return: Pandas DataFrame with the columns: exchange (string), instruments (list of strings)
    """
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


