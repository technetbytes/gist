from pyexpat.errors import messages
from flask import Flask, request, render_template, session, flash, redirect, url_for
from core.celery_core import get_celery
from config.setting import load_setting
from utilities.smtp_server import get_context, init_smtp_server
from utilities.email import build_message, generate_email_body

# Flask application
flask_app = Flask(__name__)

#Read configuration config.yml
config = load_setting()

# Set application secret_key
flask_app.config['SECRET_KEY'] = config['others']['secret_key']
flask_app.config['SEND_INFO'] = config['email']['sender']

# Initialize object
celery = get_celery(app=flask_app, config=config)

@celery.task
def send_async_email(email_info):
    print("Start sending email ...")
    # Create a secure SSL context
    context = get_context()
    try:
        message = build_message(email_info, flask_app.config['SEND_INFO'])
        smtp_server = init_smtp_server(config)
        print("message sent ....")
        smtp_server.send_message(message)
    except Exception as e:
        # Print any error messages to stdout
        print("error :- ",e)

@flask_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))

@flask_app.route('/api/v1/send_email', methods=['POST'])
def send_email():
    #fgenerate email body from request object base on request type 
    email_data = generate_email_body(request)
    #send async email
    send_async_email.delay(email_data)
    return flask_app.make_response('Hello, World')

if __name__ == '__main__':
    # run application
    flask_app.run(debug=True)