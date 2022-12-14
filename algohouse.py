import io
import time
import hashlib
import hmac
import traceback
import urllib.request
import pandas as pd
import urllib.request
from io import StringIO
import re

DOMAIN = 'https://api.algohouse.ai'

trades_names = ["ts", "bs", "price", "volume", "nan"]
trades_types = {"ts": "int64",
                "bs": "str",
                "price": "float",
                "volume": "float",
                "nan": "str"}

trades_aggregated_names = ["ts", "open", "high", "low", "close", "volume", "rec_count", "avg_price"]
trades_aggregated_types = {"ts": "int64",
                           "open": "float",
                           "high": "float",
                           "low": "float",
                           "close": "float",
                           "volume": "float",
                           "rec_count": "int",
                           "avg_price": "float"}

orderbook_names = ["ts", "bs", "delta", "reset"]
orderbook_types = {"ts": "int64",
                   "bs": "str",
                   "delta": "str",
                   "reset": "str"}


def signature(key, msg):
    key = key.encode('ascii')
    msg = msg.encode()
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


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
    url = f"{DOMAIN}{query}"
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


def get_trades(user_email: str, signkey: str,
               exchange: str, instrument: str,
               from_time: str, to_time: str) -> pd.DataFrame:
    """

    Get trades historical data
    :param user_email: e-mail of the Algohouse user who registered as API user
    :param signkey: the key to sign the request
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data
    :param to_time: end time of the requested data
    :return: Pandas DataFrame with the columns: ts, open, high, low, close, volume, rec_count, avg_price
    """
    query = f"/trades?ins={instrument}&ex={exchange}&from={from_time}&to={to_time}"
    rts = str(int(time.time()) * 1000)
    q = f"{query}&signerEmail={user_email}&requestTimestamp={rts}"
    sig = signature(signkey, q)

    url = f"{DOMAIN}{q}&signature={sig}"

    try:
        df = pd.read_csv(url,
                         encoding='utf-8',
                         delimiter='\t',
                         header=None,
                         # to avoid parsing the last strings:
                         # truncated
                         # END
                         # skipfooter=2,
                         comment="#",
                         engine='python',
                         names=trades_names,
                         na_values=[int, '', 'NA'],
                         keep_default_na=False,
                         verbose=True,
                         dtype=trades_types
                         )

        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df = df.drop(columns=['nan'])
    except Exception:
        print(traceback.format_exc())
        df = None

    return df


def get_trades_aggregated(user_email: str, signkey: str,
                          exchange: str, instrument: str,
                          from_time: str, to_time: str,
                          aggregation: str = '1m') -> pd.DataFrame:
    """

    :param user_email: e-mail of the Algohouse user who registered as API user
    :param signkey: the key to sign the request
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data
    :param to_time: end time of the requested data
    :param aggregation: the type of the aggregation (1m, 15m, 1h, 1d)
    :return: Pandas DataFrame with the columns: ts, open, high, low, close, volume, rec_count, avg_price
    """
    query = f"/trades_aggregated?ins={instrument}&ex={exchange}&from={from_time}&to={to_time}&aggregation={aggregation}"
    rts = str(int(time.time()) * 1000)
    q = f"{query}&signerEmail={user_email}&requestTimestamp={rts}"
    sig = signature(signkey, q)

    url = f"{DOMAIN}{q}&signature={sig}"

    try:
        df = pd.read_csv(url,
                         encoding='utf-8',
                         delimiter='\t',
                         header=None,
                         # to avoid parsing the last string:
                         # END
                         # skipfooter=1,
                         comment="#",
                         engine='python',
                         names=trades_aggregated_names,
                         na_values=[int, '', 'NA'],
                         keep_default_na=False,
                         verbose=True,
                         dtype=trades_aggregated_types)

        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    except Exception:
        print(traceback.format_exc())
        df = None

    return df


def get_orderbook(user_email: str, signkey: str,
                  exchange: str, instrument: str,
                  from_time: str, to_time: str) -> pd.DataFrame:
    """

    :param user_email: e-mail of the Algohouse user who registered as API user
    :param signkey: the key to sign the request
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data
    :param to_time: end time of the requested data
    :return: Pandas DataFrame with the columns: ts, open, high, low, close, volume, rec_count, avg_price
    """
    query = f"/orderbooks?ins={instrument}&ex={exchange}&from={from_time}&to={to_time}"
    rts = str(int(time.time()) * 1000)
    q = f"{query}&signerEmail={user_email}&requestTimestamp={rts}"
    sig = signature(signkey, q)

    url = f"{DOMAIN}{q}&signature={sig}"

    contents = urllib.request.urlopen(url).read()
    print()
    for match in re.finditer('# ', str(contents)):
        print('***', str(contents)[match.end():match.end() + 100])

    buffer = io.StringIO(contents.decode('utf-8'))
    df = pd.read_csv(filepath_or_buffer=buffer,
                     # encoding='utf-8',
                     delimiter='\\t',
                     lineterminator='\\n',
                     header=None,
                     comment="#",
                     # engine='python',
                     names=orderbook_names,
                     na_values=[int, '', 'NA'],
                     keep_default_na=False,
                     dtype=orderbook_types
                     )

    try:
        if False:
            df = pd.read_csv(url,
                         encoding='utf-8',
                         delimiter='\t',
                         header=None,
                         # to avoid parsing the last strings:
                         # truncated
                         # END
                         # skipfooter=4,
                         comment="#",
                         engine='python',
                         names=orderbook_names,
                         na_values=[int, '', 'NA'],
                         keep_default_na=False,
                         verbose=True,
                         dtype=orderbook_types
                         )

        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    except Exception:
        print(traceback.format_exc())
        df = None

    return df
