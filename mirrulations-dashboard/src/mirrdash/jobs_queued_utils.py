"""
This module contains the functions that will be used to query the redis DB
    for info about the jobs in the queue.

Dependencies:
    redis
"""

def get_jobs_queued_stats(redis_db):
    return {
        'num_jobs_attachments_queued': get_jobs_queued_attachments(redis_db),
        'num_jobs_comments_queued': get_jobs_queued_comments(redis_db),
        'num_jobs_dockets_queued': get_jobs_queued_dockets(redis_db),
        'num_jobs_documents_queued': get_jobs_queued_documents(redis_db)
    }


def get_jobs_queued_attachments(redis_db):
    # return int(redis_db.get('num_jobs_attachments_queued'))
    return int(0)


def get_jobs_queued_comments(redis_db):
    # return int(redis_db.get('num_jobs_comments_queued'))
    return int(0)


def get_jobs_queued_dockets(redis_db):
    # return int(redis_db.get('num_jobs_dockets_queued'))
    return int(0)


def get_jobs_queued_documents(redis_db):
    # return int(redis_db.get('num_jobs_documents_queued'))
    return int(0)