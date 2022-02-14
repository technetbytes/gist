from operator import index
from random import randint, random
import requests
import json
from message_template import *
import datetime
from const import service_address, service_api_ver1, service_port, service_email_method

addresses_arr = [to_address_1, to_address_2]
body_arr = [email_body_1, email_body_2]
subject_arr = [subject_1, subject_2]

def service_uri():    
    return "{}:{}{}{}".format(service_address,service_port,service_api_ver1,service_email_method)

def json_content_type():
    return {"content-type": "application/json"}

def content_type():
    return {"content-type": "multipart/form-data"}

def get_json_email_content():
    index_value = randint(0,1)
    to = addresses_arr[index_value]
    index_value = randint(0,1)
    subject = subject_arr[index_value]
    index_value = randint(0,1)
    body = body_arr[index_value]
    return json_email_body(to, subject.format(datetime.datetime.now()), body)

def json_email_body(to, subject, body):
    email_body = {
	    "subject": subject,
	    "to_email": to,
	    "email_body": body
    }
    body = email_body#json.loads(email_body)
    return body

def email_body():
    pass

def json_email_request():
    body = get_json_email_content()
    url = service_uri()
    headers = json_content_type()
    response = requests.post(url, json=body, headers=headers)

def simple_email_request():    
    pass