from bson.objectid import ObjectId
from models.ebook import EbookModel
from .validation import Validation
from flask import Flask, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
import gridfs
import io

ebook = EbookModel()
fs = gridfs.GridFS(ebook.database())


def addEbook(data, files):
    validator_book = Validation(data)
    validator_files = Validation(files)
    messages_book = validator_book.required(('ebook-title', 'ebook-author', 'ebook-summary'))
    messages_files = validator_files.required(('ebook-file', 'ebook-image'))
    if messages_book or messages_files:
        return messages_book + messages_files
    try:
        book_file = files['ebook-file']
        book_image = files['ebook-image']
        data["file_id"] = fs.put(book_file, filename=secure_filename(book_file.filename))
        data["image_id"] = fs.put(book_image, filename=secure_filename(book_image.filename))
        if 'ebook-tags' in data:
            data["ebook-tags"] = data['ebook-tags'].split(',')
        book_id = ebook.create(data)
        return True
    except Exception as e:
        print("error: {}".format(e))
        return False


def editEbook(book_id, data, files):
    try:
        book = ebook.find_by_id(book_id)
        if not book:
            return "book id not found"

        if data:
            validator_book = Validation(data)
            messages_book = validator_book.check_list(('title', 'author', 'summary', 'tags'))
            messages_book += validator_book.required(('title', 'author', 'summary'))

            if messages_book:
                return messages_book
            if "tags" in data:
                data["tags"] = data["tags"].split(',')

        if 'ebook-file' in files and files['ebook-file'].filename != '':
            book_file = files['book-file']
            file_id = fs.put(book_file, filename=secure_filename(book_file.filename))
            fs.delete(book['file_id'])
            data["file_id"] = file_id

        if 'ebook-image' in files and files['ebook-image'].filename != '':
            book_image = files['ebook-image']
            image_id = fs.put(book_image, filename=secure_filename(book_image.filename))
            fs.delete(book['image_id'])
            data["image_id"] = image_id
        # print(data)
        ebook.update(book_id, data)
        return True
    except Exception as e:
        print("error: {}".format(e))
    return  False


def deleteEbook(book_id):
    try:
        book = ebook.find_by_id(book_id)
        if not book:
            return "book id not found"
        fs.delete(book['file_id'])
        fs.delete(book['image_id'])
        return True if ebook.delete(book_id).deleted_count > 0 else "Could not delete user {}".format(book_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def searchEbooks(value, keys, sort_key, order):
    try:
        query = {
            '$or': [
                {key: {'$regex': value, '$options': 'i'}} for key in keys
            ]
        }
        return ebook.search(query, sort_key, order)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getEbook(book_id):
    try:
        return ebook.find_by_id(book_id)
    except Exception as e:
        print("error: {}".format(e))
        return False


def getAllEbook():
    try:
        return ebook.find_all()
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





