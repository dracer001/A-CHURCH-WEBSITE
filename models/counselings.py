from flask_pymongo import ObjectId
from models.dbConfig import getDb
import pymongo

mongo_db = getDb()


class CounselingSession:
    def __init__(self):
        self.cs = mongo_db.counseling_session

    def create(self, data):
        result = self.cs.insert_one({
            'full-name': data["full-name"],
            'email': data["email"],
            'proposed-date': data["date"],
            'category': data["category"],
            'apointment-date': None,
        })
        return result.inserted_id

    def find_by_id(self, apointment_id):
        return self.cs.find_one({'_id': ObjectId(apointment_id)})

    def find_all(self):
        return list(self.cs.find())

    def search(self, query):
        return list(self.cs.find())

    def update(self, apointment_id, update_data):
        result = self.cs.update_one(
            {"_id": ObjectId(apointment_id)},
            {"$set": update_data}
        )
        return result.modified_count  # Return the number of documents updated

    def delete(self, apointment_id):
        return self.cs.delete_one({'_id': ObjectId(apointment_id)})

