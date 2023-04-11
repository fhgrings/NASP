import pymongo
import json
import yaml

client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
print(client.list_database_names())
db = client.db_example
coll = db.kube

# with open('../data/data.json') as file:
#      file_data = json.load(file)
# coll.insert_many(file_data)


with open('../data/kube.yaml') as file:
     file_data = yaml.safe_load(file)
coll.insert_one(file_data)