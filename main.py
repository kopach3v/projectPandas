import pandas as pd
import plotly.graph_objs as go
from datetime import datetime




## ['Unix', 'Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume BTC','Volume USDT', 'tradecount']
df = pd.read_csv(r"C:\Users\Igor\PycharmProjects\projectPandas\venv\Binance_BTCUSDT_d.csv")
reverse_df = df[::-1].head(200)



def buy_sell(reverse_df):
    balance_usdt = 1000.0
    balance_btc = 0.0
    count_sell = 0
    count_buy = 0
    pnl = 0.0
    previous_open_price = None
    for index, row in reverse_df.iterrows():
        if previous_open_price is not None:
            if row.Open > previous_open_price:
                print(f"{row.Open}, Зеленая свеча")
                if balance_btc > 0.00001:
                    amount_to_spend_btc = balance_btc * 0.3
                    amount_bought_usdt = amount_to_spend_btc * row.Open
                    balance_btc -= amount_to_spend_btc
                    balance_usdt += amount_bought_usdt
                    count_sell += 1

                    print(f"Продано {amount_to_spend_btc:.4f} BTC по цене {row.Open} USDT")

            else:
                print(f"{row.Open}, Красная свеча")
                #Формула покупки Btc
                if balance_usdt > 0:

                    amount_to_spend_usdt = min(balance_usdt, 100.0)
                    amount_bought_btc = amount_to_spend_usdt / row.Open
                    balance_btc += amount_bought_btc
                    balance_usdt -= amount_to_spend_usdt
                    count_buy += 1

                    print(f"Куплено {amount_bought_btc:.4f} BTC по цене {row.Open} USDT")

        previous_open_price = row.Open

    print(f'Usdt: {balance_usdt}, Btc:{balance_btc}, Продаж:{count_sell}, Покупок: {count_buy}, PNL: {pnl}')
buy_sell(reverse_df)
# fig = go.Figure([go.Candlestick(x=reverse_df['Date'],
#                 open = reverse_df['Open'],
#                 high = reverse_df['High'],
#                 low=reverse_df['Low'],
#                 close = reverse_df['Close'])])
# fig.show()


# print(reverse_df.columns)
