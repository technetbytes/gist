from pyexpat.errors import messages
from flask import Flask, request, jsonify, render_template, session, flash, redirect, url_for, make_response
from core.celery_core import get_celery
from core.celery_api_task import CeleryApiTask
from config.setting import load_setting
from utilities.smtp_server import get_context, init_smtp_server
from utilities.email import build_message, generate_email_body
from celery.result import AsyncResult

# Flask application
flask_app = Flask(__name__)

#Read configuration config.yml
config = load_setting()

# Set application secret_key
flask_app.config['SECRET_KEY'] = config['others']['secret_key']
flask_app.config['SEND_INFO'] = config['email']['sender']

# Initialize object
celerymq = get_celery(app=flask_app, config=config)

@celerymq.task(base=CeleryApiTask,bind=True)
def send_async_email(self, email_info):
    print("Start sending email ...")
    # Create a secure SSL context
    context = get_context()
    try:
        message = build_message(email_info, flask_app.config['SEND_INFO'])
        smtp_server = init_smtp_server(config)
        print("message sent ....")
        smtp_server.send_message(message)
    except Exception as exc:
        # Print any error messages to stdout
        print("error :- ",exc)
        raise self.retry(exc=exc)

@flask_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))


@flask_app.route('/api/v1/task_status', methods=['GET'])
def task_status():
    args = request.args
    task_id = args.get('taskid')
    #return {"taskid":task_id}
    if task_id is not None:
        task_result = celerymq.AsyncResult(task_id)
        return task_result.state

@flask_app.route('/api/v1/send_email', methods=['POST'])
def send_email():
    #fgenerate email body from request object base on request type 
    email_data = generate_email_body(request)
    #send async email
    send_async_email.delay(email_data)
    response = make_response(
                jsonify(
                     message="E-mail sent.",
                    category="EMAIL",
                    status=201,
                    data=email_data),
                201,
            )
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    # run application
    flask_app.run(debug=True)