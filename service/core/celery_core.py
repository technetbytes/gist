from celery import Celery

def get_celery(app,config):
    celery = Celery(
        'main',
        backend=config['task_queue']['celery_result_backend'],
        broker=config['task_queue']['celery_broker_url'],
        include=['main']
    )
    #celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery