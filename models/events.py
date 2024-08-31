from bson.objectid import ObjectId
from models.dbConfig import getDb
import pymongo

mongo_db = getDb()


class EventModel:
    def __init__(self):
        self.events = mongo_db.events
        self.events.create_index([("title", pymongo.ASCENDING)], unique=True)

    def model(self):
        return self.events

    @staticmethod
    def database():
        return mongo_db

    def create(self, event):
        result = self.events.insert_one({
            'title': event["title"],
            'date': event["date"],
            'time': event["time"],
            'location': event["location"],
            'location_link': event.get("location_link", None),
            'event_info': event["event-info"],
            'organizers': event["organizers"],
            'flyer_id': event["flyer_id"],
            'created_by': ObjectId(event["created_by"]),
            'created_at': event["created_at"],
            'contact_info': event.get("contact-info", "UBCMx Gidan-Kwano Minna")
        })
        return result.inserted_id

    def find_by_id(self, event_id):
        return self.events.find_one({'_id': ObjectId(event_id)})

    def find_by_form_id(self, form_id):
        return self.events.find_one({'form_id': ObjectId(form_id)})

    def find_all(self):
        return list(self.events.find())

    def search(self, query, sort_key, order):
        return list(self.events.find(query).sort(sort_key, pymongo.DESCENDING)) if order == 'on' else\
            list(self.events.find(query).sort(sort_key, pymongo.ASCENDING))

    def update(self, event_id, update_data):
        result = self.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": update_data}
        )
        return result.modified_count  # Return the number of documents updated

    def delete(self, event_id):
        return self.events.delete_one({'_id': ObjectId(event_id)})
    
  
class EventRegFormModel:
    def __init__(self):
        self.reg_form = mongo_db.event_reg_form
        self.reg_form.create_index([("event_id", pymongo.ASCENDING)], unique=True)

    def model(self):
        return self.reg_form

    def create(self, reg_form, event_id):
        result = self.reg_form.insert_one({
            "form": reg_form,
            "event_id": event_id
        })
        return result.inserted_id

    def find_by_id(self, form_id):
        return self.reg_form.find_one({'_id': ObjectId(form_id)})

    def find_by_event(self, event_id):
        return self.reg_form.find_one({'event_id': event_id})

    def update(self, form_id, update_data):
        result = self.reg_form.update_one(
            {"_id": ObjectId(form_id)},
            {"$set": update_data}
        )
        return result.modified_count  # Return the number of documents updated

    def delete(self, event_id):
        return self.reg_form.delete_one({'_id': ObjectId(event_id)})


class EventRegModel:
    def __init__(self):
        self.event_reg = mongo_db.event_reg
        self.event_reg.create_index([("event_id", pymongo.ASCENDING)])
        # self.event_reg.drop_indexes()

    def model(self):
        return self.event_reg

    def create(self, event_id, form_id, data):
        result = self.event_reg.insert_one({
            "event_id": ObjectId(event_id),
            "form_id": ObjectId(form_id),
            "data": data,
        })
        return result.inserted_id

    def find_by_id(self, reg_id):
        return self.event_reg.find_one({'_id': ObjectId(reg_id)})

    def find_by_event(self, event_id):
        return list(self.event_reg.find({'event_id': ObjectId(event_id)}))

    def update(self, reg_id, update_data):
        result = self.event_reg.update_one(
            {"_id": ObjectId(reg_id)},
            {"$set": update_data}
        )
        return result.modified_count  # Return the number of documents updated

    def delete(self, event_id):
        return self.event_reg.delete_one({'_id': ObjectId(event_id)})

    def deleteAll(self, form_id):
        return self.event_reg.delete_many({"form_id": form_id})

    def reset(self,):
        return self.event_reg.drop()
