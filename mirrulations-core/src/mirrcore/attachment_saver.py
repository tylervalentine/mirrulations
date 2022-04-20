import os
import base64

class AttachmentSaver():
    def __init__(self):
        pass

    def save(self, data, path=os.path.join(os.getcwd())):
        for key in data['results'].keys():
            with open(os.path.join(path, key), 'wb') as f:
                f.write(base64.b64decode(data['results'][key].encode('ascii')))
        return 'saved'