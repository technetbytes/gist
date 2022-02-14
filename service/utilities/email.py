from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import request

def build_message(email_info, from_address):
    message = MIMEMultipart("alternative")
    message["Subject"] = email_info["subject"]
    message["From"] = from_address
    message["To"] = email_info["to"]
    body = MIMEText(email_info["body"], "html")
    message.attach(body)
    return message

def generate_email_body(req):
    email_data = {}
    if not (req is None):
        email_data = {}
        content_type = req.headers.get('Content-Type')
        if (content_type == 'application/json'):
            #get info from request object as json
            json = request.json
            email_data = {'subject': json['subject'], 'to': json['to_email'], 'body': json['email_body']}
        elif (content_type == 'multipart/form-data'):
            #get info from request object
            to_email = request.form.get('to')
            subject = request.form.get('subject')
            email_body = request.form.get('body')
            # send the email
            email_data = {'subject': subject, 'to': to_email, 'body': email_body}
    return email_data