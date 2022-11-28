import MetaTrader5 as mt5
import pytz
import time
import pandas as pd
import numpy as np
import pandas_ta as ta

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
        return rates1
    
    @staticmethod
    def Buid_EMA_Dataframe(rates1):

        df1 = pd.DataFrame(rates1)
        df1['time']=pd.to_datetime(df1['time'], unit='s')
        df1['Trend'] = df1.ta.ema(21, append=True) > df1.ta.ema(50, append=True)

       
        return df1
    
    @staticmethod
    def Build_EMA_Condition(df1):
        
        
        df1 = df1.loc[:,['time','isMaxima','isMin','Trend']]
        df1.set_index('time', inplace=True)
        return df1
    
    @staticmethod
    def Build_Buy_EMA_Analysis(df1):
        df1 = df1.tail(3)
        print(df1)
        
        if df1['Trend'][1] == True:
            return 'Buy'
        
        # return(df1['isMin'][1])
        
    @staticmethod
    def Build_Sell_EMA_Analysis(df1):
        df1 = df1.tail(3)
        if df1['Trend'][1] == False:
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
