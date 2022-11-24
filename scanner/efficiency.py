# import yfinance as yf
# import pandas as pd
# import talib
# import numpy as np
# from mpl_finance import candlestick_ohlc
# import matplotlib.dates as mpl_dates
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvasAgg
# from .models import *
# from io import StringIO


# def find_suppressed(day):
#     df=day
#     df['Date'] = pd.to_datetime(df.index)
#     df['Date'] = df['Date'].apply(mpl_dates.date2num)
#     df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
    
#     def isSupport(df,i):
#         support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
#         return support
#     def isResistance(df,i):
#         resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
#         return resistance
    
#     s =  np.mean(df['High'] - df['Low'])
    
#     def isFarFromLevel(l):
#         return np.sum([abs(l-x) < s  for x in levels]) == 0
    
#     levels = []
#     for i in range(2,df.shape[0]-2):
#         if isSupport(df,i):
#             l = df['Low'][i]
#             if isFarFromLevel(l):
#                 levels.append((i,l))
#         elif isResistance(df,i):
#             l = df['High'][i]
#             if isFarFromLevel(l):
#                 levels.append((i,l))
    
    
#     def plot_all():
#         fig, ax = plt.subplots()
#         candlestick_ohlc(ax,df.values,width=0.6, \
#                         colorup='green', colordown='red', alpha=0.8)
#         date_format = mpl_dates.DateFormatter('%d %b %Y')
#         ax.xaxis.set_major_formatter(date_format)
#         fig.autofmt_xdate()
#         fig.tight_layout()
#         fig.set_figwidth(15)
#         fig.set_figheight(5)
#         for level in levels:
#             plt.hlines(level[1],xmin=df['Date'][level[0]],\
#                     xmax=max(df['Date']),colors='blue')
#         from django.http import HttpResponse

#         imgdata = StringIO()
#         fig.savefig(imgdata, format='svg')
        
#         imgdata.seek(0)
#         data = imgdata.getvalue()
        
#         return data
#     da=plot_all() 
#     return da
    
# def stock_scanner(stock_list):
  
#     lst=[]
#     for i in stock_list:
#         minutes = yf.download(i,period="60d",interval="30m")
#         Hr = yf.download(i,period="70d",interval="1h")
#         day = yf.download(i,period="70d",interval="1d")


#         minutes['EMA_21']= talib.EMA(minutes['Close'],timeperiod=21) 
#         minutes['EMA_50']= talib.EMA(minutes['Close'],timeperiod=50)

#         Hr['EMA_21']= talib.EMA(Hr['Close'],timeperiod=21)
#         Hr['EMA_50']= talib.EMA(Hr['Close'],timeperiod=50)

#         day['EMA_21']= talib.EMA(day['Close'],timeperiod=21)
#         day['EMA_50']= talib.EMA(day['Close'],timeperiod=50)
#         day['macd'], day['macdsignal'], day['macdhist'] = talib.MACD(day['Close'], fastperiod=12, slowperiod=26, signalperiod=9)    

#         minutes['Trend'] = minutes['EMA_21'] > minutes['EMA_50']
#         Hr['Trend'] = Hr['EMA_21'] > Hr['EMA_50']
#         day['Trend'] = day['EMA_21'] > day['EMA_50']
#         day['macd_trend']=day['macd'] > day['macdsignal']
        
#         for k in range(day):
#             for j in range(minutes):
#                 if minutes['Trend'][j] == True and day['Trend'][j] == True and day['macd_trend'][j] == True:
                    
            
    
        
  
# # stock_scanner(

