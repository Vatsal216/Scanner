from django.core.management.base import BaseCommand

from scanner.stock import stock_scanner
import json
from scanner.models import *
import time
class Command(BaseCommand):

    def handle(self, *args, **options):
        print("hello")
        flag=True
        try:
            while flag:
                stock_list=[]
                stock_data=Performance_Stock.objects.all()
                for i in stock_data:
                    stock_list.append(i.stock)
                # stock_list.append("AXISBANK.NS")
                # stock_list.append("HDFCBANK.NS")
                data=stock_scanner(stock_list)
                with open("C:\\Users\\vatsa\\Desktop\\EUR\\stock\\data.json", "w") as outfile:
                    json.dump(data, outfile)
                
                time.sleep(1800)
        except Exception as e:
            e