import json
from task_store.converter import datetime_converter

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
        #print("Tasks to_json --->",self.mycond)
        for status in self.mycond:
            #print("from Tasks to_json --->",type(status))
            #print("from Tasks to_json in json form --->",str(status))#,json.dumps(status.__dict__))
            statuses.append(str(status))
        to_return["conditions"] = statuses
        #print("to_return is called --->",to_return)
        return to_return
        
def as_payload(dct):
    return Task(dct['task_name'], dct['task_id'], dct['message'], dct['conditions'])

class Task:
    def __init__(self, task_name, task_id, message, conditions):
        self.task_name = task_name
        self.task_id = task_id
        self.conditions = conditions
        self.message = message

    def __iter__(self):
        yield from {
            "task_name": self.task_name,
            "task_id": self.task_id,
            "conditions": self.conditions,
            "message":  self.message
        }.items()

    def __str__(self):
        return json.dumps(self.to_json(), ensure_ascii=False, default = datetime_converter)
    
    def __repr__(self):
        return self.__str__()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def to_json(self):
        #print("to_json is called ,,,,,,")
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