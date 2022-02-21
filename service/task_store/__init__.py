    # from task_store.status import Status
    # from task_store.task import Task
    # import json
    # import datetime

    # tk1  = Status("email_start_1",datetime.datetime.now(), datetime.datetime.now(), "Passed")
    # tk2  = Status("email_start_1",datetime.datetime.now(), datetime.datetime.now(), "Passed")
    # conditions = [tk1, tk2]
    # #print(conditions)
    # image_label_col = Task("email","id....", "done", conditions)
    # print(image_label_col)
    # #print(json.dumps(image_label_col, default=default))

    # conditions = []
    # new_task = Task(task_type, task_id, "init", conditions)
    # tasks = Tasks(new_task)
    # print(new_task.to_json())
    # TaskManager._redis.set(TaskManager._task_management_key, 
    # json.dumps(new_task.to_json()))


    

    #=================================================

    
    # from task_store import task_manager
    # import json
    # x = task_manager.TaskManager.get_task_management()
    # print(x)
    # print(str(x))
    # xx = str(x).replace("\'", "\"")
    # print(xx)
    # TaskManager._redis.set(TaskManager._task_management_key, json.dumps(xx))


    #from task_store.status import Status
    #from task_store.task import Task
    #from task_store.tasks import Tasks
    #import json
    #import datetime


    #TaskManager.create_new_task("EMAIL","afaf")
    # tk1  = Status("email_start_1",datetime.datetime.now(), datetime.datetime.now(), "Passed")
    # tk2  = Status("email_start_1",datetime.datetime.now(), datetime.datetime.now(), "Passed")
    # conditions = [tk1, tk2]
    # #print(conditions)
    # image_label_col = Task("email","id....", "done", conditions)
    # print(image_label_col)
    # #print(json.dumps(image_label_col, default=default))

    # _tasks = []

    # conditions = []
    # status_1 = ConditionCondition("START","DATE_TIME","Task is Started")
    # status_2 = ConditionCondition("DONE","DATE_TIME","Task is Done")
    # conditions.append(status_1)
    # conditions.append(status_2)
    # new_task = Welcome3Condition("type", "fafa", "init", conditions)
    # _tasks.append(new_task)

    # conditions_1 = []
    # status_3 = ConditionCondition("START","DATE_TIME_2","Task is Started")
    # status_4 = ConditionCondition("DONE","DATE_TIME_2","Task is Done")
    # conditions_1.append(status_3)
    # conditions_1.append(status_4)
    # new_task2 = Welcome3Condition("type2", "faf2", "init2", conditions_1)
    # _tasks.append(new_task)

    # tasks = Welcome3(_tasks)
    # print(json.dumps(tasks))

    # after this my original code

    # conditions = []
    # status_1 = Status("START","DATE_TIME","Task is Started")
    # status_2 = Status("DONE","DATE_TIME","Task is Done")
    # conditions.append(status_1)
    # conditions.append(status_2)
    # _tasks = []
    # new_task = Task("type", "fafa", "init", conditions)
    # _tasks.append(new_task)

    # conditions_1 = []
    # status_3 = Status("START","DATE_TIME_2","Task is Started")
    # status_4 = Status("DONE","DATE_TIME_2","Task is Done")
    # conditions_1.append(status_3)
    # conditions_1.append(status_4)
    # new_task2 = Task("type2", "faf2", "init2", conditions_1)
    # _tasks.append(new_task2)
    # tasks = Tasks(_tasks)
    # #print("---->",tasks.to_json())
    # s = TaskManager.testing_create_new_task(tasks.to_json())
    # #print("@@@@@@@",type(s))
    # js =json.loads(json.dumps(s))



    # print("======***====",type(js['conditions']))
    # print("======INITSELF====",js['conditions'])
    # print("===========",type(js['conditions'][0]))
    # print("======INITSELF====",js['conditions'])
    # print(len(js['conditions']))
    # x = json.loads(js['conditions'][1])
    # print(len(x))
    # print(x)
    #print(json.loads(json.dumps(js['conditions']))[0])
    #print("",TaskManager.function_2(js['conditions'],"fafa"))