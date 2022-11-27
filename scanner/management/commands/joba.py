from django.core.management.base import BaseCommand

from scanner.stock import stock_scanner
import json
from scanner.models import *
import time
from scanner.forex import forex_scanner

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("hello")
        flag=True
        
        while flag:
                stock_list=[]
                forex_list=[]
                forex_data=Performance_Stock.objects.filter(sector__sector='Forex')
                
                stock_data=Performance_Stock.objects.exclude(sector__sector='Forex')
                for i in stock_data:
                    stock_list.append(i.stock)

                data=stock_scanner(stock_list)
                with open("data.json", "w") as outfile:
                    json.dump(data, outfile)
                print(stock_list)
                
                for i in forex_data:
                    forex_list.append(i.stock)
                
                
                data=forex_scanner(forex_list)
                with open("forex.json", "w") as outfile:
                    json.dump(data, outfile)
                print(forex_list)
                    
                    
                    
                    
                    
                
                time.sleep(1800)
  