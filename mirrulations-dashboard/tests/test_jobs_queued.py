from operator import ge
from unittest import mock
from webbrowser import get
from fakeredis import FakeRedis
from mirrdash.jobs_queued_utils import get_jobs_queued_stats, \
    get_jobs_queued_attachments, get_jobs_queued_comments, \
        get_jobs_queued_dockets, get_jobs_queued_documents

def test_jobs_queued_stats():
    mock_database = FakeRedis()
    mock_database.set('attachments', 5)
    mock_database.set('comments', 5)
    mock_database.set('dockets', 5)
    mock_database.set('documents', 5)
    assert get_jobs_queued_stats(mock_database) == {'num_jobs_attachments_queued': 5, 'num_jobs_comments_queued': 5, \
        'num_jobs_dockets_queued': 5, 'num_jobs_documents_queued': 5}

def test_attachments_queued():
    mock_database = FakeRedis()
    mock_database.set('attachments', 5)
    assert get_jobs_queued_attachments(mock_database.get('attachments')) == 5

def test_comments_queued():
    mock_database = FakeRedis()
    mock_database.set('comments', 5)
    assert get_jobs_queued_comments(mock_database.get('comments')) == 5

def test_dockets_queued():
    mock_database = FakeRedis()
    mock_database.set('dockets', 5)
    assert get_jobs_queued_dockets(mock_database.get('dockets')) == 5

def test_documents_queued():
    mock_database = FakeRedis()
    mock_database.set('documents', 5)
    assert get_jobs_queued_documents(mock_database.get('documents')) == 5
