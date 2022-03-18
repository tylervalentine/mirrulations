from mirrmock.mock_document_count import create_mock_mongodb
from mirrdash.sum_mongo_counts import get_dockets_count, \
    get_documents_count, get_comments_count, get_done_counts,\
    get_attachments_count


def test_docket_counts():
    mock_db = create_mock_mongodb(1, 2, 3, 4)
    assert get_dockets_count(mock_db, 'mirrulations') == 1


def test_document_counts():
    mock_db = create_mock_mongodb(1, 2, 3, 4)
    assert get_documents_count(mock_db, 'mirrulations') == 2


def test_comment_counts():
    mock_db = create_mock_mongodb(1, 2, 3, 4)
    assert get_comments_count(mock_db, 'mirrulations') == 3


def test_attachment_counts():
    mock_db = create_mock_mongodb(1, 2, 3, 4)
    assert get_attachments_count(mock_db, 'mirrulations') == 4


def test_done_counts():
    mock_db = create_mock_mongodb(1, 2, 3, 4)
    assert get_done_counts(mock_db, 'mirrulations')['num_jobs_done'] == 10
