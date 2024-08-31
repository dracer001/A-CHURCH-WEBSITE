from bson.objectid import ObjectId
from models.counselings import CounselingSession
from .validation import Validation

cs = CounselingSession()


def addSession(data):
    validator = Validation(data)
    messages = validator.required(('full-name', 'email', 'date', 'category'))
    if messages:
        return messages
    try:
        cs.create(data)
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


def editSession(data, session_id):
    validator = Validation(data)
    messages = validator.check_list(('full-name', 'email', 'apointment-date', 'category', 'proposed-date', 'status'))
    if messages:
        return messages
    try:
        cs.update(session_id, data)
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


def deleteSession(session_id):
    try:
        return True if cs.delete(session_id).deleted_count > 0 else "Could not delete session {}".format(session_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getAllSession():
    try:
        return cs.find_all()
    except Exception as e:
        print("error {}".format(e))
        return False


def getSession(session_id):
    try:
        return cs.find_by_id(session_id)
    except Exception as e:
        print("error {}".format(e))
        return False

