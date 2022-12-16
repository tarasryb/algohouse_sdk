import multiprocessing as mp
from functools import partial
import pandas as pd
import numpy as np
import itertools
from ah_utils import df_chunk
import ah_settings


def normalize_orders_fn(df):
    result = []

    for index, row in df.iterrows():
        pq_pairs = row['delta'].split('|')
        for i, pq_pair in enumerate(pq_pairs):

            if pq_pair == '@': continue
            pq = pq_pair.split('@')
            try:
                q = float(pq[0])
                p = float(pq[1])
            except ValueError as e:
                # print('\n!!!ValueError exception ' + pq_pair)
                continue

            if row['bs'] == 'S':
                side = 'bid'
            else:
                side = 'ask'

            result.append({
                'ts': row['ts'],
                'side': side,
                'reset': row['reset'],
                'price': p,
                'amount': q
            })
    return result


def normalize_orders(df):
    result = []
    n = 1  # mp.cpu_count()
    p = mp.Pool(processes=n)
    df_list = df_chunk(df, n)
    result_map = p.map(partial(normalize_orders_fn), df_list)

    for rec in result_map:
        result = itertools.chain(result, rec)

    return pd.DataFrame.from_dict(result)


def build_md(df):
    df_bid = df.loc[df['side'] == 'bid']
    df_ask = df.loc[df['side'] == 'ask']

    p_min = df['price'].min()
    p_max = df['price'].max()
    p_mean = df['price'].mean()

    intervals = get_ranges(p_min, p_max, 20)
    # print(p_min, p_max, intervals)
    market_depth_list = []
    for interval in intervals:
        interval_df = df_group[(df_group.price >= interval['start']) & (df_group.price < interval['stop'])]
        # print(interval_df)
        market_depth_list.append({
            'start_p': interval['start'],
            'stop_p': interval['stop'],
            'amount': interval_df.amount.sum()}
        )
    market_depth = pd.DataFrame.from_records(market_depth_list)
    return market_depth

def process_order_group(order_g, exchange, instrument, side):
    # p_min = g[1]['price'].min()
    # p_max = g[1]['price'].max()
    # print(p_min, p_max)

    start_t = order_g[0]
    end_t = order_g[0] + ah_settings.ORDER_GROUP_SIZE
    # print('Market depth', start_t, end_t)

    df_in = inout.read_orders_db(exchange=exchange,
                                 instrument=instrument,
                                 side=side,
                                 reset=False,
                                 start_t=start_t,
                                 end_t=end_t
                                 )
    # print('*** group', order_g[0])
    df_in = normalize_orders(df_in)
    df_group = pd.concat([order_g[1], df_in])
    # df_res.info()

    p_min = df_group['price'].min()
    p_max = df_group['price'].max()

    intervals = get_ranges(p_min, p_max, 20)
    # print(p_min, p_max, intervals)
    market_depth_list = []
    for interval in intervals:
        interval_df = df_group[(df_group.price >= interval['start']) & (df_group.price < interval['stop'])]
        # print(interval_df)
        market_depth_list.append({
            'start_p': interval['start'],
            'stop_p': interval['stop'],
            'amount': interval_df.amount.sum()}
        )
    market_depth = pd.DataFrame.from_records(market_depth_list)
    # print(market_depth.to_csv())
    return market_depth
