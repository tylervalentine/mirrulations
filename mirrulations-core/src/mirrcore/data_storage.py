import pymongo


class DataStorage:
    def __init__(self):
        database = pymongo.MongoClient('mongo', 27017)['mirrulations']
        self.dockets = database['dockets']
        self.documents = database['documents']
        self.comments = database['comments']

    def exists(self, search_element):
        result_id = search_element['id']

        return self.dockets.count_documents({'id': result_id}) > 0 or \
            self.documents.count_documents({'id': result_id}) > 0 or \
            self.comments.count_documents({'id': result_id}) > 0
