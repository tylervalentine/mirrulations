import os
import shutil
from pytest import fixture
from mirrextractor.extractor import Extractor




# SAVE_DIR = 'test-area'
# SAVE_PATH = SAVE_DIR + '/saved.txt'

def mock_pdf_extraction(mocker):
    mocker.patch.object(
        Extractor,
        '_extract_pdf',
        return_value=None
    )

def test_extract_pdf(capfd, mocker):
    mock_pdf_extraction(mocker)
    Extractor.extract_text('a.pdf', 'b.txt')
    assert "Extracting text from a.pdf" in capfd.readouterr()[0]

def test_extract_non_pdf(capfd, mocker):
    mock_pdf_extraction(mocker)
    Extractor.extract_text('a.docx', 'b.txt')
    assert "FAILURE: attachment doesn't have appropriate extension a.docx" in capfd.readouterr()[0]

