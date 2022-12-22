import algohouse as ah


USER_EMAIL = 'tarasryb@gmail.com'
SIGNKEY = '9566c74d10037c4d7bbb0407d1e2c649'


def on_trade_fn(trade):
    print('>>> Got trade:\n', trade)


def on_order_fn(order):
    print('\n>>> Got order:\n', order.info())


def on_error_fn(error: Exception):
    # print(traceback.format_exc())
    print('>>> Got error: ', error)

def main():
    ah.get_stream(USER_EMAIL, SIGNKEY,
                  exchange='binance/f',
                  instrument='ETHUSDT',
                  # on_trade=on_trade_fn,
                  on_order=on_order_fn,
                  on_error=on_error_fn)


if __name__ == '__main__':
    main()
