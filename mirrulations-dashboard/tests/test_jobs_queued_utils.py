'''from mirrdash.jobs_queued_utils import get_jobs_queued_stats, \
    get_jobs_queued_attachments, get_jobs_queued_comments, \
    get_jobs_queued_dockets, get_jobs_queued_documents
from mirrmock.mock_redis import MockRedisWithStorage


def test_jobs_queued_stats():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_attachments_queued', 1)
    mock_database.set('num_jobs_comments_queued', 2)
    mock_database.set('num_jobs_dockets_queued', 3)
    mock_database.set('num_jobs_documents_queued', 4)
    assert get_jobs_queued_stats(mock_database) == \
        {'num_jobs_attachments_queued': 1, 'num_jobs_comments_queued': 2,
            'num_jobs_dockets_queued': 3, 'num_jobs_documents_queued': 4}


def test_attachments_queued():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_attachments_queued', 5)
    assert get_jobs_queued_attachments(mock_database) == 5


def test_comments_queued():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_comments_queued', 5)
    assert get_jobs_queued_comments(mock_database) == 5


def test_dockets_queued():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_dockets_queued', 5)
    assert get_jobs_queued_dockets(mock_database) == 5


def test_documents_queued():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_documents_queued', 5)
    assert get_jobs_queued_documents(mock_database) == 5'''
