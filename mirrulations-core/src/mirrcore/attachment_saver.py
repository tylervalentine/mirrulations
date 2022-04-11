import os

class AttachmentSaver():
    def __init__(self):
        pass

    def save(self, file, path='/capstone2022/attachments'):
        file.save(os.path.join(path, file.filename))
        return 'saved'