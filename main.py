import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

## ['Unix', 'Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume BTC','Volume USDT', 'tradecount']
df = pd.read_csv(r"C:\Users\Igor\PycharmProjects\projectPandas\venv\Binance_BTCUSDT_d.csv")
reverse_df = df[::-1].head(30)


def buy_sell(reverse_df):
    balance_usdt = 1000.0
    balance_btc = 0.0
    count_sell = 0
    count_buy = 0

    pnl = 0.0
    amount_to_spend_usdt = 100

    buy_wait_trades = []
    buy_sold_trades = []
    trades = []
    buy_dates = []
    buy_prices = []
    sell_dates = []
    sell_prices = []
    sold_count_in1 = []

    fig = go.Figure([go.Candlestick(x=reverse_df['Date'],
                                    open=reverse_df['Open'],
                                    high=reverse_df['High'],
                                    low=reverse_df['Low'],
                                    close=reverse_df['Close'])])
    fig.update_layout(xaxis_rangeslider_visible=False)
    config = {'scrollZoom': True}

    # previous_open_price = None
    for index, row in reverse_df.iterrows():
        date, open, close, high, low = row.Date, row.Open, row.Close, row.High, row.Low
        if open > close:
            print(f"{open}, Красная свеча")
            # Формула покупки Btc
            if balance_usdt >= 100:
                buy_dict = {}

                amount_bought_btc = amount_to_spend_usdt / close
                balance_btc += amount_bought_btc
                balance_usdt -= amount_to_spend_usdt

                buy_dict['side'] = 'BUY'
                buy_dict['time'] = date
                buy_dict['price'] = close
                buy_dict['amount'] = f'{amount_bought_btc:.6f}'
                buy_dict['qty'] = amount_to_spend_usdt
                buy_wait_trades.append(buy_dict)
                trades.append(buy_dict)
                buy_dates.append(date)
                buy_prices.append(close)
                count_buy += 1

                print(f"Куплено {amount_bought_btc:.4f} BTC по цене {close} USDT, БАЛАНС: {balance_usdt},{balance_btc:.4f}")

        elif len(buy_wait_trades) > 0:
            print(f"{open}, Зеленая свеча")
            sold_count = 0

            # for item in buy_wait_trades:
            #     buy_price = item['price']
            sold_dicts = []
            for item in buy_wait_trades:
                if item['price'] < close and balance_btc > 0:
                    sell_dict = {}
                    amount_to_spend_btc = float(item['amount'])
                    amount_bought_usdt = amount_to_spend_btc * close
                    balance_btc -= amount_to_spend_btc
                    balance_usdt += amount_bought_usdt

                    sell_dict['side'] = 'SELL'
                    sell_dict['time'] = date
                    sell_dict['price'] = close
                    sell_dict['amount'] = f'{amount_to_spend_btc:.6f}'
                    sell_dict['qty'] = f'{amount_bought_usdt:.2f}'
                    trades.append(sell_dict)
                    buy_sold_trades.append(buy_wait_trades[0])
                    sold_dicts.append(item)
                    sell_dates.append(date)
                    sell_prices.append(close)
                    sold_count +=1
                    sold_count_in1.append(sold_count)
                    count_sell += 1
                    pnl = (close*amount_to_spend_btc)-(item['price']*amount_to_spend_btc)

                    print(f"Продано {item}, по цене: {close}, БАЛАНС: {balance_usdt},{balance_btc}")
                    # print(f"Продано {amount_to_spend_btc:.4f} BTC по цене {close} USDT")
            for items in sold_dicts:
                buy_wait_trades.remove(items)
    # print(f'Usdt: {balance_usdt}, Btc:{balance_btc}, Продаж:{count_sell}, Покупок: {count_buy}, PNL: {pnl}, {trades}')
    # print(f'В ожидании на продажу: {buy_wait_trades}, Продано: {buy_sold_trades}')
    fig.add_trace(go.Scatter(
        x=buy_dates,
        y=buy_prices,  # Выберите подходящую y-координату для маркеров покупки
        mode="markers",
        marker_symbol="triangle-up",  # Символ "▲" для покупок
        marker=dict(size=10, color="green"),
        name="Покупка"
    ))

    fig.add_trace(go.Scatter(
        x=sell_dates,
        y=sell_prices,  # Выберите подходящую y-координату для маркеров покупки
        mode="markers",
        marker_symbol="triangle-down",  # Символ "▲" для покупок
        marker=dict(size=10, color="red"),
        name=f"Продажа"
    ))
    # for i, x_date in enumerate(sell_dates):
    #     fig.add_trace(go.Scatter(
    #         x=[x_date],
    #         y=sell_prices,  # Определяем высоту текста над свечей
    #         mode='text',
    #         text=[f"{sold_count_in1[i]}"],
    #         showlegend=False
    #     ))

    fig.add_annotation(
        text=f'PNL: {pnl:.2f}$',
        xref="paper",
        yref="paper",
        x=0.95,
        y=0.05,
        showarrow=False,
        font=dict(size=12)
    )
    fig.show(config=config)
    print(pnl)

buy_sell(reverse_df)



# print(reverse_df.columns)
