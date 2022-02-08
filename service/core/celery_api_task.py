from celery import Task

class CeleryApiTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))
    def on_success(self, retval, task_id, args, kwargs):
        print('{0!r} success!: {1!r}'.format(task_id, args))