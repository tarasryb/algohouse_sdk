import pandas as pd
import hashlib
import hmac


def signature(key, msg):
    key = key.encode('ascii')
    msg = msg.encode()
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def df_chunk(df: pd.DataFrame, n: int) -> list:
    """
    Splits DataFrame to n chunks

    :param df: DataFrame to split
    :param n: number of chunks to split
    :return: list of DataFrames
    """
    chunk_size = df.shape[0] // n + 1
    list_df = [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]
    return list_df
