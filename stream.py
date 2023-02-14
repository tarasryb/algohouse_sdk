import time
import urllib.request

import requests as requests

import ah_connection as ahc
import ah_settings as ahs
import ah_utils as ahu
import orderbook
import trades


def get_stream(connection: ahc.Connection,
               exchange: str, instrument: str,
               on_trade=None, on_order=None, on_error=None
               ):
    query = f"/stream?ins={instrument}&ex={exchange}"  # &to={to_time}
    rts = str(int(time.time()) * 1000)
    q = f"{query}&signerEmail={connection.user_email}&requestTimestamp={rts}"
    sig = ahu.signature(connection.signkey, q)

    url = f"{ahs.DOMAIN}{q}&signature={sig}"

    r = requests.get(url, stream=True)

    if r.encoding is None:
        r.encoding = 'utf-8'

    try:
        for line in r.iter_lines(decode_unicode=True):
            if line:
                if line[0] == '#':
                    print('>>> COMMENT ' + line[0:50])
                if line[0] == '!':
                    if not on_trade is None:
                        trades_df = trades.parse_trades_stream(line[2:])
                        on_trade(trades_df)
                if line[0] == '$':
                    if not on_order is None:
                        orders_df = orderbook.parse_orders_stream(line[2:])
                        on_order(orders_df)
    except KeyboardInterrupt as key:
        print('<<< Stopped >>>')
    except Exception as e:
        if not on_error is None:
            on_error(e)
