from django.shortcuts import render
from django.http import HttpResponse
from .stock import stock_scanner
from .form   import InputForm
from .models import *
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def HomePage(request):
    if  request.POST:
        stock_list=[]
      
        stock_list.append(request.POST['name'])
        data=stock_scanner(stock_list)
        data={'data':data[0],'graph':data[1]}
        return render(request, 'index.html',data)
    else:
        
        a=["data.json"]
        with open(a[0]) as json_file:
            data = json.load(json_file)
    
        data={'data':data}
        # k7b$Yj6w72KD
        return render(request, 'index.html',data)
