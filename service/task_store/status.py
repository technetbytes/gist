import json
from task_store.converter import datetime_converter

class Status:
    def __init__(self, status_name, status_start_datetime, message):
        self.status_name = status_name
        self.status_datetime = status_start_datetime
        self.message = message
    
    def __iter__(self):
        yield from {
            "status_name": self.status_name,
            "status_datetime": self.status_datetime,
            "message": self.message
        }.items()
    
    def __str__(self):
        # following commented code is also working as a converter of str
        # return json.dumps(dict(self), ensure_ascii=False, default = str)
        return json.dumps(dict(self), ensure_ascii=False, default = datetime_converter)

    
    def __repr__(self):
        return self.__str__()
    
    def to_json(self):
        return self.__str__()
    
    @staticmethod
    def from_json(json_dct):
      return Status(json_dct['status_name'],
                    json_dct['status_datetime'],
                    json_dct['message'])