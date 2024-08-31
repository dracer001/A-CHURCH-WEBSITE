# from flask import current_app, g
# from flask_pymongo import PyMongo
from pymongo import MongoClient

import os
from dotenv import load_dotenv


load_dotenv()
mongo_uri = os.getenv('MONGO_URI_DEV')


def getDb():
    try:
        client = MongoClient(mongo_uri)
        database = client["UBCMx"]
        # client.drop_database(database)
        return database
        # configure db url
    except Exception as e:
        print("error: {}".format(e))
        return False

# def dropDb():
#
# self.db = client  # configure db name


# def getDB():
#     """
#     Configuration method to return db instance
#     """
#     db = getattr(g, "_database", None)
#
#     if db is None:
#         db = g._database = PyMongo(current_app).db
#
#     return db


