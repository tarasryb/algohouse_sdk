import sys

import stream

sys.path.append("algohouse_sdk")

import pandas as pd
import reference_data
import trades
import orderbook
import options
import ah_connection as ahc

def get_reference_data(exchanges: list = None) -> pd.DataFrame:
    """

    :param exchanges: optional list of exchanges, in None, the function will return all of them
    :return: Pandas DataFrame with the columns: exchange (string), instruments (list of strings)
    """
    return reference_data.get_reference_data(exchanges)


def get_reference_data_v2(exchange: str = None,
                          instrument: str = None,
                          instrument2: str = None) -> pd.DataFrame:
    """

    :param exchange: optional exchange name, in None, the function will return all of them
    :param instrument: instrument name
    :param instrument2: second instrument name
    :return: Pandas DataFrame with the columns: exchange (string), instruments (list of strings)
    """
    return reference_data.get_reference_data_v2(exchange, instrument, instrument2)


def get_trades(connection: ahc.Connection,
               exchange: str, instrument: str,
               from_time: str, to_time: str) -> pd.DataFrame:
    """

    Get trades historical data
    :param connection: Algohouse Connection object
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data
    :param to_time: end time of the requested data
    :return: Pandas DataFrame with the columns: ts, bs (B, S), price, volume
    """
    return trades.get_trades(connection,
                             exchange, instrument,
                             from_time, to_time)


def get_trades_aggregated(connection: ahc.Connection,
                          exchange: str, instrument: str,
                          from_time: str, to_time: str,
                          aggregation: str = '1m') -> pd.DataFrame:
    """

    Get aggregated trades
    :param connection: Algohouse Connection object
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data
    :param to_time: end time of the requested data
    :param aggregation: the type of the aggregation (1m, 15m, 1h, 1d)
    :return: Pandas DataFrame with the columns: ts, open, high, low, close, volume, rec_count, avg_price
    """
    return trades.get_trades_aggregated(connection,
                                        exchange, instrument,
                                        from_time, to_time,
                                        aggregation)


def reset_orderbook_cache():
    """
    Reset order book cache
    """
    orderbook.exchange_cached = None
    orderbook.instrument_cached = None
    orderbook.df_n_cached = None


def get_orderbook(connection: ahc.Connection,
                  exchange: str, instrument: str,
                  from_time: str,
                  levels: int = None,
                  snapshot=False) -> dict:
    """
    Get orderbook records
    :param connection: Algohouse Connection object
    :param exchange: exchange name
    :param instrument: instrument name
    :param from_time: start time of the requested data (the number of orders to read appointed in ah_settings.ORDERS_TO_READ)
    :param levels: number of levels in Market Depth, if 0 or None, return RAW md
    :param snapshot: if True, returns the dictionary with "snapshot" key which contains DataFrame with "ts, side, reset, price, size" columns

    :return: (see "snapshot" parameter), if False, returns the Dictionary which contains two keys: "bid" and "ask". Each key contains Pandas DataFrame with the columns: price, size
    """
    return orderbook.get_orderbook(connection,
                                   exchange, instrument,
                                   from_time,
                                   levels, snapshot)


def get_stream(connection: ahc.Connection,
               exchange: str, instrument: str,
               on_trade=None, on_order=None, on_error=None
               ):
    """
    Subscribe to AlgoHouse streaming data
    :param connection: Algohouse Connection object
    :param exchange: exchange name
    :param instrument: instrument name
    :param on_trade: on get trades callback, use DataFrame parameter as get_trades function
    :param on_order: on get orders callback, use DataFrame parameter as get_orderbook function
    :param on_error: error callback
    :return:
    """
    return stream.get_stream(connection,
                             exchange, instrument,
                             on_trade, on_order, on_error
                             )


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
    return options.get_options(connection,
                               exchange, instrument,
                               from_time, to_time)
