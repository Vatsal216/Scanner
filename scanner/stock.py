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


def find_suppressed(day):
    df=day
    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
    
    def isSupport(df,i):
        support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
        return support
    def isResistance(df,i):
        resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
        return resistance
    
    s =  np.mean(df['High'] - df['Low'])
    
    def isFarFromLevel(l):
        return np.sum([abs(l-x) < s  for x in levels]) == 0
    
    levels = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['Low'][i]
            if isFarFromLevel(l):
                levels.append((i,l))
        elif isResistance(df,i):
            l = df['High'][i]
            if isFarFromLevel(l):
                levels.append((i,l))
    
    
    def plot_all():
        fig, ax = plt.subplots()
        candlestick_ohlc(ax,df.values,width=0.6, \
                        colorup='green', colordown='red', alpha=0.8)
        date_format = mpl_dates.DateFormatter('%d %b %Y')
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        fig.tight_layout()
        fig.set_figwidth(15)
        fig.set_figheight(5)
        for level in levels:
            plt.hlines(level[1],xmin=df['Date'][level[0]],\
                    xmax=max(df['Date']),colors='blue')
        from django.http import HttpResponse

        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        
        imgdata.seek(0)
        data = imgdata.getvalue()
        
        return data
    da=plot_all() 
    return da
    
def stock_scanner(stock_list):
  
    
    try: 
        lst=[]
        for i in stock_list:
            
            minutes = yf.download(i,period="60d",interval="30m")
            Hr = yf.download(i,period="70d",interval="1h")
            day = yf.download(i,period="70d",interval="1d")
            weeklo = yf.download(i,period="400d",interval="1wk")
            


            minutes['EMA_21']= talib.EMA(minutes['Close'],timeperiod=21) 
            minutes['EMA_50']= talib.EMA(minutes['Close'],timeperiod=50)

            Hr['EMA_21']= talib.EMA(Hr['Close'],timeperiod=21)
            Hr['EMA_50']= talib.EMA(Hr['Close'],timeperiod=50)

            day['EMA_21']= talib.EMA(day['Close'],timeperiod=21)
            day['EMA_50']= talib.EMA(day['Close'],timeperiod=50)
            day['macd'], day['macdsignal'], day['macdhist'] = talib.MACD(day['Close'], fastperiod=12, slowperiod=26, signalperiod=9)    

            weeklo['EMA_21']= talib.EMA(weeklo['Close'],timeperiod=21)
            weeklo['EMA_50']= talib.EMA(weeklo['Close'],timeperiod=50)
            weeklo['macd'], weeklo['macdsignal'], weeklo['macdhist'] = talib.MACD(weeklo['Close'], fastperiod=12, slowperiod=26, signalperiod=9)  

            minutes['Trend'] = minutes['EMA_21'] > minutes['EMA_50']
            Hr['Trend'] = Hr['EMA_21'] > Hr['EMA_50']
            
            day['Trend'] = day['EMA_21'] > day['EMA_50']
            day['macd_trend']=day['macd'] > day['macdsignal']
            
            weeklo['Trend'] = weeklo['EMA_21'] > weeklo['EMA_50']
            weeklo['macd_trend']=weeklo['macd'] > weeklo['macdsignal']
            
            
            if len(stock_list)==1:
                da=find_suppressed(day)
            
            minuts = minutes.tail(200)[::-1]
            minu = minutes.tail(1)
            Trend_last=''
            close_last=0
        
            for j in range(len(minuts)):
                # print(minu['Trend'][0], minuts.iloc[j, 8])
                if minu['Trend'][0] == minuts.iloc[j, 8]:
                    # print(minutes['Trend'][j], minu['Trend'][0],minutes['date_lasta'][j] )
                    pass
                elif minu['Trend'][0] != minuts.iloc[j, 8]:
                    Trend_last = minuts.index.values[j-1]
                    close_last = minuts.iloc[j-1, 3]
                
                    break
            
            last_day = weeklo.tail(2)
            
            day = day.tail(1)
            minutes = minutes.tail(2)
        
            Hr = Hr.tail(1)
            
            
        
        
        
            minutes['Pivot'] = int((last_day['High'][0] + last_day['Low'][0] + last_day['Close'][0])/3)
            minutes['R1'] = int(2*minutes['Pivot'][0] - last_day['Low'][0])
            minutes['S1'] = int(2*minutes['Pivot'][0] - last_day['High'][0])
            minutes['R2'] = int(minutes['Pivot'][0] + (last_day['High'][0] - last_day['Low'][0]))
            minutes['S2'] = int(minutes['Pivot'][0] - (last_day['High'][0] - last_day['Low'][0]))
            minutes['R3'] = int(minutes['Pivot'][0] + 2*(last_day['High'][0] - last_day['Low'][0]))
            minutes['S3'] = int(minutes['Pivot'][0] - 2*(last_day['High'][0] - last_day['Low'][0]))
            
            weeklo = weeklo.tail(2)
            minutes['1_day_trend'] =  day['Trend'][0]
            minutes['1_hr_trend'] = Hr['Trend'][0]
            minutes['1_day_macd_trend'] = day['macd_trend'][0]
            minutes['1_weekly_trend']=weeklo['Trend'][0]
            minutes['1_weekly_macd_trend']=weeklo['Trend'][0]
            # minutes['date']=minutes.index.values[1]
            minutes['name']=i
            if len(stock_list)==1:
                minutes['graph']=da
            if minutes['Trend'][1] == True and minutes['Trend'][0] == False:
                # Performance_Stock.objects.filter(name=i).update(signal= minutes['Trend'][1],name=i,close=minutes['Close'][1])
                
                if minutes['Trend'][1] == True and minutes['1_day_macd_trend'][1] == True and minutes['1_day_trend'][1]== True and minutes['1_weekly_trend'][1]==True and minutes['1_weekly_macd_trend'][1]==True: 
                    minutes['Signla'] = 'Strong Buy'
                elif minutes['Trend'][1] == True and minutes['1_day_macd_trend'][1] == True and minutes['1_day_trend'][1]== True: 
                    minutes['Signla'] = 'Buy'
                elif minutes['Trend'][1] == True and minutes['1_day_macd_trend'][1] == True: 
                    minutes['Signla'] = 'Buy'
                elif minutes['Trend'][1] == True and minutes['1_day_trend'][1] == True: 
                    minutes['Signla'] = 'Buy (Check Support and Resistance)'
                else:
                    minutes['Signla'] = 'Wait'
                minutes['Trend'] = str(minutes['Trend'][1]) +' '+ '(Now)'
            else:
                # stcok_data=Performance_Stock.objects.get(name=i)
                
                if minutes['Trend'][1] == True and minutes['1_day_macd_trend'][1] == True and minutes['1_day_trend'][1]== True and minutes['1_weekly_trend'][1]==True and minutes['1_weekly_macd_trend'][1]==True: 
                    minutes['Signla'] = 'Strong Buy'
                elif minutes['Trend'][1] == True and minutes['1_day_macd_trend'][1] == True and minutes['1_day_trend'][1]== True: 
                    minutes['Signla'] = 'Buy'
                elif minutes['Trend'][1] == True and minutes['1_day_macd_trend'][1] == True: 
                    minutes['Signla'] = 'Buy'
                elif minutes['Trend'][1] == True and minutes['1_day_trend'][1] == True: 
                    minutes['Signla'] = 'Buy (Check Support and Resistance)'
                else:
                    minutes['Signla'] = 'Wait'
                    
            
            
            
                Trend_last = str(Trend_last)
                Trend_last=Trend_last.replace("T"," ")
                Trend_last=Trend_last.split(".", 1)[0]
                
                
                minutes['Trend'] = str(minutes['Trend'][1])+'   '+str(Trend_last) + ' '+'Price '+str(int(close_last)) 
                minutes['up_side'] = int(minutes['Close'][1] - close_last )
                minutes['highest']=minutes['up_side']
                minutes['Close']=int(minutes['Close'][1])
                import json
                # with open("data.json") as json_file:
                #     data1 = json.load(json_file)
                with open("data.json", "r") as read_file:
                    data1 = json.load(read_file)
                    
                    for k,v in data1[0].items():
                    
                        if v==i:
                            if k == 'highest' and v <minutes['up_side'] :
                                v=minutes['up_side']
                            
                
            
        
        
            minutes=minutes.to_dict('records')[1]
            lst.append(minutes)
        
        if len(stock_list)==1:
            return lst,da
        else:
            return lst
    except Exception as e:
        return 'Stock Not Found. Kindly add .NS at the end. Example (WIPRO.NS)'



