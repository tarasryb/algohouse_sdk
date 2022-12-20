import sys

sys.path.append("algohouse_sdk")

import pandas as pd
import reference_data
import trades
import orderbook


def get_reference_data(exchanges: list = None) -> pd.DataFrame:
    """

    :param exchanges: optional list of exchanges, in None, the function will return all of them
    :return: Pandas DataFrame with the columns: exchange (string), instruments (list of strings)
    """
    return reference_data.get_reference_data(exchanges)


def get_trades(user_email: str, signkey: str,
               exchange: str, instrument: str,
               from_time: str, to_time: str) -> pd.DataFrame:
    """

    Get trades historical data
    :param user_email: e-mail of the Algohouse user who registered as API user
    :param signkey: the key to sign the request
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data
    :param to_time: end time of the requested data
    :return: Pandas DataFrame with the columns: ts, open, high, low, close, volume, rec_count, avg_price
    """
    return trades.get_trades(user_email, signkey,
                             exchange, instrument,
                             from_time, to_time)


def get_trades_aggregated(user_email: str, signkey: str,
                          exchange: str, instrument: str,
                          from_time: str, to_time: str,
                          aggregation: str = '1m') -> pd.DataFrame:
    """

    Get aggregated trades
    :param user_email: e-mail of the Algohouse user who registered as API user
    :param signkey: the key to sign the request
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data
    :param to_time: end time of the requested data
    :param aggregation: the type of the aggregation (1m, 15m, 1h, 1d)
    :return: Pandas DataFrame with the columns: ts, open, high, low, close, volume, rec_count, avg_price
    """
    return trades.get_trades_aggregated(user_email, signkey,
                                        exchange, instrument,
                                        from_time, to_time,
                                        aggregation)


def get_orderbook(user_email: str, signkey: str,
                  exchange: str, instrument: str,
                  from_time: str,
                  levels: int,
                  snapshot=False) -> dict:
    """

    Get orderbook records
    :param user_email: e-mail of the Algohouse user who registered as API user
    :param signkey: the key to sign the request
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data (the number of orders to read appointed in ah_settings.ORDERS_TO_READ)
    :param levels: number of levels in Market Depth, if 0 or None, return RAW md
    :param snapshot: if True, returns the dictionary with "snapshot" key which contains DataFrame with "ts, side, reset, price, size" columns

    :return: (see "snapshot" parameter), if False, returns the Dictionary which contains two keys: "bid" and "ask". Each key contains Pandas DataFrame with the columns: price, size
    """
    return orderbook.get_orderbook(user_email, signkey,
                                   exchange, instrument,
                                   from_time,
                                   levels, snapshot)
