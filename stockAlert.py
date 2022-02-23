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
import smtplib, ssl


minutes = 5 #minutes of sleep after each check
stocks = [
    {'symbol': 'XRP', 'price': 1.7 , 'direction': 'up'}, 
    {'symbol': 'XRP', 'price': 0.8 , 'direction': 'down'}, 
    ]


class StockAlert:
    load_dotenv()
    NUMBER_ENV = os.getenv('NUMBER')
    KEY_ENV = os.getenv('KEY')
    SECRET_ENV = os.getenv('SECRET')
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv('SENDER_EMAIL_ENV')  # Enter your address
    receiver_email = os.getenv('RECEIVER_EMAIL_ENV')   # Enter receiver address
    GMAIL_PASS_ENV = os.getenv('GMAIL_PASS')

    
    def __init__(self, direction, stockTicker, targetValue ):
    
        self.stockTicker = stockTicker
        self.targetValue = targetValue
        self.direction = direction
        self.flag = 0
  

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
    def sendMail(self):
            SUBJECT = "Stock Alert from Alon's Python3 Script"
            TEXT = f"""
            exec ! {self.stockTicker} {str(self.lastPrice)} target price:  {str(self.targetValue)} 
                       direction {self.direction}
                        """
            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(self.sender_email, self.GMAIL_PASS_ENV)
                server.sendmail(self.sender_email, self.receiver_email, message)

list = []

for obj in stocks:
    list.append(StockAlert(obj['direction'] or 'up', obj['symbol'], obj['price'] ))
sizeOfList = len(list)
counter = 0


while(sizeOfList != counter):
  
        for obj in list:
            if obj.direction == 'up':
                if (obj.checkPrice() >= obj.targetValue and obj.flag !=1):
                    obj.sendSMS()
                    obj.sendMail()
                    obj.flag = 1
                    counter+=1
                    print(f"exec! {str(minutes)} minutes..  {obj.stockTicker} {str(obj.lastPrice)}  target price:  {str(obj.targetValue)} , direction: {obj.direction}")  
                else:
                    print(f"sleeping {str(minutes)} minutes..  {obj.stockTicker} {str(obj.lastPrice)}  target price:  {str(obj.targetValue)} , direction: {obj.direction}")

                            
            if obj.direction == 'down': 
                 
                if (obj.checkPrice() <= obj.targetValue and obj.flag !=1):
                    obj.sendSMS()
                    obj.sendMail()
                    obj.flag = 1
                    counter+=1
                    print(f"exec! {str(minutes)} minutes..  {obj.stockTicker} {str(obj.lastPrice)}  target price:  {str(obj.targetValue)} , direction: {obj.direction}")  
                else:
                    print(f"sleeping {str(minutes)} minutes..  {obj.stockTicker} {str(obj.lastPrice)}  target price:  {str(obj.targetValue)} , direction: {obj.direction}")
                
        print('counter ' + str(counter))
        




 
        time.sleep(minutes * 60)