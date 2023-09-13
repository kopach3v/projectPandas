import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

## ['Unix', 'Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume BTC','Volume USDT', 'tradecount']
df = pd.read_csv(r"C:\Users\Igor\PycharmProjects\projectPandas\venv\Binance_BTCUSDT_d.csv")
reverse_df = df[::-1].head(50)


def buy_sell(reverse_df):
    balance_usdt = 1000.0
    balance_btc = 0.0
    count_sell = 0
    count_buy = 0
    pnl = 0.0

    buy_wait_trades = []
    buy_sold_trades = []
    trades = []

    # previous_open_price = None
    for index, row in reverse_df.iterrows():
        # if previous_open_price is not None:
        if row.Open > row.Close:
            print(f"{row.Open}, Красная свеча")
            # Формула покупки Btc
            if balance_usdt > 0:
                buy_orders = {}
                amount_to_spend_usdt = min(balance_usdt, 100.0)
                amount_bought_btc = amount_to_spend_usdt / row.Open
                balance_btc += amount_bought_btc
                balance_usdt -= amount_to_spend_usdt

                buy_orders['side'] = 'BUY'
                buy_orders['time'] = row.Date
                buy_orders['price'] = row.Open
                buy_orders['amount'] = f'{amount_bought_btc:.6f}'
                buy_orders['qty'] = amount_to_spend_usdt
                buy_wait_trades.append(buy_orders)
                trades.append(buy_orders)
                count_buy += 1

                print(f"Куплено {amount_bought_btc:.4f} BTC по цене {row.Open} USDT")

        elif len(buy_wait_trades) >0 and buy_wait_trades[0]['price']  < row.Open  :
            print(f"{row.Open}, Зеленая свеча")
            if balance_btc > 0.00001:
                sell_orders = {}
                amount_to_spend_btc = balance_btc
                amount_bought_usdt = amount_to_spend_btc * row.Open
                balance_btc -= amount_to_spend_btc
                balance_usdt += amount_bought_usdt

                sell_orders['side'] = 'SELL'
                sell_orders['time'] = row.Date
                sell_orders['price'] = row.Open
                sell_orders['amount'] = f'{amount_to_spend_btc:.6f}'
                sell_orders['qty'] = f'{amount_bought_usdt:.2f}'
                trades.append(sell_orders)
                buy_sold_trades.append(buy_wait_trades[0])
                buy_wait_trades.pop(0)
                count_sell += 1

                print(f"Продано {amount_to_spend_btc:.4f} BTC по цене {row.Open} USDT")

    print(f'Usdt: {balance_usdt}, Btc:{balance_btc}, Продаж:{count_sell}, Покупок: {count_buy}, PNL: {pnl}, {trades}')
    print(f'В ожидании на продажу: {buy_wait_trades}, Продано: {buy_sold_trades}')

buy_sell(reverse_df)
# fig = go.Figure([go.Candlestick(x=reverse_df['Date'],
#                 open = reverse_df['Open'],
#                 high = reverse_df['High'],
#                 low=reverse_df['Low'],
#                 close = reverse_df['Close'])])
# fig.show()


# print(reverse_df.columns)
