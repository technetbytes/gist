import json
from task_store.converter import datetime_converter
from task_store.status import Status

# As per design we have finalized that, we have to Task class 1) Task Class and Detail Task Class.
# Detail Task Class hold condition object, which hold different task status. PENDING, RECEIVED, START, DONE, FAIL 

class QuickViewTask:
    def __init__(self, task_name, task_id, message, status) -> None:
        self.task_name = task_name
        self.task_id = task_id
        self.message = message
        self.status = status

    def __iter__(self):
        yield from {
            "task_name": self.task_name,
            "task_id": self.task_id,
            "message":  self.message,
            "status" : self.status
        }.items()
    
    def __str__(self):
        return json.dumps(self.to_json(), ensure_ascii=False, default = datetime_converter)

    def __repr__(self):
        return self.__str__()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    def to_json(self):
        to_return = {"task_id": self.task_id, "task_name": self.task_name, "message": self.message, "status": self.status}
        return to_return

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
        to_return = {"task_name": self.task_name, "task_id": self.task_id, "message": self.message, "conditions":self.conditions}
        statuses = []
        for status in self.conditions:
            if isinstance(status, dict):
                from collections import namedtuple
                dtuple = namedtuple("ObjectName", status.keys())(*status.values())
                conditions = []
                _s = Status(dtuple.id, dtuple.status_name, dtuple.status_datetime, dtuple.message)
                statuses.append(_s.to_json())
            if isinstance(status,Status):    
                statuses.append(status.to_json())  
        to_return["conditions"] = statuses
        return to_return

# import json
# from task_store.converter import datetime_converter

# class Task:
#     def __init__(self, task_name, task_id, message, conditions):
#         self.task_name = task_name
#         self.task_id = task_id
#         self.conditions = conditions
#         self.message = message

#     def __iter__(self):
#         yield from {
#             "task_name": self.task_name,
#             "task_id": self.task_id,
#             "conditions": self.conditions,
#             "message":  self.message
#         }.items()

#     def __str__(self):
#         return json.dumps(self.to_json(), ensure_ascii=False, default = datetime_converter)
    
#     def __repr__(self):
#         return self.__str__()

#     def toJSON(self):
#         return json.dumps(self, default=lambda o: o.__dict__, 
#             sort_keys=True, indent=4)

#     def to_json(self):
#         to_return = {"task_name": self.task_name, "task_id": self.task_id, "message": self.message}
#         statuses = []
#         for status in self.conditions:
#             statuses.append(status.__dict__)        
#         #statuses = {}
#         #for key, status in self.conditions.items():
#         #     single_status = []
#         #     for status_set in status:
#         #         single_status.append(status_set.__dict__)
#         #         statuses[key] = single_status

#         to_return["conditions"] = statuses
#         return to_return