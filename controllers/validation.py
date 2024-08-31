import mimetypes


class Validation:
    def __init__(self, data):
        self.data = data

    def required(self, required_list):
        msg_list = []
        for item in required_list:
            if item not in self.data:
                msg_list.append("{} not found".format(item))
            elif self.data[item] == "":
                msg_list.append("{} is empty".format(item))
        return msg_list

    def check_list(self, allowable_list):
        msg_list = []
        for key, value in self.data.items():
            if key not in allowable_list:
                msg_list.append("{} not allowed".format(key))
            # elif value == "":
            #     msg_list.append("{} is empty".format(key))
        return msg_list

    # @staticmethod
    def allowed_files(self, file, file_types):
        mime_type, _ = mimetypes.guess_type(file.filename)
        return mime_type in file_types

