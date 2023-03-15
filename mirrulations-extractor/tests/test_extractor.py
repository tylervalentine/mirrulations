import os
import shutil
from pytest import fixture
from mirrextractor.extractor import Extractor


SAVE_DIR = 'test-area'
SAVE_PATH = SAVE_DIR + '/saved.txt'


@fixture(autouse=True)
def remove_saved_file():
    absolute_path = os.path.dirname(__file__)
    save_dir = os.path.join(absolute_path, SAVE_DIR)
    save_path = os.path.join(absolute_path, SAVE_PATH)

    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    if os.path.isfile(save_path):
        os.remove(save_path)


def test_extractor_creates_saved_file():
    absolute_path = os.path.dirname(__file__)

    save_path = os.path.join(absolute_path, SAVE_PATH)

    Extractor.extract_text(
        os.path.join(absolute_path, 'pdfs/empty.pdf'),
        save_path)

    assert os.path.isfile(save_path)


def test_extractor_extracts_pdf_with_text_a():
    absolute_path = os.path.dirname(__file__)

    save_path = os.path.join(absolute_path, SAVE_PATH)

    Extractor.extract_text(
        os.path.join(absolute_path, 'pdfs/a.pdf'),
        save_path)

    with open(save_path, "r", encoding="utf-8") as in_file:
        text = in_file.read()

    assert text.strip() == 'a'


def test_extractor_doesnt_save_non_pdf():
    absolute_path = os.path.dirname(__file__)

    save_path = os.path.join(absolute_path, SAVE_PATH)

    Extractor.extract_text(
        os.path.join(absolute_path, 'pdfs/a.docx'),
        save_path)

    assert not os.path.isfile(save_path)


def test_error_when_file_is_already_open():
    absolute_path = os.path.dirname(__file__)

    file_name = 'a.pdf'
    attachment_path = os.path.join(absolute_path, 'pdfs/' + file_name)
    copy_path = os.path.join(absolute_path, SAVE_DIR + '/' + file_name)

    shutil.copy(attachment_path, copy_path)

    save_path = os.path.join(absolute_path, SAVE_PATH)
    
    # File will be open at the same time we are trying to extract it.
    with open(copy_path, "w", encoding="utf-8") as _:
        Extractor.extract_text(copy_path, save_path)

    assert not os.path.isfile(save_path)
