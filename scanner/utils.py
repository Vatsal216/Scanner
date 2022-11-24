import MetaTrader5 as mt5
import pytz
import time
import pandas as pd
import numpy as np
import talib



class EMA_Analysis():

    @staticmethod
    def Connect_MT5():

        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()
        return mt5

    @staticmethod
    def Fetching_Data(mt5,ticket):
        timezone = pytz.timezone("Etc/UTC")
        rates1 = mt5.copy_rates_from_pos(ticket, mt5.TIMEFRAME_M30,0,500)
        rates2 = mt5.copy_rates_from_pos(ticket, mt5.TIMEFRAME_H4,0,500)   
        return rates1,rates2
    
    @staticmethod
    def Buid_EMA_Dataframe(rates1):
        rates2 = rates1[1]
        rates1 = rates1[0]
        
        df2 = pd.DataFrame(rates2)

        df1 = pd.DataFrame(rates1)
        df1['time']=pd.to_datetime(df1['time'], unit='s')
        df1['MA_20'] = talib.MA(df1['tick_volume'],timeperiod=20,matype=0)
        df1['EMA_21']= talib.EMA(df1['close'],timeperiod=21)
        df1['EMA_50']= talib.EMA(df1['close'],timeperiod=50)
        
        df2['EMA_21']= talib.EMA(df2['close'],timeperiod=21)
        df2['EMA_50']= talib.EMA(df2['close'],timeperiod=50)
        df2['macd'], df2['macdsignal'], df2['macdhist'] = talib.MACD(df2['close'], fastperiod=12, slowperiod=26, signalperiod=9)    

        
       
        return df1,df2
    
    @staticmethod
    def Build_EMA_Condition(df1):
        df2=df1[1]
        df1 =df1[0]
        
        df1['isMaxima'] = max(df1['close'].tolist())
        df1['isMin'] = min(df1['close'].tolist())
        df1['Trend'] = df1['EMA_21'] > df1['EMA_50']
        df2['Trend_higher'] = df2['EMA_21'] > df2['EMA_50']
        df2['macd_trend'] = df2['macd']> df2['macdsignal']
        
        df1 = df1.loc[:,['time','Trend']]
        df2 = df2.loc[:,['time','Trend_higher','macd_trend']]
        df1.set_index('time', inplace=True)
        df2.set_index('time', inplace=True)
        return df1,df2
    
    @staticmethod
    def Build_Buy_EMA_Analysis(df1):
        df2 = df1[1]
        df1 = df1[0]
        
        
        df1 = df1.tail(3)
        df2 = df2.tail(3)
        
        if df1['Trend'][1] == True and df2['Trend_higher'][1] == True and df2['macd_trend'][1] == True or df1['Trend'][1] == True and df2['Trend_higher'][1] == True or df1['Trend'][1] == True and df1['macd_trend'][1] == True:
            return 'Buy'
        
        # return(df1['isMin'][1])
        
    @staticmethod
    def Build_Sell_EMA_Analysis(df1):
        df2 = df1[1]
        df1 = df1[0]
        
        
        df1 = df1.tail(3)
        df2 = df2.tail(3)
        
        if df1['Trend'][1] == False and df2['Trend_higher'][1] == False and df2['macd_trend'][1] == False or df1['Trend'][1] == False and df2['Trend_higher'][1] == False or df1['Trend'][1] == False and df1['macd_trend'][1] == False:
            return 'Sell'
        
    @staticmethod
    def Exceute_EMA_Buy(ticket):
        mt5=EMA_Analysis.Connect_MT5()
        rates1=EMA_Analysis.Fetching_Data(mt5,ticket)
        df1=EMA_Analysis.Buid_EMA_Dataframe(rates1)
        df1=EMA_Analysis.Build_EMA_Condition(df1)
        signal=EMA_Analysis.Build_Buy_EMA_Analysis(df1)
        return signal

    @staticmethod
    def Exceute_EMA_Sell(ticket):
        mt5=EMA_Analysis.Connect_MT5()
        rates1=EMA_Analysis.Fetching_Data(mt5,ticket)
        df1=EMA_Analysis.Buid_EMA_Dataframe(rates1)
        df1=EMA_Analysis.Build_EMA_Condition(df1)
        signal=EMA_Analysis.Build_Sell_EMA_Analysis(df1)
        return signal
