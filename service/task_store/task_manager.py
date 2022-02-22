from task_store.task import Task
from task_store.tasks import Tasks
from task_store.status import Status
import redis
import datetime
from config.setting import Config
import json
from utilities.json_extension import check_update_list
from task_store.converter import datetime_converter

class TaskManager:

    _redis = None
    _task_management_key = None
    def __redis():
        server = Config.get_complete_property('redis','server')
        port = Config.get_complete_property('redis','port')
        db = Config.get_complete_property('redis','db')
        TaskManager._redis = redis.Redis(server, port, db)
        TaskManager._task_management_key = Config.get_complete_property('redis','task_management_key')

    @staticmethod
    def __find_task_object(json_object, name):
        for dict in json_object:
            x = json.loads(dict)
            if x['task_id'] == name:
                return x

    @staticmethod
    def __find_task(json_object, name):
        task = [obj for obj in json_object if obj['task_id']==name]
        if len(task) > 1 and task is not None:
            return task[0]
        return None

    @staticmethod
    def clear_task_tasks_obj_as_dict():
        # check and then create redis server object       
        if TaskManager._redis is None:
            TaskManager.__redis()
        TaskManager._redis.delete(TaskManager._task_management_key)


    def get_task_management():
        # check and then create redis server object       
        if TaskManager._redis is None:
            TaskManager.__redis()
        tasks_data_as_bytes = TaskManager._redis.get(TaskManager._task_management_key)
        if tasks_data_as_bytes is not None:
            tasks_data_as_str = tasks_data_as_bytes.decode("utf-8")
            tasks_obj_as_dict = json.loads(tasks_data_as_str)                        
            return tasks_obj_as_dict
        else:
            return None

    @staticmethod
    def __update_json_object(tasks_obj_as_dict, replace_obj):
        for task in tasks_obj_as_dict:
            if json.loads(task)['task_id'] == replace_obj['task_id']:
                task = json.dumps(replace_obj)
                break
        return tasks_obj_as_dict

    @staticmethod
    def update_task_management_ext(event, name, status, id):
        tasks_obj_as_dict = TaskManager.get_task_management()        
        if tasks_obj_as_dict is not None:
            for element in tasks_obj_as_dict:
                for elt in  tasks_obj_as_dict[element]:
                    if elt['task_id'] == id:
                        new_status = Status(id, name, str(datetime.datetime.now()), status)
                        elt['conditions'].append(new_status)
        tasks = Tasks(tasks_obj_as_dict['conditions'])
        TaskManager._redis.set(TaskManager._task_management_key, json.dumps(tasks.to_json()))

    @staticmethod
    def update_task_management(event, name, status, id):
        tasks_obj_as_dict = TaskManager.get_task_management()
        if tasks_obj_as_dict is not None:
            #convert dict into json object called cache_object and add new item in the existing collection
            cache_data = json.loads(json.dumps(tasks_obj_as_dict))
            if cache_data is not None:
                current_task = TaskManager.__find_task_object(cache_data['conditions'], id)
                if current_task is not None:
                    # get task status list
                    current_task_conditions = current_task['conditions']
                    # add new status in the task_conditions list
                    new_status = Status(id, name, datetime.datetime.now(), status)
                    current_task_conditions.append(new_status)
                    # update object
                    update_json_obj = TaskManager.__update_json_object(cache_data['conditions'], current_task)

    @staticmethod
    def create_new_task(message_type, task):
    # check and then create redis server object       
        if TaskManager._redis is None:
            TaskManager.__redis()        
        _conditions = []
        _tasks = []
        tasks_obj_as_dict = TaskManager.get_task_management()
        if tasks_obj_as_dict is None:
            #first time creating task in the redis
            if task is not None:
                new_task = Task(message_type, task.id, "init", _conditions)
                _tasks.append(new_task)
                tasks = Tasks(_tasks)
                TaskManager._redis.set(TaskManager._task_management_key, json.dumps(tasks.to_json()))
        else:
            new_task = Task(message_type, task.id, "init", _conditions)
            #convert dict into json object called cache_object and add new item in the existing collection
            cache_data = json.loads(json.dumps(tasks_obj_as_dict))
            # print(cache_data)
            cache_data['conditions'].append(new_task)   
            # prefixed by an asterisk operator to unpack the values in order to create a typename tuple subclass
            tasks = Tasks(*cache_data.values())
            TaskManager._redis.set(TaskManager._task_management_key, json.dumps(tasks.to_json()))
            return tasks_obj_as_dict
            
    @staticmethod
    def testing_create_new_task(task):
        # check and then create redis server object       
        if TaskManager._redis is None:
            TaskManager.__redis()
        
        tasks_obj_as_dict = TaskManager.get_task_management()
        if tasks_obj_as_dict is None:
            TaskManager._redis.set(TaskManager._task_management_key, json.dumps(task))
        else:
            return tasks_obj_as_dict


# from task_store.task import Task
# from task_store.tasks import Tasks
# from task_store.status import Status
# import redis
# import datetime
# from config.setting import Config
# import json
# from utilities.json_extension import check_update_list
# from task_store.converter import datetime_converter

# class TaskManager:

#     _redis = None
#     _task_management_key = None
#     def __redis():
#         server = Config.get_complete_property('redis','server')
#         port = Config.get_complete_property('redis','port')
#         db = Config.get_complete_property('redis','db')
#         TaskManager._redis = redis.Redis(server, port, db)
#         TaskManager._task_management_key = Config.get_complete_property('redis','task_management_key')

#     @staticmethod
#     def __find_task_object(json_object, name):
#         for dict in json_object:
#             x = json.loads(dict)
#             if x['task_id'] == name:
#                 return x

#     @staticmethod
#     def __find_task(json_object, name):
#         task = [obj for obj in json_object if obj['task_id']==name]
#         if len(task) > 1 and task is not None:
#             return task[0]
#         return None

#     @staticmethod
#     def clear_task_tasks_obj_as_dict():
#         # check and then create redis server object       
#         if TaskManager._redis is None:
#             TaskManager.__redis()
#         TaskManager._redis.delete(TaskManager._task_management_key)


#     def get_task_management():
#         # check and then create redis server object       
#         if TaskManager._redis is None:
#             TaskManager.__redis()
#         tasks_data_as_bytes = TaskManager._redis.get(TaskManager._task_management_key)
#         if tasks_data_as_bytes is not None:
#             tasks_data_as_str = tasks_data_as_bytes.decode("utf-8")
#             tasks_obj_as_dict = json.loads(tasks_data_as_str)                        
#             return tasks_obj_as_dict
#         else:
#             return None

#     @staticmethod
#     def __update_json_object(tasks_obj_as_dict, replace_obj):
#         for task in tasks_obj_as_dict:
#             if json.loads(task)['task_id'] == replace_obj['task_id']:
#                 task = json.dumps(replace_obj)
#                 break
#         return tasks_obj_as_dict

#     @staticmethod
#     def update_task_management_ext(event, name, status, id):
#         tasks_obj_as_dict = TaskManager.get_task_management()        
#         if tasks_obj_as_dict is not None:
#             #Iterating all the fields of the JSON
#             for element in tasks_obj_as_dict:
#                 #If Json Field value is a list
#                 if (isinstance(tasks_obj_as_dict[element], list)):
#                     # add new status in the task_conditions list
#                     new_status = Status(id, name, datetime.datetime.now(), status)
#                     check_update_list(tasks_obj_as_dict[element], element, new_status)
#             tasks = Tasks(tasks_obj_as_dict['conditions'])
#             TaskManager._redis.set(TaskManager._task_management_key, json.dumps(tasks.to_json()))

#     @staticmethod
#     def update_task_management(event, name, status, id):
#         tasks_obj_as_dict = TaskManager.get_task_management()
#         if tasks_obj_as_dict is not None:
#             #convert dict into json object called cache_object and add new item in the existing collection
#             cache_data = json.loads(json.dumps(tasks_obj_as_dict))
#             if cache_data is not None:
#                 current_task = TaskManager.__find_task_object(cache_data['conditions'], id)
#                 if current_task is not None:
#                     # get task status list
#                     current_task_conditions = current_task['conditions']
#                     # add new status in the task_conditions list
#                     new_status = Status(id, name, datetime.datetime.now(), status)
#                     current_task_conditions.append(new_status)
#                     # update object
#                     update_json_obj = TaskManager.__update_json_object(cache_data['conditions'], current_task)

#     @staticmethod
#     def create_new_task(message_type, task):
#     # check and then create redis server object       
#         if TaskManager._redis is None:
#             TaskManager.__redis()        
#         _conditions = []
#         _tasks = []
#         tasks_obj_as_dict = TaskManager.get_task_management()
#         if tasks_obj_as_dict is None:
#             #first time creating task in the redis
#             if task is not None:
#                 new_task = Task(message_type, task.id, "init", _conditions)
#                 _tasks.append(new_task)
#                 tasks = Tasks(_tasks)
#                 TaskManager._redis.set(TaskManager._task_management_key, json.dumps(tasks.to_json()))
#         else:
#             new_task = Task(message_type, task.id, "init", _conditions)
#             #convert dict into json object called cache_object and add new item in the existing collection
#             cache_data = json.loads(json.dumps(tasks_obj_as_dict))
#             # print(cache_data)
#             cache_data['conditions'].append(new_task)   
#             # prefixed by an asterisk operator to unpack the values in order to create a typename tuple subclass
#             tasks = Tasks(*cache_data.values())
#             TaskManager._redis.set(TaskManager._task_management_key, json.dumps(tasks.to_json()))
#             return tasks_obj_as_dict
            
#     @staticmethod
#     def testing_create_new_task(task):
#         # check and then create redis server object       
#         if TaskManager._redis is None:
#             TaskManager.__redis()
        
#         tasks_obj_as_dict = TaskManager.get_task_management()
#         if tasks_obj_as_dict is None:
#             TaskManager._redis.set(TaskManager._task_management_key, json.dumps(task))
#         else:
#             return tasks_obj_as_dict
