import os
from pytest import fixture
from mirrextractor.extractor import Extractor


SAVE_PATH = 'saved/saved.txt'


@fixture(autouse=True)
def remove_saved_file():
    absolute_path = os.path.dirname(__file__)
    path = os.path.join(absolute_path, SAVE_PATH)

    if os.path.isfile(path):
        os.remove(path)


def test_extractor_creates_saved_file():
    absolute_path = os.path.dirname(__file__)

    save_path = os.path.join(absolute_path, SAVE_PATH)

    Extractor.extract_pdf(
        os.path.join(absolute_path, 'pdfs/empty.pdf'),
        save_path)

    assert os.path.isfile(save_path)
