import json
from task_store.converter import datetime_converter
from task_store.task import Task

class Tasks:
    def __init__(self, conditions):
        self.mycond = conditions
    
    def __iter__(self):
        yield from {
            "conditions": self.mycond,
        }.items()
    
    def __str__(self):
        return json.dumps(self.to_json(), ensure_ascii=False, default = datetime_converter)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        to_return = {}
        statuses = []
        for status in self.mycond:
            # running code
            statuses.append(str(status))
        to_return["conditions"] = statuses
        return to_return
        
def as_payload(dct):
    return Task(dct['task_name'], dct['task_id'], dct['message'], dct['conditions'])