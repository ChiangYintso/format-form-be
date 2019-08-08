from pymongo import MongoClient


class MongoDB:
    def __init__(self, uri):
        self.__uri = uri
        self.client = MongoClient(self.__uri)
        self.db = self.client['format_form']
