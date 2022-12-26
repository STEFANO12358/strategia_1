import seaborn as sns
import pandas as pd
import yfinance as yf


#heatmap della correlazione delle close
def take_price(ticker, interval, period):
    ticker = ticker
    interval = interval
    period= period
    x = yf.download(tickers= ticker,
                interval= interval,
                period=period).dropna()

    return x
    pass

z = take_price('AAPL', '1d', '3y').pct_change().dropna() * 100

z = z.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1)
periodi = 10
for i in range(1, periodi+1):
    nome_colonna = 'Close_' + str(i)
    z[nome_colonna] = z.Close.shift(i)
z.dropna(inplace= True)
plt.figure(figsize=(8,6),dpi=110)
sns.heatmap(z.corr(), cmap='RdYlGn', linecolor='White', linewidth=0.1, annot=True)
