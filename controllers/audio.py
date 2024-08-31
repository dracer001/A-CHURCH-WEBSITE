from flask import make_response
from bson.objectid import ObjectId
from models.audio import AudioModel
from .validation import Validation
from werkzeug.utils import secure_filename
import gridfs
import io

audio = AudioModel()
fs = gridfs.GridFS(audio.database())


def addAudio(data, files):
    validator_audio = Validation(data)
    validator_files = Validation(files)
    messages_audio = validator_audio.required(('audio-title',))
    messages_files = validator_files.required(('audio-file',))
    if messages_audio or messages_files:
        return messages_audio + messages_files
    try:
        audio_file = files['audio-file']
        data["file_id"] = fs.put(audio_file, filename=secure_filename(audio_file.filename))
        if 'audio-image' in files and files['audio-image'].filename != "":
            audio_image = files['audio-image']
            data["image_id"] = fs.put(audio_image, filename=secure_filename(audio_image.filename))
        if 'audio-tags' in data:
            data["audio-tags"] = data['audio-tags'].split(',')
        audio_id = audio.create(data)
        return True
    except Exception as e:
        print("error: {}".format(e))


def editAudio(audio_id, data, files):
    try:
        audio_item = audio.find_by_id(audio_id)
        if not audio_item:
            return "audio id not found"

        if data:
            validator = Validation(data)
            message = validator.check_list(('audio-title', 'audio-artist', 'audio-tags'))
            message += validator.required(('audio-title',))
            if message:
                return message
            if "audio-tags" in data:
                print(data['audio-tags'])
                data["tags"] = data["audio-tags"].split(',')

        if 'audio-file' in files and files['audio-file'].filename != '':
            audio_file = files['audio-file']
            file_id = fs.put(audio_file, filename=secure_filename(audio_file.filename))
            fs.delete(audio_item['file_id'])
            data["file_id"] = file_id

        if 'audio-image' in files and files['audio-image'].filename != "":
            audio_image = files['audio-image']
            image_id = fs.put(audio_image, filename=secure_filename(audio_image.filename))
            fs.delete(audio_item['image_id'])
            data['image_id'] = image_id
        audio.update(audio_id, data)
        return True
    except Exception as e:
        print("error: {}".format(e))
    return  False


def deleteAudio(audio_id):
    try:
        audio_item = audio.find_by_id(audio_id)
        print(audio_item)
        if not audio_item:
            return "audio_item id not found"
        fs.delete(audio_item['file_id'])
        fs.delete(audio_item['image_id'])
        return True if audio.delete(audio_item['_id']).deleted_count > 0 else "Could not delete user {}".format(audio_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getAudio(audio_id):
    try:
        return audio.find_by_id(audio_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getAllAudio():
    try:
        return audio.find_all()
    except Exception as e:
        print("error: {}".format(e))
        return False


def downloadAudio(audio_id):
    try:
        audio_item = audio.find_by_id(audio_id)
        if not audio_item:
            return "Audio Not Found"
        file_id = audio_item['file_id']
        file_data = fs.get(file_id)
        return file_data
    except Exception as e:
        print("error: {}".format(e))


def get_file(file_id):
    try:
        grid_out = fs.get(ObjectId(file_id))
        file_data = grid_out.read()
        return file_data, grid_out
    except Exception as e:
        print(f"Error: {e}")
        return "File not found"


def reset(field, value):
    try:
        audios = getAllAudio()
        for audio_item in audios:
            audio.update(audio_item['_id'], {field:value})
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False
