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


def get_orderbook(user_email: str, signkey: str,
                  exchange: str, instrument: str,
                  from_time: str, to_time: str,
                  metric: str) -> pd.DataFrame:
    query = f"/orderbooks?ins={instrument}&ex={exchange}&from={from_time}&to={to_time}"
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
                     # engine='python',
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

    if metric == 'full':
        return df_n

    if metric == 'reset':
        return df_n.loc[df_n['reset'] == 'R']

    # if metric == 'md':
    #     df_md = build_md(df_n)
    #     return df_md

    # df_reset_g = df_reset.groupby('ts')

    return

    # md_list = []
    # for g in df_g:
    #     md_group = process_order_group(g, exchange, instrument, side)
    #     md_list.append(md_group)
    #     print(pd.DataFrame.from_records(md_group).to_csv())
    #
    # return df


def get_orderbook_md(user_email: str, signkey: str,
                     exchange: str, instrument: str,
                     from_time: str, to_time: str,
                     levels: int) -> pd.DataFrame:
    df = get_orderbook(user_email, signkey, exchange, instrument, from_time, to_time,
                       metric='full')

    df_md = build_md(df)

    return df
