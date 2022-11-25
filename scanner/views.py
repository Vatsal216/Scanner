from django.shortcuts import render
from django.http import HttpResponse
from .stock import stock_scanner
from .form   import InputForm
from .models import *
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from datetime import date, datetime

def HomePage(request):
    print(request.POST and request.POST['name']!='', request.POST)
    if  request.POST:
        stock_list=[]
        
        
        print(request.POST)
        data={'data':'data not found'}
    
        if request.POST['name']!='':
            stock_list.append(request.POST['name'])
            data=stock_scanner(stock_list)
            data={'data':data[0],'graph':data[1]}
            
        elif 'option' in request.POST and request.POST['option']!='':
            with open("data.json") as json_file:
                data = json.load(json_file)
            for i in data:
                for k,v in i.items():
                    if 'Buy' in i['Signla']:
                        if k == 'Trend' or  k == '1_day_trend':
                            
                            dates = v.split()[1]
                            if datetime.strptime(dates, '%Y-%m-%d').date() == date.today():
                                stock_list.append(i)
                    
            
            data={'data':stock_list}                
            
            
        return render(request, 'index.html',data)
    else:
    
        with open("data.json") as json_file:
            data = json.load(json_file)
    
        data={'data':data}
        # k7b$Yj6w72KD
        return render(request, 'index.html',data)
