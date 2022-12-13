import datetime
import pandas as pd

import algohouse as ah

USER_EMAIL = 'tarasryb@gmail.com'
SIGNKEY = '9566c74d10037c4d7bbb0407d1e2c649'
# USER_EMAIL = 'vyklyuk@ukr.net'
# SIGNKEY = '81855ad8681d0d86d1e91e00167939cb'


def test_get_trades_aggregated():
    res = ah.get_trades_aggregated(USER_EMAIL, SIGNKEY,
                                          instrument='1000LUNCBUSD',
                                          exchange='binance/f',
                                          from_time='2022-11-12T00:00:00',
                                          to_time='2022-11-20T23:00:00',
                                          aggregation='1m')
    print(res)
    assert not res is None


def test_get_trades():
    res = ah.get_trades(USER_EMAIL, SIGNKEY,
                                          instrument='1000LUNCBUSD',
                                          exchange='binance/f',
                                          from_time='2022-11-12T00:00:00',
                                          to_time='2022-11-20T23:00:00')
    print(res)
    assert not res is None


def test_ssl():
    key = "9566c74d10037c4d7bbb0407d1e2c649"
    q = "/trades_aggregated?ins=1000LUNCBUSD&ex=binance/f&from=2020-01-01T00:00:00&to=2022-12-07T23:00:00&aggregation=1m&signerEmail=tarasryb@gmail.com&requestTimestamp=1670846172000"
    res = ah.signature(key, q)
    assert res == 'd063e03c80b7ed1f20707cab8e2ce89b5eb2b16fb848b9b25c03b8702add0342'

