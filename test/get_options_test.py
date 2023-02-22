import datetime
import pandas as pd

import algohouse as ah
import ah_connection as ahc

USER_EMAIL = 'intern@intela.io'
SIGNKEY = '7c45593ac289db2a1d37e6a0387bbd18'


def test_get_options():
    conn = ahc.Connection(USER_EMAIL, SIGNKEY)
    res = ah.get_options(conn,
                        exchange='binance/o',
                        instrument='BTC-230220-25500-C',
                        from_time='2023-02-19T00:00:00',
                        to_time='2023-02-25T00:00:00')
    print()
    print(res)
    assert not res is None


