```
pip install --upgrade 'volcengine-python-sdk[ark]'
```

API 这些在网站上看
https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey?apikey=%7B%7D

## mongoDB
```shell
python -m pip install "pymongo[srv]"
pip install --quiet sentence-transformers pymongo einops

```
参考文档
https://cloud.mongodb.com/v2/66ab7c7c307c4319cb9c6bc5#/overview
https://www.mongodb.com/zh-cn/docs/atlas/atlas-vector-search/create-embeddings/

## Deadlines DataBase
```jason
{
    "Title": "Task Title", # required
    "Description": "Task Description", # optional
    "Start Time": "Task Start Time", # timestamp, optional
    "Deadline": "Task Deadline", # timestamp, required
    "Subtasks": [], # if task is a parent task, this field will contain subtasks' _id, optional
    "Parent Task": [], # if task is a subtask, this field will contain parent task's _id, required for subtasks
    "Status": 0, # optional
        for subtasks: default is 0. 0 - Incomplete, 1 - ongoing, 2 - completed, -1 - overdue
        for parent tasks: default is 0. 0 - Not start yet, 10 - allocated, 20 - completed , -10 overdue
    "user_id": 1, 
    "Type": 0, # 0 for Task, 1 for Subtask
}

```

