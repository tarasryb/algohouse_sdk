import io
import time
import traceback
import re
import urllib.request
import pandas as pd
import ah_connection as ahc
import ah_utils as ahu
import ah_settings as ahs

# ts underlying_price settlement_price open_interest min_price max_price mark_price
# mark_iv last_price interest_rate index_price
# greek_vega greek_theta greek_rho greek_gamma greek_delta
# estimated_delivery_price bid_iv best_bid_amount best_bid_price
# ask_iv best_ask_amount best_ask_price volume_24h
options_names = ["ts", "comment", "underlying_price", "settlement_price", "open_interest", "min_price", "max_price",
                 "mark_price", "mark_iv", "last_price", "interest_rate", "index_price",
                 "greek_vega", "greek_theta", "greek_rho", "greek_gamma", "greek_delta",
                 "estimated_delivery_price", "bid_iv", "best_bid_amount", "best_bid_price",
                 "ask_iv", "best_ask_amount", "best_ask_price", "volume_24h", "nan"
                 ]
options_types = {"ts": "int64", "comment":"str",
                 "underlying_price":"float", "settlement_price":"float", "open_interest":"float", "min_price":"float", "max_price":"float",
                "mark_price":"float", "mark_iv":"float", "last_price":"float", "interest_rate":"float", "index_price":"float",
                "greek_vega":"float", "greek_theta":"float", "greek_rho":"float", "greek_gamma":"float", "greek_delta":"float",
                "estimated_delivery_price":"float", "bid_iv":"float", "best_bid_amount":"float", "best_bid_price":"float",
                "ask_iv":"float", "best_ask_amount":"float", "best_ask_price":"float", "volume_24h":"float",
                "nan": "str"}


def get_options(connection: ahc.Connection,
               exchange: str, instrument: str,
               from_time: str, to_time: str) -> pd.DataFrame:
    """

    Get options quotes
    :param connection: Algohouse connection object
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data
    :param to_time: end time of the requested data
    :return: Pandas DataFrame with the columns: ts, bs (B, S), price, volume
    """
    query = f"/option_quotes?ins={instrument}&ex={exchange}&from={from_time}&to={to_time}"
    rts = str(int(time.time()) * 1000)
    q = f"{query}&signerEmail={connection.user_email}&requestTimestamp={rts}"
    sig = ahu.signature(connection.signkey, q)

    url = f"{ahs.DOMAIN}{q}&signature={sig}"

    try:
        contents = urllib.request.urlopen(url).read()
    except TimeoutError as e:
        print('!!! API connection timeout')
        return
    print()
    for match in re.finditer('# ', str(contents)):
        print('***', str(contents)[match.end():match.end() + 100])

    buffer = io.StringIO(contents.decode('utf-8'))
    try:
        df = pd.read_csv(filepath_or_buffer=buffer,
    # try:
    #     df = pd.read_csv(url,
    #                      encoding='utf-8',
                         delimiter=' ',#'\\t',
    #                      lineterminator='\\n',
                         header=None,
                         # to avoid parsing the last strings:
                         # truncated
                         # END
                         # skipfooter=2,
                         comment="#",
                         engine='python',
                         names=options_names,
                         na_values=[int, '', 'NA'],
                         keep_default_na=False,
                         # verbose=True,
                         dtype=options_types
                         )

    # try:
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        comment = df['comment']
        splitted = comment.apply(lambda str: str.split('-'))
        splitted_df = pd.DataFrame.from_records(splitted.values)
        splitted_df = splitted_df.rename(columns={0: "underlying_index", 1:"expiry", 2: "strike_price", 3: "kind"})
        df = df.merge(splitted_df, left_index=True, right_index=True)

        df = df.drop(columns=['nan'])
    except Exception:
        print(traceback.format_exc())
        df = None

    return df

