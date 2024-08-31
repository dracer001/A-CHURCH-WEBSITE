from datetime import datetime
from bson.objectid import ObjectId
from models.events import EventModel, EventRegModel, EventRegFormModel
from .validation import Validation
from flask import Flask, request, redirect, session, render_template, send_file
from werkzeug.utils import secure_filename
import gridfs
import io

events = EventModel()
event_form = EventRegFormModel()
event_reg = EventRegModel()

fs = gridfs.GridFS(events.database())


def addEvent(data, files):
    validator = Validation(data)
    messages = validator.required(('title', 'date', 'time', 'location', 'organizers'))
    if messages:
        print("messages")
        return messages, ""
    try:
        if 'flyer' in files and files['flyer'].filename != '':
            flyer = files['flyer']
            data["flyer_id"] = fs.put(flyer, filename=secure_filename(flyer.filename))
        else:
            data["flyer_id"] = None
        data["created_by"] = session["user_id"]
        data["created_at"] = datetime.now()
        event_id = events.create(data)
        print(event_id)
        return True, event_id
    except Exception as e:
        print("error: {}".format(e))
        return False, ""


def editEvent(event_id, data, files):
    try:
        event = events.find_by_id(event_id)
        if not event:
            return "event id not found"
        if data:
            validator = Validation(data)
            messages = validator.check_list(('title', 'date', 'time', 'location', 'event_info',
                                            'organizers', 'location_link', 'contact_info',))
            if messages:
                return messages

        if 'flyer' in files and files['flyer'].filename != '':
            flyer = files['flyer']
            data["flyer_id"] = fs.put(flyer, filename=secure_filename(flyer.filename))
            fs.delete(event['flyer_id'])
        data["updated_at"] = datetime.now()
        events.update(event_id, data)
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


def deleteEvent(event_id):
    try:
        event = events.find_by_id(event_id)
        if not event:
            return "event id not found"
        fs.delete(event['flyer_id'])
        events.delete(event_id)
        form = event_form.find_by_event(event_id)
        if form:
            event_form.delete(form['_id'])
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


def searchEvent(value, keys, sort_key, order):
    try:
        query = {
            '$or': [
                {key: {'$regex': value, '$options': 'i'}} for key in keys
            ]
        }
        return events.search(query, sort_key, order)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getEvent(event_id):
    try:
        return events.find_by_id(event_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getAllEvents():
    try:
        return events.find_all()
    except Exception as e:
        print("error: {}".format(e))
        return False


def get_file(file_id):
    try:
        grid_out = fs.get(ObjectId(file_id))
        file_data = grid_out.read()
        return file_data, grid_out
    except Exception as e:
        print(f"Error: {e}")
        return "File not found"


def createEventForm(data, event_id):
    try:
        form_id = event_form.create(data, event_id)
        events.update(event_id, {"form_id": ObjectId(form_id)})
        return True, form_id
    except Exception as e:
        print("error: {}".format(e))
        return False, ""


def editEventForm(form_id, data):
    try:
        event_id = event_form.update(form_id, data)
        return True
    except Exception as e:
        print("error: {}".format(e))


def deleteEventForm(form_id):
    try:
        event_form.delete(form_id)
        event_reg.deleteAll(form_id)
        event_id = events.find_by_form_id(form_id)
        events.update(event_id['_id'], {"form_id": None})
        return True
    except Exception as e:
        print("error: {}".format(e))


def getEventForm(form_id):
    try:
        event = event_form.find_by_id(form_id)
        return event
    except Exception as e:
        print("error: {}".format(e))


def getEventFormByEvent_id(event_id):
    try:
        form = event_form.find_by_event(event_id)
        return form
    except Exception as e:
        print("error: {}".format(e))


# [
#     {
#         formEL: input,
#         elType: text,
#         elName: fullname,
#         options: []
#     }
# ]


def addEventReg(event_id, form_id, data):
    try:
        event_id = event_reg.create(event_id, form_id, data)
        return True
    except Exception as e:
        print("error: {}".format(e))


def editEventReg(reg_id, data):
    try:
        event_reg.update(reg_id, data)
        return True
    except Exception as e:
        print("error: {}".format(e))


def deleteEventReg(reg_id):
    try:
        event_reg.delete(reg_id)
        return True
    except Exception as e:
        print("error: {}".format(e))


def getEventReg(reg_id):
    try:
        return event_reg.find_by_id(reg_id)
    except Exception as e:
        print("error: {}".format(e))


def getAllEventReg(event_id):
    try:
        return event_reg.find_by_event(event_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def reset_registration():
    try:
        return event_reg.reset()
    except Exception as e:
        print("error: {}".format(e))
        return False


def reset(field, value):
    try:
        event = getAllEvents()
        for event_item in event:
            events.update(event_item['_id'], {field: value})
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False
