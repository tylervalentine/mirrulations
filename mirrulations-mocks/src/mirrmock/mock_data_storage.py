
class MockDataStorage:

    def __init__(self):
        self.added = []
        self.attachments_added = []
        self.collection_size = 1

    def exists(self, search_element=None):
        if search_element is not None:
            return False
        return False

    def add(self, data):
        self.added.append(data)

    def add_attachment(self, data):
        self.attachments_added.append(data)

    def get_collection_size(self):
        return self.collection_size
