"""
This module contains the functions that will be used to query the redis DB
    for info about the jobs in the queue.
    THIS IS NOT USED

Dependencies:
    redis
"""


"""def get_jobs_queued_stats(redis_db):
    try:
        return {
            'num_jobs_attachments_queued':
            get_jobs_queued_attachments(redis_db),
            'num_jobs_comments_queued':
            get_jobs_queued_comments(redis_db),
            'num_jobs_dockets_queued':
            get_jobs_queued_dockets(redis_db),
            'num_jobs_documents_queued':
            get_jobs_queued_documents(redis_db)
        }
    except TypeError:
        return {
            'num_jobs_attachments_queued': None,
            'num_jobs_comments_queued': None,
            'num_jobs_dockets_queued': None,
            'num_jobs_documents_queued': None
        }


def get_jobs_queued_attachments(redis_db):
    return int(redis_db.get('num_jobs_attachments_queued'))


def get_jobs_queued_comments(redis_db):
    return int(redis_db.get('num_jobs_comments_queued'))


def get_jobs_queued_dockets(redis_db):
    return int(redis_db.get('num_jobs_dockets_queued'))


def get_jobs_queued_documents(redis_db):
    return int(redis_db.get('num_jobs_documents_queued'))"""
