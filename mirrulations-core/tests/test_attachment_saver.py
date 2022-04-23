from mirrcore.attachment_saver import AttachmentSaver
from werkzeug.datastructures import FileStorage
import os, base64

def test_attachment_is_saved():
    attachment_saver = AttachmentSaver()
    files = {'results': {'test.pdf': base64.b64encode(open(os.path.join(os.getcwd(),'mirrulations-core/tests/test_files/test.pdf'), 'rb').read()).decode('ascii')}}
    assert attachment_saver.save(files, path=os.path.join(os.getcwd(), 'mirrulations-core/tests/test_put_files')) == 'saved'
