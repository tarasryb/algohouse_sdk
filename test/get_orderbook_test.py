import datetime
import pandas as pd

import algohouse as ah
import ah_settings as ahs

USER_EMAIL = 'tarasryb@gmail.com'
SIGNKEY = '9566c74d10037c4d7bbb0407d1e2c649'
# USER_EMAIL = 'vyklyuk@ukr.net'
# SIGNKEY = '81855ad8681d0d86d1e91e00167939cb'


def _test_get_orderbook():
    ahs.DOMAIN = 'http://127.0.0.1:5000'
    res = ah.get_orderbook(USER_EMAIL, SIGNKEY,
                                          exchange='tiny',  # 'binance/f',  # 'lbank',  # 'binance',  # 'binance/f',
                                          instrument='1000LUNCBUSD',  # 'APEBUSD',  # 'BTS_USDT',  # 'BTCB_USD',  # '1000LUNCBUSD',
                                          from_time='2022-11-12T10:00:00',
                                          to_time='2022-11-12T10:05:00',
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


def test_get_cached_orderbook():
    ahs.DOMAIN = 'http://127.0.0.1:5000'
    res = ah.get_orderbook(USER_EMAIL, SIGNKEY,
                                          exchange='small',  # 'binance/f',  # 'lbank',  # 'binance',  # 'binance/f',
                                          instrument='1000LUNCBUSD',  # 'APEBUSD',  # 'BTS_USDT',  # 'BTCB_USD',  # '1000LUNCBUSD',
                                          from_time='2022-11-12T10:00:00',
                                          levels=None
                           )
    print(len(res['bid']))
    print(len(res['ask']))

    ahs.ORDER_LINES_TO_READ = 1000
    res = ah.get_orderbook(USER_EMAIL, SIGNKEY,
                                          exchange='binance/f', #'big,small, tiny'  # 'binance/f',  # 'lbank',  # 'binance',  # 'binance/f',
                                          instrument='1000LUNCBUSD',  # 'APEBUSD',  # 'BTS_USDT',  # 'BTCB_USD',  # '1000LUNCBUSD',
                                          from_time='2022-11-12T10:00:00',
                                          levels=10
                           )
    print(len(res['bid']))
    print(len(res['ask']))
    assert not res is None




def _test_get_orderbook_md():
    res = ah.get_orderbook_md(USER_EMAIL, SIGNKEY,
                                          exchange='binance/f',  # 'lbank',  # 'binance',  # 'binance/f',
                                          instrument='BTCBUSD',  # 'BTS_USDT',  # 'BTCB_USD',  # '1000LUNCBUSD',
                                          from_time='2022-11-12T10:00:00',
                                          to_time='2022-11-12T10:00:10',
                                          levels=10
                           )
    print(res.shape)
    assert not res is None


