import json
from task_store.converter import datetime_converter

class Task:
    def __init__(self, task_name, task_id, message, conditions):
        self.task_name = task_name
        self.task_id = task_id
        self.conditions = conditions
        self.message = message

    def __iter__(self):
        yield from {
            "task_name": self.version,
            "task_id": self.type,
            "conditions": self.conditions,
            "message":  self.message
        }.items()
    
    def __str__(self):
        return json.dumps(self.to_json(), ensure_ascii=False, default = datetime_converter)
    
    def __repr__(self):
        return self.__str__()

    def to_json(self):
        to_return = {"task_name": self.task_name, "task_id": self.task_id, "message": self.message}
        statuses = []
        for status in self.conditions:
            statuses.append(status.__dict__)        
        #statuses = {}
        #for key, status in self.conditions.items():
        #     single_status = []
        #     for status_set in status:
        #         single_status.append(status_set.__dict__)
        #         statuses[key] = single_status

        to_return["conditions"] = statuses
        return to_return