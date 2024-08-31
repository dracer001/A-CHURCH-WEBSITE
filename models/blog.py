from flask_pymongo import ObjectId
from models.dbConfig import getDb
import pymongo

mongo_db = getDb()


class BlogModel:
    def __init__(self):
        self.blog = mongo_db.blog

    def model(self):
        return self.blog

    @staticmethod
    def database():
        return mongo_db

    def create(self, blog):
        result = self.blog.insert_one({
            'title': blog["title"],
            'content': blog["content"],
            'image-id': blog.get('image_id', None),
            'tags': blog.get('tags', None),
            'blogger': ObjectId(blog["blogger"]),
            'post-date': blog["post-date"],
            'update-date': None,
            'comments': []
        })
        return result.inserted_id

    def find_by_id(self, blog_id):
        return self.blog.find_one({'_id': ObjectId(blog_id)})

    def find_all(self):
        return list(self.blog.find())

    def search(self, query, sort_key, order):
        return list(self.blog.find(query).sort(sort_key, pymongo.DESCENDING)) if order == 'on' else\
            list(self.blog.find(query).sort(sort_key, pymongo.ASCENDING))

    def update(self, blog_id, update_data):
        result = self.blog.update_one(
            {"_id": ObjectId(blog_id)},
            {"$set": update_data}
        )
        return result.modified_count  # Return the number of documents updated

    def delete(self, blog_id):
        return self.blog.delete_one({'_id': ObjectId(blog_id)})


class BloggerModel:
    def __init__(self):
        self.blogger = mongo_db.blogger
        self.blogger.create_index([("username", pymongo.ASCENDING)], unique=True)
        self.blogger.create_index([("email", pymongo.ASCENDING)], unique=True)

    def model(self):
        return self.blogger

    @staticmethod
    def database():
        return mongo_db

    def create(self, blogger):
        result = self.blogger.insert_one({
            'full-name': blogger["full-name"],
            'username': blogger['username'],
            'email': blogger["email"],
            'password': blogger["password"],
            'bio': blogger.get("bio", None),
            'image_id': blogger.get("image-id", None),
            'status': blogger.get("status", "pending")
        })
        return result.inserted_id

    def find_by_id(self, blogger_id):
        return self.blogger.find_one({'_id': ObjectId(blogger_id)})

    def find_all(self):
        return list(self.blogger.find())

    def search(self, query):
        return list(self.blogger.find(query))

    def update(self, blogger_id, update_data):
        result = self.blogger.update_one(
            {"_id": ObjectId(blogger_id)},
            {"$set": update_data}
        )
        return result.modified_count  # Return the number of documents updated

    def delete(self, blogger_id):
        return self.blogger.delete_one({'_id': ObjectId(blogger_id)})

    def reset_all(self):
        return self.blogger.drop()
