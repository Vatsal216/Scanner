from django.db import models

# Create your models here.

# class Stocks(models.Model):
#     symbol = models.CharField(max_length=255)
#     industry = models.CharField(max_length=255)


# class Date(models.Model):
#     date = models.DateField(auto_now_add=True)
    
# class day_price(models.Model):
#     stock = models.ForeignKey(Stocks)
#     date = models.ForeignKey(Date)
#     open = models.CharField(max_length=255)
#     high = models.CharField(max_length=255)
#     low = models.CharField(max_length=255)
#     close = models.CharField(max_length=255)
#     volume = models.CharField(max_length=255)
    

# class Day_Support_Resistance(models.Model):
#     stock = models.ForeignKey(Stocks)
#     date = models.ForeignKey(Date)
#     support = models.CharField(max_length=255)
#     Resistance = models.CharField(max_length=255)


# class Hours_Support_Resistance(models.Model):
#     stock = models.ForeignKey(Stocks)
#     date = models.ForeignKey(Date)
#     support = models.CharField(max_length=255)
#     Resistance = models.CharField(max_length=255)


# class Pivot_Point(models.Model):
#     stock = models.ForeignKey(Stocks)
#     date = models.ForeignKey(Date)
#     S1 = models.CharField(max_length=255)
#     S2 = models.CharField(max_length=255)
#     S3 = models.CharField(max_length=255)
#     P = models.CharField(max_length=255)
#     R1 = models.CharField(max_length=255)
#     R2 = models.CharField(max_length=255)
#     R3 = models.CharField(max_length=255)


# class Volume_Delivery(models.Model):
#     stock = models.ForeignKey(Stocks)
#     date = models.ForeignKey(Date)
#     delivery_day = models.CharField(max_length=255)
#     price_change = models.CharField(max_length=255)
#     inside = models.CharField(max_length=255)
#     delivery_weekly = models.CharField(max_length=255)
#     delivery_monthly = models.CharField(max_length=255)
    


# class volume_analyzer(models.Model):
#     stock = models.ForeignKey(Stocks)
#     date = models.ForeignKey(Date)
#     vah = models.CharField(max_length=255)
#     val = models.CharField(max_length=255)
    
    
# class bhoom_analyzer(models.Model):
#     stock = models.ForeignKey(Stocks)
#     date = models.ForeignKey(Date)
#     thirty_minute = models.CharField(max_length=255)
#     day = models.CharField(max_length=255)
#     weekday = models.CharField(max_length=255)
    
    
    
    
class Performance_Stock(models.Model):
    stock = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    signal = models.CharField(max_length=255, null=True,blank=True)
    close= models.CharField(max_length=255, null=True,blank=True)
    
    def __str__(self):
        return self.stock