from const import service_address, service_api_ver1, service_port, service_sms_method
import requests

def service_uri():    
    return "{}:{}{}{}".format(service_address,service_port,service_api_ver1,service_sms_method)

def json_content_type():
    return {"content-type": "application/json"}

def sms_request():
    body = {"Number": 123445, "Body":"Hello World"}
    url = service_uri()
    headers = json_content_type()
    response = requests.post(url, json=body, headers=headers)