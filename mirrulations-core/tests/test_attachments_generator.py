# from mirrcore.attachments_generator import AttachmentsGenerator
from mirrcore.job_queue import JobQueue
import fakeredis

def test_attachment_generator_is_created_with_job_queue_and_database():
    database = fakeredis.FakeRedis()
    job_queue = JobQueue(database)
    # attachment_generator = AttachmentsGenerator(job_queue, database)
    # assert attachment_generator is not None