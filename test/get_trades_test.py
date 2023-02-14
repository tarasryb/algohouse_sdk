import datetime
import pandas as pd

import algohouse as ah
import ah_connection as ahc

USER_EMAIL = 'intern@intela.io'
SIGNKEY = '7c45593ac289db2a1d37e6a0387bbd18'


def test_get_trades_aggregated():
    conn = ahc.Connection(USER_EMAIL, SIGNKEY)
    res = ah.get_trades_aggregated(conn,
                                   instrument='1000LUNCBUSD',
                                   exchange='binance/f',
                                   from_time='2022-11-12T00:00:00',
                                   to_time='2022-11-20T23:00:00',
                                   aggregation='1m')
    print()
    print(res)
    assert not res is None


def test_get_trades():
    conn = ahc.Connection(USER_EMAIL, SIGNKEY)
    res = ah.get_trades(conn,
                        instrument='1000LUNCBUSD',
                        exchange='binance/f',
                        from_time='2022-11-12T00:00:00',
                        to_time='2022-11-20T23:00:00')
    print()
    print(res)
    assert not res is None


