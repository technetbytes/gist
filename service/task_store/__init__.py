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