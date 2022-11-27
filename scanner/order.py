import pytz
import datetime
import MetaTrader5 as mt5
from .models import *

def Buy_executed_order(ticker1,price_tp,price_sl):
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    
    mt5.login(login = '113295068' , password='Alexa098')
    
    
  
 

    
    lot = 0.1

    point = mt5.symbol_info(ticker1).point
    positions=mt5.positions_get(symbol=ticker1)
  
    price = mt5.symbol_info_tick(ticker1).ask
        
    sl = price - price_sl * point 
    tp = price + price_tp * point
    deviation = 20
    request1 = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ticker1,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl":sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 234000,
        "comment": 'command',
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result1 = mt5.order_send(request1)
    # check the execution result
    print(result1)
    mt5.shutdown()
  


def Sell_executed_order(ticker1,price_tp,price_sl):
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    mt5.login(login = '113295068' , password='Alexa098')
    lot = 0.1
    

    point = mt5.symbol_info(ticker1).point
    positions=mt5.positions_get(symbol=ticker1)
    
    
    price = mt5.symbol_info_tick(ticker1).ask
       
    sl = price + price_sl * point 
    tp = price - price_tp * point
    deviation = 20
    request1 = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": ticker1,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": 234000,
        "comment": 'Strategy1',
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result1 = mt5.order_send(request1)
    # check the execution result
    print(result1)
    
    print(result1)
    mt5.shutdown()
    