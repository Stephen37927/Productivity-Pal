from pymongo import MongoClient
from collections.abc import MutableMapping

def get_database():
    # 提供 mongodb atlas url 以使用 pymongo 将 python 连接到 mongodb
    CONNECTION_STRING = "mongodb+srv://kaopu_nlp:NLPkaokaokao7607@xlincluster.cqjabof.mongodb.net/?retryWrites=true&w=majority&appName=xLinCluster"

    # 使用 MongoClient 创建连接。您可以导入 MongoClient 或者使用 pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # 为我们的示例创建数据库（我们将在整个教程中使用相同的数据库
    return client['test1']


# 添加此项是为了让许多文件可以重用函数 get_database()
if __name__ == "__main__":
    # 获取数据库
    dbname = get_database()
    collection_name = dbname["collection1"]
    item_1 = {
        "_id": "U1Iq",
        "item_name": "Blender",
        "max_discount": "10%",
        "batch_number": "RR450020FRG",
        "price": 340,
        "category": "kitchen appliance"
    }

    item_2 = {
        "_id": "U1Iw",
        "item_name": "Egg",
        "category": "food",
        "quantity": 12,
        "price": 36,
        "item_description": "brown country eggs"
    }
    collection_name.insert_many([item_1, item_2])
