import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def take_price_data(ticker, interval, period):
    ticker = ticker
    interval = interval
    period= period
    x = yf.download(tickers= ticker,
                interval= interval,
                period=period).dropna()
    #statistiche
    x['avgprice'] = (x.Open + x.High + x.Low + x.Close) / 4
    x['medprice'] = x.Open - (x.High - x.Low) /2
    x['medbody_price'] = x.Open - abs(x.Close - x.Open)/2
    x['body'] = x.Close - x.Open
    x['range'] = x.High - x.Low
    x['sma_50'] = x.Close.rolling(50).mean()
    return x
    pass

#input
variazione= 0 #variazione percentuale richiesta
money = 10000  #soldi per operazione

#pass into percentage
x = take_price_data('AAPL', '1h', '1y').copy().dropna()
s = take_price_data('AAPL', '1h', '1y').copy().pct_change().dropna() * 100

#aggiunta parametri basilari
strategy = s.copy().iloc[:, :-3]
strategy.drop(['Adj Close', 'Volume'], axis= 1,inplace = True)
strategy.columns = ['dopen', 'dhigh', 'dlow', 'dclose', 'daveragep', 'dmedp', 'dmedbody_p']
strategy['open'] = x.Open
strategy['close'] = x.Close
strategy['high'] = x.High
strategy['low'] = x.Low
strategy['avgprice'] = x.avgprice
strategy['sma_100'] = strategy.close.rolling(100).mean()
#strategia
strategy['stocks']= money/ strategy.open
strategy['positions'] = np.where((abs(strategy.dclose.shift(1)) >= variazione) &
                                 (strategy.close.shift(1) < strategy.close.shift(2)) &
                                  (strategy.close < strategy.sma_100),1,0)
strategy['entry'] = strategy.open
strategy['exit'] = strategy.close
strategy['trade'] = -(strategy.exit - strategy.open) * strategy.stocks
strategy['gain'] = strategy.trade * strategy.positions
strategy['equity'] = strategy.gain.cumsum()

#sostituiamo i numeri nulli del gain
strategy['gain'] = np.where(strategy.gain !=0, strategy['gain'], np.nan)

#scartiamo il primo valore
strategy = strategy[1:]

#output strategia
successo = strategy.gain > 0
percentuale_di_successo = (successo.count()/strategy.gain.sum()) * 100
net_profit = strategy.equity[-1]
corrispondente = round((net_profit * 100) / money,2)
print('la percentuale di successo di questa strategia è: ', percentuale_di_successo,'%',   '\nil net profit di questa strategia è: ',
net_profit,'$', ' corrispondente al ', corrispondente, '%',' del capitale di parenza' )

#output grafico
plt.plot(z.equity)
plt.show()
