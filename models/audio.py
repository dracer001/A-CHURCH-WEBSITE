from flask_pymongo import ObjectId
from models.dbConfig import getDb
import pymongo

mongo_db = getDb()


class AudioModel:
    def __init__(self):
        self.audio = mongo_db.audio
        self.audio.create_index([("title", pymongo.ASCENDING)], unique=True)

    def model(self):
        return self.audio

    @staticmethod
    def database():
        return mongo_db

    def create(self, audio):
        result = self.audio.insert_one({
            'title': audio["audio-title"],
            'file_id': audio["file_id"],
            'image_id': audio.get("image_id") or "",
            'artist': audio["audio-artist"] or "Unknown",
            'tags': audio["audio-tags"] or None,
        })
        return result.inserted_id

    def find_by_id(self, audio_id):
        return self.audio.find_one({'_id': ObjectId(audio_id)})

    def find_all(self):
        return list(self.audio.find())

    def search(self, query):
        return list(self.audio.find({
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'tags': {'$regex': query, '$options': 'i'}},
            ]
        }))

    def update(self, audio_id, update_data):
        print("models:", update_data['audio-tags'])
        result = self.audio.update_one(
            {"_id": ObjectId(audio_id)},
            {"$set": update_data}
        )
        return result.modified_count  # Return the number of documents updated

    def delete(self, audio_id):
        return self.audio.delete_one({'_id': ObjectId(audio_id)})