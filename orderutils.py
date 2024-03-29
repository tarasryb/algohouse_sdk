import multiprocessing as mp
from functools import partial
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import itertools
from ah_utils import df_chunk
import ah_settings as ahs


def normalize_orders_fn(df):
    result = []
    for index, row in df.iterrows():
        row_ts = row['ts']
        if str(row['delta']) == 'nan': continue
        
        pq_pairs = row['delta'].split('|')
        for i, pq_pair in enumerate(pq_pairs):

            if pq_pair == '@': continue
            pq = pq_pair.split('@')
            if len(pq) < 2:
                # chunk like "+432"
                try:
                    delta_ms = int(pq[0])
                except ValueError as e:
                    delta_ms = 0
                    print('\n!!!ValueError exception (delta_ms) ' + pq[0])

                row_ts = row['ts'] + timedelta(milliseconds=delta_ms)
                continue
            try:
                q = float(pq[0])
                p = float(pq[1])
            except ValueError as e:
                print('\n!!!ValueError exception (pq pair) ' + pq_pair)
                continue

            if row['bs'] == 'S':
                side = 'ask'
            else:
                side = 'bid'

            result.append({
                'ts': row_ts,
                'side': side,
                'reset': row['reset'],
                'price': p,
                'size': q
            })
    return result


def normalize_orders(df):
    result = []
    n = mp.cpu_count()
    p = mp.Pool(processes=n)
    df_list = df_chunk(df, n)
    result_map = p.map(partial(normalize_orders_fn), df_list)

    for rec in result_map:
        result = itertools.chain(result, rec)

    return pd.DataFrame.from_dict(result)


def normalize_orders_single_core(df):
    result_list = normalize_orders_fn(df)
    return pd.DataFrame.from_records(result_list)


def filter_by_price(df):
    df_q = df.price.quantile(ahs.FILTER_BAD_PRICES_QUANTILE)
    df_min = df_q - (df_q * ahs.FILTER_BAD_PRICES_RATIO)
    df_max = df_q + (df_q * ahs.FILTER_BAD_PRICES_RATIO)
    df_filtered = df[(df.price >= df_min) & (df.price <= df_max)]
    return df_filtered


def build_raw_md(df, for_time):
    for_time_dt = datetime.strptime(for_time, ahs.DATETIME_FORMAT)
    md = {}
    prev_reset = False
    reset_count = 0

    for index, row in df.iterrows():
        ts = row['ts']

        reset = not row['reset'] is None
        if reset & (not prev_reset):
            md = {}
            reset_count += 1

        prev_reset = reset

        if ts > for_time_dt:
            return md

        p = row['price']
        a = row['size']

        if a == 0:
            if not p in md.keys():
                # print('!!! Error, no key on delete position:' + str(p))
                pass
            else:
                md.pop(p)
        else:
            md[p] = a

    return md


def build_raw_md_for_side(df, side, for_time):
    df_side = df.loc[df['side'] == side]

    if ahs.FILTER_BAD_PRICES:
        df_side_filtered = filter_by_price(df_side)
    else:
        df_side_filtered = df_side

    side_raw_md = build_raw_md(df_side_filtered, for_time)
    side_raw_md_df = pd.DataFrame({'price': side_raw_md.keys(), 'size': side_raw_md.values()})
    return side_raw_md_df.sort_values(by=['price'])


def get_ranges(p_min, p_max, chunks):
    step = (p_max - p_min) / (chunks)
    points = np.arange(p_min, p_max, step).tolist()
    points.append(p_max)
    intervals = []
    for i, rec in enumerate(points):
        if i >= len(points)-1: break
        intervals.append({'start': rec, 'stop': points[i + 1]})
    return intervals


def build_md_for_side(df, levels):
    p_min = df['price'].min()
    p_max = df['price'].max()
    intervals = get_ranges(p_min, p_max, levels)
    market_depth_list = []
    for interval in intervals:
        interval_df = df[(df.price >= interval['start']) & (df.price < interval['stop'])]
        market_depth_list.append({
            'price': interval['start'],
            # 'stop_p': interval['stop'],
            'size': interval_df.size.sum()}
        )
    market_depth = pd.DataFrame.from_records(market_depth_list)

    return market_depth


def build_md(df, for_time, levels: int):
    if df.empty:
        return {"bid": pd.DataFrame(), "ask": pd.DataFrame()}

    bid_raw_md = build_raw_md_for_side(df, 'bid', for_time)
    ask_raw_md = build_raw_md_for_side(df, 'ask', for_time)

    if (levels is None) or (levels == 0):
        return {"bid": bid_raw_md, "ask": ask_raw_md}
    else:
        bid_md = build_md_for_side(bid_raw_md, levels)
        ask_md = build_md_for_side(ask_raw_md, levels)
        return {"bid": bid_md, "ask": ask_md}


def build_md_classic_for_side(md):
    size = 0
    md_c = []
    for index, row in md.iterrows():

        if not index == 0:
            size = size + row['size']

        md_c.append({"price": row['price'],
                     "size": size})

    md_c_df = pd.DataFrame.from_records(md_c)
    return md_c_df


def build_md_classic(md):
    bid_df = md['bid']
    if bid_df.empty:
        bid_md_c = pd.DataFrame()
    else:
        bid_df = bid_df.sort_values(by=['price'], ascending=False, ignore_index=True)
        bid_md_c = build_md_classic_for_side(bid_df)
        bid_md_c = bid_md_c.sort_values(by=['price'], ignore_index=True)

    ask_df = md['ask']
    if ask_df.empty:
        ask_md_c = pd.DataFrame()
    else:
        ask_df = ask_df.sort_values(by=['price'], ignore_index=True)
        ask_md_c = build_md_classic_for_side(ask_df)

    return {"bid": bid_md_c, "ask": ask_md_c}

