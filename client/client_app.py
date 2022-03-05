import time
import schedule
from email_message import json_email_request, simple_email_request
from sms_message import sms_request
from whatsapp_message import whatsapp_request
import random

def messaging():
    number = random.randint(1,3)
    if number == 1:
        print("sending email ...")
        json_email_request()
    elif number == 2:
        print("sending sms ...")
        sms_request()
    elif number == 3:
        print("sending whatsapp ...")
        whatsapp_request()
  
schedule.every(1).seconds.do(messaging)

def start_scheduler():
    while True:
        schedule.run_pending()
        #time.sleep(1)

if __name__ == '__main__':
    start_scheduler()