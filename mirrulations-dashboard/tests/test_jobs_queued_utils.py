from operator import ge
from unittest import mock
from webbrowser import get
from fakeredis import FakeRedis
from mirrdash.jobs_queued_utils import get_jobs_queued_stats, \
    get_jobs_queued_attachments, get_jobs_queued_comments, \
        get_jobs_queued_dockets, get_jobs_queued_documents

def test_jobs_queued_stats():
    mock_database = FakeRedis()
    mock_database.set('attachments', int(5))
    mock_database.set('comments', int(5))
    mock_database.set('dockets', int(5))
    mock_database.set('documents', int(5))
    assert get_jobs_queued_stats(mock_database) == {'num_jobs_attachments_queued': None, 'num_jobs_comments_queued': None, \
        'num_jobs_dockets_queued': None, 'num_jobs_documents_queued': None}

def test_attachments_queued():
    mock_database = FakeRedis()
    mock_database.set('attachments', int(5))
    assert get_jobs_queued_attachments(mock_database) == '5'

def test_comments_queued():
    mock_database = FakeRedis()
    mock_database.set('comments', 5)
    assert get_jobs_queued_comments(mock_database) == 5

def test_dockets_queued():
    mock_database = FakeRedis()
    mock_database.set('dockets', 5)
    assert get_jobs_queued_dockets(mock_database) == 5

def test_documents_queued():
    mock_database = FakeRedis()
    mock_database.set('documents', 5)
    assert get_jobs_queued_documents(mock_database) == 5
