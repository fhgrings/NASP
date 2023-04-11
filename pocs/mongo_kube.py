import pymongo
import yaml
from kubernetes import client, config
import os

myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
db = myclient["db_example"]
coll = db["kube"]

myquery = { "apiVersion": "v1" }

mydoc = coll.find(myquery)

kube = mydoc[0]

del kube['_id']
open('kube.yaml', 'w').write(yaml.dump(kube))

config.load_kube_config(config_file='./kube.yaml')

v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

os.remove('kube.yaml')