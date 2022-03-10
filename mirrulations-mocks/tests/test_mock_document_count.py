
from mirrmock.mock_document_count import create_mock_mongodb

def test_mock_document_count():
    mock_db = create_mock_mongodb(1, 2, 3)

    assert mock_db['mirrulations']['dockets'].count_documents({}) == 1
    assert mock_db['mirrulations']['documents'].count_documents({}) == 2
    assert mock_db['mirrulations']['comments'].count_documents({}) == 3