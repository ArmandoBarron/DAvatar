# from pymongo import MongoClient
# from .constants import DB_PAIR

# myclient = None
# def init_db():
#   try:
#     myclient = MongoClient('mongodb://'+DB_PAIR+'/',
#     waitQueueTimeoutMS=100, 
#     maxPoolSize=200)
#     print("Connected successfully!")
#     print(myclient)
#   except:   
#     print("Could not connect to db")
