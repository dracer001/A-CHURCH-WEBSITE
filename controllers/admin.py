from flask import render_template, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId
from models.admin import AdminUser
from .validation import Validation

admin_user = AdminUser()


def authAdmin():
    user_id = session.get('user_id')
    if user_id is None:
        g.admin = None
    else:
        g.admin = admin_user.find_by_id(user_id)


def createAdminUser(data, s_user=False):
    if not g.admin and admin_user.get_super():
        return "Super User Already Exists, cannot create duplicate"
    validator = Validation(data)
    messages = validator.required(('username', 'email'))
    if messages:
        return messages
    try:
        user = admin_user.search(data["username"])
        if user:
            return "user already exists"
        if s_user:
            password = data["password"]
        else:
            password = data["username"] + "123"
        password = generate_password_hash(password)
        admin_user.create(username=data["username"], email=data["email"], password=password, s_user=s_user)
        return True
    except KeyError:
        print("Key error Found")
        return False
    except Exception as e:
        print("error: {}".format(e))
        return False


def getSuperUser():
    if user := admin_user.get_super():
        print(user)
        return "Super User Already Exists, cannot create duplicate"
    else:
        return False


def editAdminUser(data, user_id):
    data = data.to_dict()
    validator = Validation(data)
    messages = validator.check_list(('username', 'email', 'password'))
    if messages:
        return messages
    try:
        user = admin_user.find_by_id(user_id)
        if not user:
            return "user not found"
        if 'password' in data:
            if g.admin["password"] != data["password"]:
                data["password"] = generate_password_hash(data["password"])
            else:
                del data["password"]
        admin_user.update(user_id, data)
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


def deleteAdminUser(user_id):
    try:
        return True if admin_user.delete(user_id).deleted_count > 0 else "Could not delete user {}".format(user_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def barnAdminUser(data):
    print("data = ", data, "datatype = ", type(data))
    barn_ids = []
    try:
        for id in data:
            print("id = ", id)
            barn_ids.append(id) if admin_user.update(id, {"barn": True}) > 0 else ""
        return barn_ids
    except Exception as e:
        print("error {}".format(e))
        return False


def unBarnAdminUser(data):
    unbarn_ids = []
    try:
        for id in data:
            unbarn_ids.append(id) if admin_user.update(id, {"barn": False}) > 0 else ""
        return unbarn_ids
    except Exception as e:
        print("error {}".format(e))
        return False


def getAdminUsers():
    try:
        return admin_user.find_all()
    except Exception as e:
        print("error {}".format(e))
        return False


def getAdminUser(user_id):
    try:
        return admin_user.find_by_id(user_id)
    except Exception as e:
        print("error {}".format(e))
        return False


def loginAdmin(data):
    validator = Validation(data)
    messages = validator.required(('username', 'password'))
    if messages:
        return messages
    try:
        user = admin_user.search(data["username"])
        if not user:
            return "user not found"
        user = user[0]
        session['user_id'] = str(user['_id'])
        return True if check_password_hash(user['password'], data['password']) else "incorrect password"
    except Exception as e:
        print("error: {}".format(e))
        return False
#     return render_template('media/ebook_file.html')
#

def reset(field, value):
    try:
        admins = getAdminUsers()
        for admin in admins:
            admin_user.update(admin['_id'], {field:value})
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False
