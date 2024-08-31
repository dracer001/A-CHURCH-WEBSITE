from bson.objectid import ObjectId
from models.dbConfig import getDb
import pymongo

mongo_db = getDb()


class EbookModel:
    def __init__(self):
        self.ebook = mongo_db.ebook
        self.ebook.create_index([("title", pymongo.ASCENDING)], unique=True)

    def model(self):
        return self.ebook

    @staticmethod
    def database():
        return mongo_db

    def create(self, book):
        result = self.ebook.insert_one({
            'title': book["ebook-title"],
            'author': book["ebook-author"],
            'summary': book["ebook-summary"],
            'file_id': book["file_id"],
            'image_id': book["image_id"],
            'tags': book.get("ebook-tags", None)
        })
        return result.inserted_id

    def find_by_id(self, book_id):
        return self.ebook.find_one({'_id': ObjectId(book_id)})

    def find_all(self):
        return list(self.ebook.find())

    def search(self, query, sort_key, order):
        return list(self.ebook.find(query).sort(sort_key, pymongo.DESCENDING)) if order == 'on' else\
            list(self.ebook.find(query).sort(sort_key, pymongo.ASCENDING))

    def update(self, book_id, update_data):
        print(update_data)
        result = self.ebook.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": update_data}
        )
        return result.modified_count  # Return the number of documents updated

    def delete(self, book_id):
        return self.ebook.delete_one({'_id': ObjectId(book_id)})