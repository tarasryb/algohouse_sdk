import datetime
import pandas as pd

import algohouse as ah


def test_get_info():
    res = ah.get_reference_data()
    # print(res)
    assert not res is None


def test_get_info_2():
    res = ah.get_reference_data(['bitfinex/d', 'binance/f'])
    # print(res)
    assert not res is None


