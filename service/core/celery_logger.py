from datetime import datetime as dt
from task_store.task_manager import TaskManager

class CeleryLogger:
    def log_task_status_change(self, task, event):        
        print('[{}] {} {} (STATE={}, UUID={})'.format(
            self._to_datetime(task.timestamp),
            event['type'].upper(),
            task.name,
            task.state.upper(),
            task.uuid
        ))
        TaskManager().update_task_management(
            event['type'].upper(),
            task.name,
            task.state.upper(),
            task.uuid)

    def log_event_details(self, event):
        print('EVENT DETAILS: {}'.format(event))

    def log_task_details(self, task):
        print('TASK DETAILS:')
        print('UUID: {}'.format(task.uuid))
        print('Name: {}'.format(task.name))
        print('State: {}'.format(task.state))
        print('Received: {}'.format(self._to_datetime(task.received)))
        print('Sent: {}'.format(self._to_datetime(task.sent)))
        print('Started: {}'.format(self._to_datetime(task.started)))
        print('Rejected: {}'.format(self._to_datetime(task.rejected)))
        print('Succeeded: {}'.format(self._to_datetime(task.succeeded)))
        print('Failed: {}'.format(self._to_datetime(task.failed)))
        print('Retried: {}'.format(self._to_datetime(task.retried)))
        print('Revoked: {}'.format(self._to_datetime(task.revoked)))
        print('args (arguments): {}'.format(task.args))
        print('kwargs (keyword arguments): {}'.format(task.kwargs))
        print('ETA (Estimated Time of Arrival): {}'.format(task.eta))
        print('Expires: {}'.format(task.expires))
        print('Retries: {}'.format(task.retries))
        print('Worker: {}'.format(task.worker))
        print('Result: {}'.format(task.result))
        print('Exception: {}'.format(task.exception))
        print('Timestamp: {}'.format(self._to_datetime(task.timestamp)))
        print('Runtime: {}'.format(task.runtime))
        print('Traceback: {}'.format(task.traceback))
        print('Exchange: {}'.format(task.exchange))
        print('Routing Key: {}'.format(task.routing_key))
        print('Clock: {}'.format(task.clock))
        print('Client: {}'.format(task.client))
        print('Root: {}'.format(task.root))
        print('Root ID: {}'.format(task.root_id))
        print('Parent: {}'.format(task.parent))
        print('Parent ID: {}'.format(task.parent_id))
        print('Children:')
        for child in task.children:
            print('\t{}\n'.format(str(child)))

    def _to_datetime(self, timestamp):
        return dt.fromtimestamp(timestamp) if timestamp is not None else None