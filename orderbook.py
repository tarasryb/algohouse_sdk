from datetime import datetime, timedelta
import io
import time
import traceback
import urllib.request
import pandas as pd
import urllib.request
import re
import ah_settings as ahs
import ah_utils as ahu
from orderutils import normalize_orders, build_md

orderbook_names = ["ts", "bs", "delta", "reset"]
orderbook_types = {"ts": "int64",
                   "bs": "str",
                   "delta": "str",
                   "reset": "str"}

df_n_cached = None
exchange_cached = None
instrument_cached = None


def fits_to_cache(exchange, instrument, from_time):
    if (df_n_cached is None) | (exchange_cached is None) | (instrument_cached is None):
        return False

    from_time_cached = df_n_cached['ts'].min()
    to_time_cached = df_n_cached['ts'].max()
    from_time_dt = datetime.strptime(from_time, ahs.DATETIME_FORMAT)
    fits_to_time_cached = (from_time_dt >= from_time_cached) & (from_time_dt <= to_time_cached)

    return (exchange == exchange_cached) & (instrument == instrument_cached) & fits_to_time_cached


def get_orderbook_from_server(user_email: str, signkey: str,
                              exchange: str, instrument: str,
                              from_time: str) -> pd.DataFrame:
    query = f"/orderbooks?ins={instrument}&ex={exchange}&from={from_time}&limit={ahs.ORDER_LINES_TO_READ}"  # &to={to_time}
    rts = str(int(time.time()) * 1000)
    q = f"{query}&signerEmail={user_email}&requestTimestamp={rts}"
    sig = ahu.signature(signkey, q)

    url = f"{ahs.DOMAIN}{q}&signature={sig}"

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
                     engine='python',
                     names=orderbook_names,
                     na_values=[int, '', 'NA'],
                     keep_default_na=False,
                     dtype=orderbook_types
                     )

    try:
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    except Exception:
        print(traceback.format_exc())
        df = None

    df_n = normalize_orders(df)
    return df_n


def get_orderbook(user_email: str, signkey: str,
                  exchange: str, instrument: str,
                  from_time: str,
                  levels: int) -> dict:

    global exchange_cached
    global instrument_cached
    global df_n_cached

    if not fits_to_cache(exchange, instrument, from_time):
        exchange_cached = exchange
        instrument_cached = instrument
        df_n_cached = get_orderbook_from_server(user_email, signkey, exchange, instrument, from_time)

    df_md = build_md(df_n_cached, from_time, levels)
    return df_md


