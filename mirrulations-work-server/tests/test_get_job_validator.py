from mirrserver.get_job_validator import GetJobValidator
from mirrserver.get_job_validator import MissingClientIDException
import pytest


def test_get_job_no_client_id():
    validator = GetJobValidator()
    # data = {'jobs_waiting_queue': 1}
    client_id = None
    with pytest.raises(MissingClientIDException):
        validator.check_get_jobs(client_id)


# def test_get_job_no_jobs():
#     validator = GetJobValidator()
#     # data = {'jobs_waiting_queue': 0}
#     client_id = '5'
#     with pytest.raises(NoJobsException):
#         validator.check_get_jobs(client_id)


def test_get_job_valid_client_id_and_jobs():
    validator = GetJobValidator()
    # data = {'jobs_waiting_queue': 1}
    client_id = '10'
    assert validator.check_get_jobs(client_id)
