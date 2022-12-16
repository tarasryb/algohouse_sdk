import pandas as pd

import ah_utils as ahu


def test_ssl():
    key = "9566c74d10037c4d7bbb0407d1e2c649"
    q = "/trades_aggregated?ins=1000LUNCBUSD&ex=binance/f&from=2020-01-01T00:00:00&to=2022-12-07T23:00:00&aggregation=1m&signerEmail=tarasryb@gmail.com&requestTimestamp=1670846172000"
    res = ahu.signature(key, q)
    assert res == 'd063e03c80b7ed1f20707cab8e2ce89b5eb2b16fb848b9b25c03b8702add0342'


def test_df_chunk():
    n = 3
    df = pd.DataFrame([
        {"n": 1, "t": "a1"},
        {"n": 2, "t": "a2"},
        {"n": 3, "t": "a3"},
        {"n": 4, "t": "a4"},
        {"n": 5, "t": "a5"},
        {"n": 6, "t": "a6"},
        {"n": 7, "t": "a7"},
        {"n": 8, "t": "a8"},
        {"n": 9, "t": "a9"},
        {"n": 10, "t": "a10"},
        {"n": 11, "t": "a11"},
    ])
    res = ahu.df_chunk(df, n)
    # print(res)
    assert len(res) == 3


