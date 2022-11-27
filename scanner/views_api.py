from django.shortcuts import render
from .models import *
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import *
from .order import *
from .strategy import *
@api_view(['GET','POST'])
def Lux_Bhoomi_View(request):
        
        
        request.body = request.body.decode()
        request.body = request.body.split(" ")
        print(request.body)
        if len(request.body)>2:
                if request.body[2] == 'EMA':
                        Higher_time.objects.filter(name=request.body[1]+'m').update(signal=request.body[0])
        elif len(request.body)>1:
                if request.body[0] == 'GreenStar' or request.body[0] == 'RedStar':
                        print('a')
                        strategy4(request)
        return Response({'Symbol':"A"})
