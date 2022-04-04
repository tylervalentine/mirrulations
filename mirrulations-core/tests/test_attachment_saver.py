from mirrcore.attachment_saver import AttachmentSaver
from werkzeug.datastructures import FileStorage
import os

def test_attachment_is_saved():
    attachment_saver = AttachmentSaver()
    with open('mirrulations-core/tests/test.pdf', 'rb') as fp:
        file = FileStorage(fp, filename='test.pdf')
        assert attachment_saver.save(file, path=os.path.join(os.getcwd(), 'mirrulations-core/tests')) == 'saved'
