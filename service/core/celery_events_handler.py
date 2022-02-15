#import celery_logger
from core.celery_logger import CeleryLogger

class CeleryEventsHandler:
    def __init__(self, celery_app, session, verbose_logging=False):
        self._app = celery_app
        self._state = celery_app.events.State()
        self._logger = CeleryLogger()
        self._verbose_logging = verbose_logging

    def _event_handler(handler):
        def wrapper(self, event):
            self._state.event(event)
            task = self._state.tasks.get(event['uuid'])
            
            self._logger.log_task_status_change(task, event)
            if(self._verbose_logging):
                self._logger.log_event_details(event)
                self._logger.log_task_details(task)
            
            handler(self, event)
        return wrapper

    @_event_handler
    def _on_task_sent(self, event):
        pass

    @_event_handler
    def _on_task_received(self, event):
        pass

    @_event_handler
    def _on_task_started(self, event):
        pass

    @_event_handler
    def _on_task_succeeded(self, event):
        pass

    @_event_handler
    def _on_task_failed(self, event):
         pass

    @_event_handler
    def _on_task_rejected(self, event):
         pass

    @_event_handler
    def _on_task_revoked(self, event):
         pass

    @_event_handler
    def _on_task_retried(self, event):
        pass

    def start_listening(self):
        with self._app.connection() as connection:
            recv = self._app.events.Receiver(connection, handlers={
                'task-sent': self._on_task_sent,
                'task-received': self._on_task_received,
                'task-started': self._on_task_started,
                'task-succeeded': self._on_task_succeeded,
                'task-failed': self._on_task_failed,
                'task-rejected': self._on_task_rejected,
                'task-revoked': self._on_task_revoked,
                'task-retried': self._on_task_retried
            })
            recv.capture(limit=None, timeout=10)