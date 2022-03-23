"""
This module contains the functions that will increment and decrement the counts of job
    types in the queues

Dependencies:
    redis
"""
import redis

def change_queue_counter(redis_db, job_type, increment=True):
    # match the job type to the proper counter
    if job_type == 'attachments':
        queue_var = 'num_jobs_attachments_queued'
    elif job_type == 'comments':
        queue_var = 'num_jobs_comments_queued'
    elif job_type == 'dockets':
        queue_var = 'num_jobs_dockets_queued'
    elif job_type == 'documents':
        queue_var = 'num_jobs_documents_queued'
    else: return

    # increment or decrement the var
    if increment:
        redis_db.incr(queue_var)
    else:
        redis_db.decr(queue_var)