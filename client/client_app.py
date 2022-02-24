import time
import schedule
from email_message import json_email_request, simple_email_request

def messaging():
    print("sending email ...")
    json_email_request()
  
schedule.every(1).seconds.do(messaging)

def start_scheduler():
    while True:
        schedule.run_pending()
        #time.sleep(1)

if __name__ == '__main__':
    start_scheduler()