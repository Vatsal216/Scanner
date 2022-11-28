import yfinance as yf
import pandas as pd
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
import pandas_ta as ta
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
        minutes['Trend'] = minutes.ta.ema(21, append=True) > minutes.ta.ema(50, append=True)
        

        Hr['time'] = pd.to_datetime(Hr['time'], unit='s')
        Hr['Trend'] = Hr.ta.ema(21, append=True) > Hr.ta.ema(50, append=True)
        Hr.ta.macd(close=weeklo['close'], fast=12, slow=26, signal=9, append=True)
        Hr['macd_trend'] = Hr['MACD_12_26_9'] > Hr['MACDs_12_26_9']
        
    

        day['time'] = pd.to_datetime(day['time'], unit='s')
        day['Trend'] = day.ta.ema(21, append=True) > day.ta.ema(50, append=True)
        day.ta.macd(close=weeklo['close'], fast=12, slow=26, signal=9, append=True)
        day['macd_trend'] = day['MACD_12_26_9'] > day['MACDs_12_26_9']

        weeklo['time'] = pd.to_datetime(weeklo['time'], unit='s')
        weeklo['Trend'] = weeklo.ta.ema(21, append=True) > weeklo.ta.ema(50, append=True)
        weeklo.ta.macd(close=weeklo['close'], fast=12, slow=26, signal=9, append=True)
        weeklo['macd_trend'] = weeklo['MACD_12_26_9'] > weeklo['MACDs_12_26_9']

      
        minutes.set_index('time', inplace=True)

        
        Hr.set_index('time', inplace=True)

     
        day.set_index('time', inplace=True)
       
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

            if (minutes['Trend'][1] == True or minutes['close'][1] > minutes['EMA_21'][1]) and minutes['1_hr_trend'][1] == True  and minutes['1_day_macd_trend'][1] == True and minutes['1_day_trend'][1] == True and minutes['1_weekly_trend'][1] == True and minutes['1_weekly_macd_trend'][1] == True:
                minutes['Signla'] = 'Strong Buy'
                Buy_executed_order(i,700,380)
                Forex_order.objects.create(Forexname=i,minutes=minutes['Trend'][1],hours_macd=minutes['1_hr_trend'][1],day_ema=minutes['1_day_trend'][1],day_macd=minutes['1_day_macd_trend'][1],weekly_ema=minutes['1_weekly_trend'][1],weekly_macd=minutes['1_weekly_macd_trend'][1])
           
            elif (minutes['Trend'][1] == False or minutes['close'][1] < minutes['EMA_21'][1]) and minutes['1_hr_trend'][1] == False and minutes['1_day_macd_trend'][1] == False and minutes['1_day_trend'][1] == False and minutes['1_weekly_trend'][1] == False and minutes['1_weekly_macd_trend'][1] == False:
                minutes['Signla'] = 'Strong Sell'
                Sell_executed_order(i,700,380)
                Forex_order.objects.create(Forexname=i,minutes=minutes['Trend'][1],hours_macd=minutes['1_hr_trend'][1],day_ema=minutes['1_day_trend'][1],day_macd=minutes['1_day_macd_trend'][1],weekly_ema=minutes['1_weekly_trend'][1],weekly_macd=minutes['1_weekly_macd_trend'][1])

            elif (minutes['Trend'][1] == False or minutes['close'][1] < minutes['EMA_21'][1]) and minutes['1_hr_trend'][1] == False and minutes['1_day_macd_trend'][1] == False   and minutes['1_weekly_macd_trend'][1] == False:
                minutes['Signla'] = 'Strong Sell'
                Sell_executed_order(i,1000,500)
                Forex_order.objects.create(Forexname=i,minutes=minutes['Trend'][1],hours_macd=minutes['1_hr_trend'][1],day_macd=minutes['1_day_macd_trend'][1],weekly_macd=minutes['1_weekly_macd_trend'][1])

            elif (minutes['Trend'][1] == True or minutes['close'][1] > minutes['EMA_21'][1]) and minutes['1_hr_trend'][1] == True and minutes['1_day_macd_trend'][1] == True   and minutes['1_weekly_macd_trend'][1] == True:
                minutes['Signla'] = 'Strong Buy'
                Buy_executed_order(i,1000,500)
                Forex_order.objects.create(Forexname=i,minutes=minutes['Trend'][1],hours_macd=minutes['1_hr_trend'][1],day_macd=minutes['1_day_macd_trend'][1],weekly_macd=minutes['1_weekly_macd_trend'][1])

                  
            elif (minutes['Trend'][1] == True or minutes['close'][1] > minutes['EMA_21'][1]) and minutes['1_day_macd_trend'][1] == True and minutes['1_day_trend'][1] == True:
                minutes['Signla'] = 'Buy'
                Buy_executed_order(i,600,350)
                Forex_order.objects.create(Forexname=i,minutes=minutes['Trend'][1],day_macd=minutes['1_day_macd_trend'][1],day_ema=minutes['1_day_trend'][1])

            elif (minutes['Trend'][1] == False or  minutes['close'][1] < minutes['EMA_21'][1]) and minutes['1_day_macd_trend'][1] == False and minutes['1_day_trend'][1] == False:
                minutes['Signla'] = 'Sell'
                Sell_executed_order(i,600,350)
                Forex_order.objects.create(Forexname=i,minutes=minutes['Trend'][1],day_macd=minutes['1_day_macd_trend'][1],day_ema=minutes['1_day_trend'][1])
            elif (minutes['Trend'][1] == True or  minutes['close'][1] > minutes['EMA_21'][1]) and minutes['1_hr_trend'][1] == True:
                minutes['Signla'] = 'Buy'
                Buy_executed_order(i,500,350)
                Forex_order.objects.create(Forexname=i,minutes=minutes['Trend'][1],hours_macd=minutes['1_hr_trend'][1])
            elif (minutes['Trend'][1] == False or  minutes['close'][1] > minutes['EMA_21'][1]) and minutes['1_hr_trend'][1] == False:
                minutes['Signla'] = 'Sell'
                Sell_executed_order(i,500,350)
                Forex_order.objects.create(Forexname=i,minutes=minutes['Trend'][1],hours_macd=minutes['1_hr_trend'][1])
          
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
