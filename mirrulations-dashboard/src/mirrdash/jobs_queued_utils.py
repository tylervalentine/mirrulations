def get_jobs_queued_stats(redis_db):
    return {
        'num_jobs_attachments_queued': get_jobs_queued_attachments(redis_db),
        'num_jobs_comments_queued': get_jobs_queued_comments(redis_db),
        'num_jobs_dockets_queued': get_jobs_queued_dockets(redis_db),
        'num_jobs_documents_queued': get_jobs_queued_documents(redis_db),
    }


def get_jobs_queued_attachments(redis_db):
    return int(redis_db.get('num_jobs_attachments_queued'))


def get_jobs_queued_comments(redis_db):
    return int(redis_db.get('num_jobs_comments_queued'))


def get_jobs_queued_dockets(redis_db):
    return int(redis_db.get('num_jobs_dockets_queued'))


def get_jobs_queued_documents(redis_db):
    return int(redis_db.get('num_jobs_documents_queued'))