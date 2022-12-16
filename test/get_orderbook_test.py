import datetime
import pandas as pd

import algohouse as ah

USER_EMAIL = 'tarasryb@gmail.com'
SIGNKEY = '9566c74d10037c4d7bbb0407d1e2c649'
# USER_EMAIL = 'vyklyuk@ukr.net'
# SIGNKEY = '81855ad8681d0d86d1e91e00167939cb'


def _test_get_orderbook():
    res = ah.get_orderbook(USER_EMAIL, SIGNKEY,
                                          exchange='lbank',  # 'binance',  # 'binance/f',
                                          instrument='BTS_USDT',  # 'BTCB_USD',  # '1000LUNCBUSD',
                                          from_time='2022-11-12T10:00:00',
                                          to_time='2022-11-12T10:02:00',
                                          metric='full'
                           )
    print(res.shape)
    assert not res is None


def _test_get_orderbook_reset():
    res = ah.get_orderbook(USER_EMAIL, SIGNKEY,
                                          exchange='lbank',  # 'binance',  # 'binance/f',
                                          instrument='BTS_USDT',  # 'BTCB_USD',  # '1000LUNCBUSD',
                                          from_time='2022-11-12T10:00:00',
                                          to_time='2022-11-12T10:02:00',
                                          metric='reset'
                           )
    print(res.shape)
    assert not res is None


def test_get_orderbook_md():
    res = ah.get_orderbook_md(USER_EMAIL, SIGNKEY,
                                          exchange='binance/f',  # 'lbank',  # 'binance',  # 'binance/f',
                                          instrument='BTCBUSD',  # 'BTS_USDT',  # 'BTCB_USD',  # '1000LUNCBUSD',
                                          from_time='2022-11-12T10:00:00',
                                          to_time='2022-11-12T10:00:10',
                                          levels=10
                           )
    print(res.shape)
    assert not res is None


