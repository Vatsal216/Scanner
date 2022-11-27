from .models import *
from rest_framework.response import Response
from .utils import *
from .order import *
    


def strategy4(request):
    
    
    if  'GreenStar' == request.body[0]:
        ticker1 = request.body[1]+'m'
        data=Higher_time.objects.get(name=ticker1)
        Signal=EMA_Analysis.Exceute_EMA_Buy(ticker1)
        print(Signal,data.signal)
        if data.signal == 'Bullish' and Signal == 'Buy':
            print(data, Signal)
            Buy_executed_order(ticker1,500,350)
    
    elif  'RedStar' == request.body[0]:
        ticker1 = request.body[1]+'m'  
        data=Higher_time.objects.get(name=ticker1)
        Signal=EMA_Analysis.Exceute_EMA_Sell(ticker1)
        print(Signal,data.signal)
        if data.signal == 'Bearish' and Signal == 'Sell':
            Sell_executed_order(ticker1,500,350)
            print('ggu')

    