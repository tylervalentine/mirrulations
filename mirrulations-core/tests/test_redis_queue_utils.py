'''from mirrcore.redis_queue_utils import change_queue_counter
from mirrmock.mock_redis import MockRedisWithStorage


def test_attachments_queue_incr():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_attachments_queued', 5)
    change_queue_counter(mock_database, 'attachments', True)
    assert mock_database.get('num_jobs_attachments_queued') == 6


def test_attachments_queue_decr():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_attachments_queued', 5)
    change_queue_counter(mock_database, 'attachments', False)
    assert mock_database.get('num_jobs_attachments_queued') == 4

def test_comments_queue_incr():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_comments_queued', 5)
    change_queue_counter(mock_database, 'comments', True)
    assert mock_database.get('num_jobs_comments_queued') == 6


def test_comments_queue_decr():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_comments_queued', 5)
    change_queue_counter(mock_database, 'comments', False)
    assert mock_database.get('num_jobs_comments_queued') == 4

def test_dockets_queue_incr():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_dockets_queued', 5)
    change_queue_counter(mock_database, 'dockets', True)
    assert mock_database.get('num_jobs_dockets_queued') == 6


def test_dockets_queue_decr():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_dockets_queued', 5)
    change_queue_counter(mock_database, 'dockets', False)
    assert  mock_database.get('num_jobs_dockets_queued') == 4


def test_documents_queue_incr():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_documents_queued', 5)
    change_queue_counter(mock_database, 'documents', True)
    assert mock_database.get('num_jobs_documents_queued') == 6


def test_documents_queue_decr():
    mock_database = MockRedisWithStorage()
    mock_database.set('num_jobs_documents_queued', 5)
    change_queue_counter(mock_database, 'documents', False)
    assert mock_database.get('num_jobs_documents_queued') == 4'''