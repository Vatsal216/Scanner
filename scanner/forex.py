import yfinance as yf
import pandas as pd
import talib
import numpy as np
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from .models import *
from io import StringIO
import MetaTrader5 as mt5
import pytz
from .order import *

def stock_mt():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    return mt5


def forex_scanner(forex_list):

    lst = []
    for i in forex_list:

        mt5 = stock_mt()
        timezone = pytz.timezone("Etc/UTC")
        minutes = mt5.copy_rates_from_pos(i, mt5.TIMEFRAME_M30, 0, 100)
        minutes = pd.DataFrame(minutes)

        Hr = mt5.copy_rates_from_pos(i, mt5.TIMEFRAME_H4, 0, 100)
        Hr = pd.DataFrame(Hr)

        day = mt5.copy_rates_from_pos(i, mt5.TIMEFRAME_D1, 0, 100)
        day = pd.DataFrame(day)

        weeklo = mt5.copy_rates_from_pos(i, mt5.TIMEFRAME_W1, 0, 100)
        weeklo = pd.DataFrame(weeklo)

        minutes['time'] = pd.to_datetime(minutes['time'], unit='s')

        minutes['EMA_21'] = talib.EMA(minutes['close'], timeperiod=21)
        minutes['EMA_50'] = talib.EMA(minutes['close'], timeperiod=50)

        Hr['time'] = pd.to_datetime(Hr['time'], unit='s')
        Hr['EMA_21'] = talib.EMA(Hr['close'], timeperiod=21)
        Hr['EMA_50'] = talib.EMA(Hr['close'], timeperiod=50)
        Hr['macd'], Hr['macdsignal'], Hr['macdhist'] = talib.MACD(
            Hr['close'], fastperiod=12, slowperiod=26, signalperiod=9)

        day['time'] = pd.to_datetime(day['time'], unit='s')
        day['EMA_21'] = talib.EMA(day['close'], timeperiod=21)
        day['EMA_50'] = talib.EMA(day['close'], timeperiod=50)
        day['macd'], day['macdsignal'], day['macdhist'] = talib.MACD(
            day['close'], fastperiod=12, slowperiod=26, signalperiod=9)

        weeklo['time'] = pd.to_datetime(weeklo['time'], unit='s')
        weeklo['EMA_21'] = talib.EMA(weeklo['close'], timeperiod=21)
        weeklo['EMA_50'] = talib.EMA(weeklo['close'], timeperiod=50)
        weeklo['macd'], weeklo['macdsignal'], weeklo['macdhist'] = talib.MACD(
            weeklo['close'], fastperiod=12, slowperiod=26, signalperiod=9)

        minutes['Trend'] = minutes['EMA_21'] > minutes['EMA_50']
        minutes.set_index('time', inplace=True)

        Hr['Trend'] = Hr['EMA_21'] > Hr['EMA_50']
        Hr['macd_trend'] = Hr['macd'] > Hr['macdsignal']
        Hr.set_index('time', inplace=True)

        day['Trend'] = day['EMA_21'] > day['EMA_50']
        day['macd_trend'] = day['macd'] > day['macdsignal']
        day.set_index('time', inplace=True)
       
        weeklo['Trend'] = weeklo['EMA_21'] > weeklo['EMA_50']
        weeklo['macd_trend'] = weeklo['macd'] > weeklo['macdsignal']
        weeklo.set_index('time', inplace=True)

        minuts = minutes.tail(200)[::-1]
        day_time = day.tail(1500)[::-1]
  
        minu = minutes.tail(1)
        Trend_last = ''


        for j in range(len(minuts)):
            # print(minu['Trend'][0], minuts.iloc[j, 8])
           
            if minu['Trend'][0] == minuts.iloc[j, 9]:
                # print(minutes['Trend'][j], minu['Trend'][0],minutes['date_lasta'][j] )
                pass
            elif minu['Trend'][0] != minuts.iloc[j, 9]:
                Trend_last = minuts.index.values[j-1]
                break
        Trend_last_dya = ''

        for j in range(len(day_time)):
            # print(minu['Trend'][0], minuts.iloc[j, 8])
            if day_time['Trend'][0] == day_time.iloc[j, 12]:
                # print(minutes['Trend'][j], minu['Trend'][0],minutes['date_lasta'][j] )
                pass
            elif day_time['Trend'][0] != day_time.iloc[j, 12]:
                Trend_last_dya = day_time.index.values[j-1]

                break

        day = day.tail(1)
        minutes = minutes.tail(2)

        Hr = Hr.tail(1)

        weeklo = weeklo.tail(2)

        minutes['1_day_trend'] = day['Trend'][0]
        minutes['1_hr_trend'] = Hr['macd_trend'][0]
        minutes['1_day_macd_trend'] = day['macd_trend'][0]
        minutes['1_weekly_trend'] = weeklo['Trend'][0]
        minutes['1_weekly_macd_trend'] = weeklo['macd_trend'][0]
        # minutes['date']=minutes.index.values[1]
        minutes['name'] = i

        if minutes['Trend'][1] == True and minutes['Trend'][0] == False:
            # Performance_Stock.objects.filter(name=i).update(signal= minutes['Trend'][1],name=i,close=minutes['close'][1])

            if minutes['Trend'][1] == True and minutes['1_hr_trend'][1] == True and minutes['1_day_macd_trend'][1] == True and minutes['1_day_trend'][1] == True and minutes['1_weekly_trend'][1] == True and minutes['1_weekly_macd_trend'][1] == True:
                minutes['Signla'] = 'Strong Buy'
                Buy_executed_order(i,700,380)
            elif minutes['Trend'][1] == False and minutes['1_hr_trend'][1] == False and minutes['1_day_macd_trend'][1] == False and minutes['1_day_trend'][1] == False and minutes['1_weekly_trend'][1] == False and minutes['1_weekly_macd_trend'][1] == False:
                minutes['Signla'] = 'Strong Sell'
                Sell_executed_order(i,700,380)
            elif minutes['Trend'][1] == False and minutes['1_hr_trend'][1] == False and minutes['1_day_macd_trend'][1] == False   and minutes['1_weekly_macd_trend'][1] == False:
                minutes['Signla'] = 'Strong Sell'
                Sell_executed_order(i,1000,500)
            elif minutes['Trend'][1] == True and minutes['1_hr_trend'][1] == True and minutes['1_day_macd_trend'][1] == True   and minutes['1_weekly_macd_trend'][1] == True:
                minutes['Signla'] = 'Strong Buy'
                Buy_executed_order(i,1000,500)
                  
            elif minutes['Trend'][1] == True and minutes['1_day_macd_trend'][1] == True and minutes['1_day_trend'][1] == True:
                minutes['Signla'] = 'Buy'
                Buy_executed_order(i,600,350)
            elif minutes['Trend'][1] == False and minutes['1_day_macd_trend'][1] == False and minutes['1_day_trend'][1] == False:
                minutes['Signla'] = 'Sell'
                Sell_executed_order(i,600,350)
            elif minutes['Trend'][1] == True and minutes['1_hr_trend'][1] == True:
                minutes['Signla'] = 'Buy'
                Buy_executed_order(i,500,350)
            elif minutes['Trend'][1] == False and minutes['1_hr_trend'][1] == False:
                minutes['Signla'] = 'Sell'
                Sell_executed_order(i,500,350)
          
            else:
                minutes['Signla'] = 'Wait'
            minutes['Trend'] = str(minutes['Trend'][1]) + ' ' + '(Now)'
            
            
        else:
            # stcok_data=Performance_Stock.objects.get(name=i)

            if minutes['Trend'][1] == True and minutes['1_hr_trend'][1] == True and minutes['1_day_macd_trend'][1] == True and minutes['1_day_trend'][1] == True and minutes['1_weekly_trend'][1] == True and minutes['1_weekly_macd_trend'][1] == True:
                minutes['Signla'] = 'Strong Buy'
            if minutes['Trend'][1] == False and minutes['1_hr_trend'][1] == False and minutes['1_day_macd_trend'][1] == False and minutes['1_day_trend'][1] == False and minutes['1_weekly_trend'][1] == False and minutes['1_weekly_macd_trend'][1] == False:
                minutes['Signla'] = 'Strong Sell'
            elif minutes['Trend'][1] == True and minutes['1_day_macd_trend'][1] == True and minutes['1_day_trend'][1] == True:
                minutes['Signla'] = 'Buy'
            elif minutes['Trend'][1] == False and minutes['1_day_macd_trend'][1] == False and minutes['1_day_trend'][1] == False:
                minutes['Signla'] = 'Sell'
            elif minutes['Trend'][1] == True and minutes['1_hr_trend'][1] == True:
                minutes['Signla'] = 'Buy'
            elif minutes['Trend'][1] == False and minutes['1_hr_trend'][1] == False:
                minutes['Signla'] = 'Sell'
          
            else:
                minutes['Signla'] = 'Wait'

            Trend_last = str(Trend_last)
            Trend_last = Trend_last.replace("T", " ")
            Trend_last = Trend_last.split(".", 1)[0]

            minutes['Trend'] = str(minutes['Trend'][1])+'   '+str(Trend_last)
            Trend_last_dya = str(Trend_last_dya)
            Trend_last_dya = Trend_last_dya.replace("T", " ")
            Trend_last_dya = Trend_last_dya.split(" ", 1)[0]
            minutes['1_day_trend'] = str(
                minutes['1_day_trend'][1])+'   '+str(Trend_last_dya)
            minutes['close'] = int(minutes['close'][1])

        minutes = minutes.to_dict('records')[1]
        lst.append(minutes)

    if len(forex_list) == 1:
        return lst
    else:
        return lst
