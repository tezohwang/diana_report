from pymongo import MongoClient

from .constant import DATABASE

client = MongoClient(DATABASE['db_uri'])
db = client[DATABASE['db_name']]
print("db connected")
