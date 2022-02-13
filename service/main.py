from socket import socket
from threading import Lock
from pyexpat.errors import messages
from flask import Flask, request, jsonify, render_template, session, flash, redirect, url_for, make_response
from core.celery_core import get_celery
from core.celery_api_task import CeleryApiTask
from config.setting import load_setting
from utilities.smtp_server import get_context, init_smtp_server
from utilities.email import build_message, generate_email_body
from celery.result import AsyncResult
from flask_socketio import SocketIO, emit, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

# Flask application
flask_app = Flask(__name__)

#Read configuration config.yml
config = load_setting()

# Set application secret_key
flask_app.config['SECRET_KEY'] = config['others']['secret_key']
flask_app.config['SEND_INFO'] = config['email']['sender']

# init Socket-IO
socketio = SocketIO(flask_app, async_mode=async_mode)

thread = None
thread_lock = Lock()

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
        return render_template('index.html', email=session.get('email', ''), async_mode=socketio.async_mode)

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

@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.event
def server_ping():
    emit('server_pong')

@socketio.event
def connect():
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    # run application using socket
    #flask_app.run(debug=True)
    socketio.run(flask_app,host='0.0.0.0', port=10001)