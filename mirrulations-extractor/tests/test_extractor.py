import os
from pytest import fixture
from mirrextractor.extractor import Extractor


SAVE_DIR = 'saved'
SAVE_PATH = 'saved/saved.txt'


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

    Extractor.extract_pdf(
        os.path.join(absolute_path, 'pdfs/empty.pdf'),
        save_path)

    assert os.path.isfile(save_path)
