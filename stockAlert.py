"""
main idea:
- check price every x minutes (5 minutes , make sense)
- send SMS if above value (simple script using OOP)
"""

import time
import requests
import datetime as dt  
import vonage
import os
from dotenv import load_dotenv


class StockAlert:
    
    
    def __init__(self, direction, stockTicker='IOTA', targetValue=1.8 ):
        


        load_dotenv()
        self.stockTicker = stockTicker
        self.targetValue = targetValue
        self.direction = direction
        self.flag = 0
        self.NUMBER_ENV = os.getenv('NUMBER')
        self.KEY_ENV = os.getenv('KEY')
        self.SECRET_ENV = os.getenv('SECRET')

    def checkPrice(self):
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol="+self.stockTicker+"USDT")
        r.json()
        print (float(r.json()['lastPrice']))
        self.lastPrice = float(r.json()['lastPrice'])
        return self.lastPrice

    def sendSMS(self):
        if (self.NUMBER_ENV[0] == '0' and len(self.NUMBER_ENV)==10):
            self.NUMBER_ENV="972"+self.NUMBER_ENV[1:]
            
        
        client = vonage.Client(self.KEY_ENV, self.SECRET_ENV)
        sms = vonage.Sms(client)
        msg = self.stockTicker + " last price is: " + str(self.lastPrice)
        responseData = sms.send_message(
            {
                "from": "Vonage APIs",
                "to": self.NUMBER_ENV,
                "text": msg,
            }
        )
list = []
stocks = [
    {'symbol': 'IOTA', 'price': 1.7 , 'direction': 'up'}, 
    {'symbol': 'IOTA', 'price': 0.8 , 'direction': 'down'}, 
    ]
for obj in stocks:
    list.append(StockAlert(obj['direction'] or 'up', obj['symbol'], obj['price'] ))
sizeOfList = len(list)
counter = 0
while(sizeOfList != counter):
  
        for obj in list:
            if obj.direction == 'up':
                if (obj.checkPrice() >= obj.targetValue and obj.flag !=1):
                    # obj.sendSMS()
                    obj.flag = 1
                    counter+=1
                else:
                    print("sleeping 5 minutes.. "+ obj.stockTicker + " " + str(obj.lastPrice) + " target price: " +  str(obj.targetValue) + 
                        ' ' + obj.direction)

                            
            if obj.direction == 'down': 
                 
                if (obj.checkPrice() <= obj.targetValue and obj.flag !=1):
                    obj.sendSMS()
                    obj.flag = 1
                    counter+=1
                    print("exec !"+ obj.stockTicker + " " + str(obj.lastPrice) + " target price: " +  str(obj.targetValue) + 
                        ' ' + obj.direction)    
                else:
                    print("sleeping 5 minutes.. "+ obj.stockTicker + " " + str(obj.lastPrice) + " target price: " +  str(obj.targetValue) + 
                        ' ' + obj.direction)    
                
        print('counter ' + str(counter))
        




 
        time.sleep(300)