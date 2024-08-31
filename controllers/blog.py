import uuid
from datetime import datetime
from bson.objectid import ObjectId
from models.blog import BlogModel, BloggerModel
from .validation import Validation
from werkzeug.utils import secure_filename
import gridfs
import io

from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, g


blog = BlogModel()
blogger = BloggerModel()
fs_blog = gridfs.GridFS(blog.database())
fs_blogger = gridfs.GridFS(blogger.database())


def addBlog(data, files):

    validator_blog = Validation(data)
    validator_files = Validation(files)

    # Validate required fields
    messages = validator_blog.required(('title', 'content'))
    if messages:
        return False, messages

    try:
        # Handle blog image
        blog_image = files.get('blog-image', None)
        if blog_image:
            if validator_files.allowed_files(blog_image, {'image/png', 'image/jpeg', 'image/gif'}):
                data["image_id"] = fs_blog.put(blog_image, filename=secure_filename(blog_image.filename))
            else:
                return False, "Image type not allowed"

        # Split tags into a list
        if "tags" in data:
            data["tags"] = data['tags'].split(',')

        # Process blog content
        processed_content = []
        for content in data["content"]:
            if (content["field-type"] == "text" or content["field-type"] == "sub-header") and content["content"]:
                content["content"] = content["content"].strip()
            elif (content["field-type"] == "ul" or content["field-type"] == "ol") and content["content"]:
                content["content"] = [item.strip() for item in content["content"]]
            elif content["field-type"] == "image" and content["content"]:
                blog_image = files.get('blog-image', None)
                filename = content["content"]
                if filename in files:
                    file = files[filename]
                    if validator_files.allowed_files(file, {'image/png', 'image/jpeg', 'image/gif'}):
                        content["content"] = fs_blog.put(file, filename=secure_filename(file.filename))
                        # content["content"] = file_id
            processed_content.append(content)

        # Assign processed content back to data
        data["content"] = processed_content

        # Additional blog fields
        data['blogger'] = g.user['_id']
        data['post-date'] = datetime.now()

        blog_id = blog.create(data)

        return True, blog_id

    except Exception as e:
        print("error: {}".format(e))
        return False, str(e)


def editBlog(blog_id, data, files):
    try:
        blog_item = blog.find_by_id(blog_id)
        if not blog_item:
            return "book id not found"

        if data:
            validator_book = Validation(data)
            messages_book = validator_book.check_list(('title', 'tags', 'content'))
            if messages_book:
                return messages_book
            if "tags" in data:
                data["tags"] = data["tags"].split(',')

        validator_files = Validation(files)
        blog_image = files['blog_image']
        if blog_image and validator_files.allowed_files(blog_image, {'image/png', 'image/jpeg', 'image/gif'}):
            data["image_id"] = fs_blog.put(blog_image, filename=secure_filename(blog_image.filename))
        blog.update(blog_id, data)
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


def deleteBlog(blog_id):
    try:
        blog_item = blog.find_by_id(blog_id)
        if not blog_item:
            return "blog id not found"
        fs_blog.delete(blog_item['image_id'])
        return True if blog.delete(blog_id).deleted_count > 0 else "Could not delete user {}".format(blog_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def searchBlog(value, keys, sort_key, order):
    try:
        query = {
            '$or': [
                {key: {'$regex': value, '$options': 'i'}} for key in keys
            ]
        }
        return blog.search(query, sort_key, order)
    except Exception as e:
        print("error: {}".format(e))
        return False


def searchBloggerBlog(blogger_id, value, keys, sort_key, order):
    try:
        query = {
            'blogger': blogger_id,
            '$or': [
                {key: {'$regex': value, '$options': 'i'}} for key in keys
            ]
        }
        return blog.search(query, sort_key, order)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getBloggerBlog(blogger_id):
    try:
        query = {
            'blogger': blogger_id
        }
        return blog.search(query, "post-date", "off")
    except Exception as e:
        print("error: {}".format(e))
        return False


def getBlog(blog_id):
    try:
        return blog.find_by_id(blog_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getAllBlog():
    try:
        return blog.find_all()
    except Exception as e:
        print("error: {}".format(e))
        return False


def addComment(blog_id, data):
    validator = Validation(data)
    if messages := validator.required(('comment', 'commentor')):
        return messages
    try:
        blog_item = blog.find_by_id(blog_id)
        if not blog_item:
            return "blog_id not found"
        data["comment_date_time"] = datetime.now()
        data['comment_id'] = uuid.uuid4()
        blog_item["comments"].append(blog_item)
        blog.update(blog_id, blog_item)
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


def editComment(blog_id, comment_id, data):
    validator = Validation(data)
    if messages := validator.check_list(('comment', 'commentor')):
        return messages
    try:
        blog_item = blog.find_by_id(blog_id)
        if not blog_item:
            return "blog_id not found"
        data["comment_date_time_update"] = datetime.now()

        for comment in blog_item["comment"]:
            if comment["comment_id"] == comment_id:
                comment.update(data)
                break
        # comment = [comment for comment in blog_item["comments"] if comment["comment_id"] == comment_id]
        # comment[0].update(data)
        blog.update(blog_id, blog_item)
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


def deleteComment(blog_id, comment_id):
    try:
        blog_item = blog.find_by_id(blog_id)
        if not blog_item:
            return "blog_id not found"

        for comment in blog_item["comments"]:
            if comment["comment_id"] == comment_id:
                blog_item["comments"].remove(comment)
                break
        # comment = [comment for comment in blog_item["comments"] if comment["comment_id"] == comment_id]
        # comment[0].update(data)
        blog.update(blog_id, blog_item)
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


# BLOGGER CONTROLLER
def createBlogger(data):
    validator = Validation(data)
    messages = validator.required(('full-name', 'username', 'email', 'password'))
    if messages:
        return False, messages
    data["password"] = generate_password_hash(data["password"])
    try:
        if blogger.search({"username": data['username']}):
            return False, "username already exists"
        if blogger.search({"email": data['email']}):
            return False, "email already registered"
        print(data)
        blogger_id = blogger.create(data)
        return True, blogger_id
    except Exception as e:
        print("error: {}".format(e))
        return False, e


def editBlogger(blogger_id, data, files):
    try:
        blogger_item = blogger.find_by_id(blogger_id)
        if not blogger_item:
            return "user id not found"

        if data:
            validator_blogger = Validation(data)
            messages = validator_blogger.check_list(('full-name', 'email', 'bio', 'status'))
            if messages:
                return messages
        validator_files = Validation(files)
        blogger_image = files.get('blogger-image', None)
        if blogger_image and validator_files.allowed_files(blogger_image, {'image/png', 'image/jpeg', 'image/gif'}):
            data["image_id"] = fs_blogger.put(blogger_image, filename=secure_filename(blogger_image.filename))
        blogger.update(blogger_id, data)
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


def deleteBlogger(blogger_id):
    try:
        blogger_item = blogger.find_by_id(blogger_id)
        if not blogger_item:
            return "blogger id not found"
        fs_blogger.delete(blogger_item['image_id'])
        return True if blogger.delete(blogger_id).deleted_count > 0 else "Could not delete user {}".format(blogger_id)
    except Exception as e:
        print("error: {}".format(e))
        return False
    
    
def changePassword(blogger_id, old_p, new_p):
    try:
        blogger_item = blogger.find_by_id(blogger_id)
        if not blogger_item:
            return "blogger id not found"
        if check_password_hash(blogger_item['password'], old_p):
            new_p_hash = generate_password_hash(new_p)
            blogger.update(blogger_id, {"password": new_p_hash})
            return True
        return "password mismatch"
    except Exception as e:
        print("error: {}".format(e))
        return False


# def searchBlogger(data):
#     try:
#         return blogger.search(data)
def searchBlogger(value, keys):
    try:
        query = {
            '$or': [
                {key: {'$regex': value, '$options': 'i'}} for key in keys
            ]
        }
        return blogger.search(query)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getBlogger(blogger_id):
    try:
        return blogger.find_by_id(blogger_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getAllBlogger():
    try:
        return blogger.find_all()
    except Exception as e:
        print("error: {}".format(e))
        return False


def barnBlogger(data):
    try:
        barn_ids = [blogger_id for blogger_id in data if blogger.update(blogger_id, {"barn": True})]
        return barn_ids
    except Exception as e:
        print("error {}".format(e))
        return False


def unBarnAdminUser(data):
    try:
        unbarn_ids = [blogger_id for blogger_id in data if blogger.update(blogger_id, {"barn": False})]
        return unbarn_ids
    except Exception as e:
        print("error {}".format(e))
        return False


def authBlogger():
    blogger_id = session.get('blogger_id')
    if blogger_id is None:
        g.user = None
    else:
        g.user = blogger.find_by_id(blogger_id)


def loginBlogger(data):
    validator = Validation(data)
    messages = validator.required(('username', 'password'))
    if messages:
        return False, messages
    try:

        user = blogger.search({
            '$or': [
                {'username': {'$regex': data['username'], '$options': 'i'}},
                {'email': {'$regex': data['username']}},
            ]
        })
        if not user:
            return False, "user not found"
        user = user[0]
        if check_password_hash(user['password'], data['password']):
            session['user_id'] = str(user['_id'])
            return True, user['_id']
        return False, "incorrect password"
    except Exception as e:
        print("error: {}".format(e))
        return False, e


def get_blog_img(file_id):
    try:
        grid_out = fs_blog.get(ObjectId(file_id))
        file_data = grid_out.read()
        return file_data, grid_out
    except Exception as e:
        print(f"Error: {e}")
        return "File not found"




def resetAllBlogger():
    try:
        blogger.reset_all()
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


