from asyncio import constants
import redis
import pyfiglet
from threading import Lock
from pyexpat.errors import messages
from flask_socketio import SocketIO, emit, disconnect
from utilities.constant import *
from flask_session import Session
from flask import Flask, request, jsonify, render_template, session, flash, redirect, url_for, make_response
from core.celery_core import get_celery
from core.celery_api_task import CeleryApiTask
from config.setting import load_setting, Config
from utilities.smtp_server import get_context, init_smtp_server
from utilities.email import build_message, generate_email_body
from celery.result import AsyncResult
import argparse
from core.celery_events_handler import CeleryEventsHandler
from task_store.task_manager import TaskManager

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

# Flask application
flask_app = Flask(__name__)

# Set application secret_key
flask_app.config['SECRET_KEY'] = Config.get_complete_property('others','secret_key')
flask_app.config['SEND_INFO'] = Config.get_complete_property('email','sender') 

# init Socket-IO
socketio = SocketIO(flask_app, async_mode=async_mode)

thread = None
thread_lock = Lock()

# Initialize object celery
celerymq = get_celery(app=flask_app)

def quick_view_task_watch():
    while True:
        socketio.sleep(3)
        snapshot_data = TaskManager.snapshot_data()
        if snapshot_data is not None:
            socketio.emit('quick_view_data',{'data': snapshot_data, 'state':'LOAD'})
        else:
            socketio.emit('quick_view_data',{'data': 'None', 'state':'ERROR'})

def init_socket_bkTask():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(quick_view_task_watch)

def init_celery_logger(app):
    parser = argparse.ArgumentParser(
        description='Monitor of task-related events, generated by a Celery worker.'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help='Detailed information about an event and a related task.'
    )
    args = parser.parse_args()
    events_handler = CeleryEventsHandler(app, None, args.verbose)
    import threading
    threading.Thread(target= events_handler.start_listening, daemon=True).start()

@celerymq.task(base=CeleryApiTask,bind=True,name='WhatsApp')
def send_async_whatsapp(self, whatsapp_info):
    print("Start sending whatsapp ...")
    # Create a secure SSL context
    context = get_context()
    try:
        print("whatsapp sent ....")
    except Exception as exc:
        # Print any error messages to stdout
        print("error :- ",exc)
        raise self.retry(exc=exc)

@celerymq.task(base=CeleryApiTask,bind=True,name='SMS')
def send_async_sms(self, sms_info):
    print("Start sending SMS ...")
    # Create a secure SSL context
    context = get_context()
    try:
        print("sms sent ....")
    except Exception as exc:
        # Print any error messages to stdout
        print("error :- ",exc)
        raise self.retry(exc=exc)

@celerymq.task(base=CeleryApiTask,bind=True,name='Email')
def send_async_email(self, email_info):
    print("Start sending email ...")
    # Create a secure SSL context
    context = get_context()
    try:
        # message = build_message(email_info, flask_app.config['SEND_INFO'])
        # smtp_server = init_smtp_server()
        print("message sent ....")
        # smtp_server.send_message(message)
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
    if task_id is not None:
        task_result = celerymq.AsyncResult(task_id)
        return task_result.state

@flask_app.route('/api/v1/send_whatsapp', methods=['POST'])
def send_whatsapp():
    #generate whatsapp body from request object base on request type 
    whatsapp_data = request.json
    #send async email
    task = send_async_whatsapp.delay(whatsapp_data)
    #Store task info in redis-cache   
    TaskManager.create_new_task(MESSAGE_TYPE_WHATSAPP, task)    
    response = make_response(
                jsonify(
                     message="SMS sent.",
                    category=MESSAGE_TYPE_WHATSAPP,
                    status=201,
                    data=whatsapp_data),
                201,
            )
    response.headers["Content-Type"] = "application/json"
    return response

@flask_app.route('/api/v1/send_sms', methods=['POST'])
def send_sms():
    #generate sms body from request object base on request type 
    sms_data = request.json
    #send async email
    task = send_async_sms.delay(sms_data)
    #Store task info in redis-cache   
    TaskManager.create_new_task(MESSAGE_TYPE_SMS, task)    
    response = make_response(
                jsonify(
                     message="SMS sent.",
                    category=MESSAGE_TYPE_SMS,
                    status=201,
                    data=sms_data),
                201,
            )
    response.headers["Content-Type"] = "application/json"
    return response

@flask_app.route('/api/v1/send_email', methods=['POST'])
def send_email():
    #fgenerate email body from request object base on request type 
    email_data = generate_email_body(request)
    #send async email
    task = send_async_email.delay(email_data)
    #Store task info in redis-cache   
    TaskManager.create_new_task(MESSAGE_TYPE_EMAIL, task)    
    response = make_response(
                jsonify(
                     message="E-mail sent.",
                    category=MESSAGE_TYPE_EMAIL,
                    status=201,
                    data=email_data),
                201,
            )
    response.headers["Content-Type"] = "application/json"
    return response

@socketio.event
def connecting_service(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('connected_service',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.event
def messaging_data(message):
    messages = TaskManager.get_tasks()
    if messages is not None:
        emit('received_data',{'data': messages, 'state':'LOAD'})
    else:
        emit('received_data',{'data': 'None', 'state':'ERROR'})

@socketio.event
def server_ping():
    emit('server_pong')

@socketio.event
def connect():
    emit('service_init', {'data': 'Connected .... init', 'count': 0})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    # run application using socket
    result = pyfiglet.figlet_format("LWMQ")
    print(result)
    ##init celery logger
    init_celery_logger(celerymq)
    ##background socket task for quick view task
    init_socket_bkTask()
    ##init server socket listener
    socketio.run(flask_app,host='0.0.0.0', port=10001)