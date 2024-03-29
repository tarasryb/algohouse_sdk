import io
import time
import traceback
import pandas as pd
import ah_connection as ahc
import ah_utils as ahu
import ah_settings as ahs

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

trades_stream_names = ["ts", "ins", "bs", "price", "volume"]
trades_stream_types = {"ts": "int64",
                       "ins": "str",
                       "bs": "str",
                       "price": "float",
                       "volume": "float"}


def get_trades(connection: ahc.Connection,
               exchange: str, instrument: str,
               from_time: str, to_time: str) -> pd.DataFrame:
    """

    Get trades historical data
    :param connection: Algohouse connection object
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data
    :param to_time: end time of the requested data
    :return: Pandas DataFrame with the columns: ts, bs (B, S), price, volume
    """
    query = f"/trades?ins={instrument}&ex={exchange}&from={from_time}&to={to_time}"
    rts = str(int(time.time()) * 1000)
    q = f"{query}&signerEmail={connection.user_email}&requestTimestamp={rts}"
    sig = ahu.signature(connection.signkey, q)

    url = f"{ahs.DOMAIN}{q}&signature={sig}"

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


def parse_trades_stream(contents: str):
    buffer = io.StringIO(contents)
    try:
        df = pd.read_csv(filepath_or_buffer=buffer,
                         delimiter=' ',
                         header=None,
                         comment="#",
                         engine='python',
                         names=trades_stream_names,
                         na_values=[int, '', 'NA'],
                         keep_default_na=False,
                         verbose=True,
                         dtype=trades_stream_types
                         )

        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    except Exception:
        print(traceback.format_exc())
        df = None

    return df


def get_trades_aggregated(connection: ahc.Connection,
                          exchange: str, instrument: str,
                          from_time: str, to_time: str,
                          aggregation: str = '1m') -> pd.DataFrame:
    """

    :param connection: Algohouse connection object
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data
    :param to_time: end time of the requested data
    :param aggregation: the type of the aggregation (1m, 15m, 1h, 1d)
    :return: Pandas DataFrame with the columns: ts, open, high, low, close, volume, rec_count, avg_price
    """
    query = f"/trades_aggregated?ins={instrument}&ex={exchange}&from={from_time}&to={to_time}&aggregation={aggregation}"
    rts = str(int(time.time()) * 1000)
    q = f"{query}&signerEmail={connection.user_email}&requestTimestamp={rts}"
    sig = ahu.signature(connection.signkey, q)

    url = f"{ahs.DOMAIN}{q}&signature={sig}"

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
