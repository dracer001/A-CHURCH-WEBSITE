from flask_pymongo import ObjectId
from models.dbConfig import getDb
import pymongo

mongo_db = getDb()


class AdminUser:
    def __init__(self):
        self.admin_user = mongo_db.adminUsers
        self.admin_user.create_index([("username", pymongo.ASCENDING)], unique=True)
        self.admin_user.create_index([("email", pymongo.ASCENDING)], unique=True)

    def create(self, username, email, password, s_user):
        result = self.admin_user.insert_one({
            'username': username,
            'email': email,
            'password': password,
            's_user': s_user,
            'barn': False,
            'roles': []
        })
        return result.inserted_id

    def find_by_id(self, user_id):
        return self.admin_user.find_one({'_id': ObjectId(user_id)})

    def find_all(self):
        return list(self.admin_user.find())

    def search(self, query):
        return list(self.admin_user.find({
            '$or': [
                {'username': {'$regex': query, '$options': 'i'}},
                {'email': {'$regex': query, '$options': 'i'}},
            ]
        }))

    def get_super(self):
        return self.admin_user.find_one({'s_user': True})

    def update(self, user_id, update_data):
        result = self.admin_user.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count  # Return the number of documents updated

    def delete(self, user_id):
        return self.admin_user.delete_one({'_id': ObjectId(user_id)})

