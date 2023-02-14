import datetime

import algohouse as ah
import ah_connection as ahc


USER_EMAIL = 'intern@intela.io'
SIGNKEY = '7c45593ac289db2a1d37e6a0387bbd18'


def on_trade_fn(trade):
    print('>>> Got trade:\n', trade)


order_callback_count = 0


def on_order_fn(orders):
    global order_callback_count
    print('\n>>> Got orders:\n', order_callback_count, datetime.datetime.now(), len(orders.index))
    order_callback_count += 1


def on_error_fn(error: Exception):
    # print(traceback.format_exc())
    print('>>> Got error: ', error)


def main():
    conn = ahc.Connection(USER_EMAIL, SIGNKEY)
    ah.get_stream(conn,
                  exchange='bitfinex', #'binance',
                  instrument='BTCUSD', #'ETHUSDT',
                  on_trade=on_trade_fn,
                  on_order=on_order_fn,
                  on_error=on_error_fn)


if __name__ == '__main__':
    main()
