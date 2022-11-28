from django.db import models
    
class Higher_time(models.Model):
    signal = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)    
    
    def __str__(self):
        return self.name
    

class Sector(models.Model):
    sector = models.CharField(max_length=255)
    
    def __str__(self):
        return self.sector
    
class Performance_Stock(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True,blank=True)
    stock = models.CharField(max_length=255)

    def __str__(self):
        return self.stock
        
class Stock_order(models.Model):
    stockname = models.ForeignKey(Performance_Stock, on_delete=models.CASCADE, null=True,blank=True)
    dateTimeField = models.DateField(auto_now_add=True)
    closed_date = models.CharField(max_length=255,blank=True,null=True)   
    price_order = models.IntegerField()
    target_hit = models.IntegerField()
    action = models.CharField(max_length=255,blank=True,null=True)        
                   
    def __str__(self):
        return self.stockname


class Forex_order(models.Model):
    Forexname = models.CharField(max_length=255,blank=True,null=True)
    dateTimeField = models.DateField(auto_now_add=True)
    minutes = models.CharField(max_length=255,blank=True,null=True)
    hours_macd = models.CharField(max_length=255,blank=True,null=True)  
    day_ema = models.CharField(max_length=255,blank=True,null=True)  
    day_macd = models.CharField(max_length=255,blank=True,null=True)  
    weekly_ema = models.CharField(max_length=255,blank=True,null=True)  
    weekly_macd = models.CharField(max_length=255,blank=True,null=True)  
          
                   
    def __str__(self):
        return self.stockname
    