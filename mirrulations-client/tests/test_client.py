# pylint: disable=W0212
import os
# import json
# from unittest.mock import patch
import responses
from mirrcore.path_generator import PathGenerator
import pytest
from pytest import fixture  # , raises
import requests_mock
from mirrclient.client import NoJobsAvailableException, Client
from mirrclient.client import is_environment_variables_present
from mirrmock.mock_redis import ReadyRedis, InactiveRedis
from mirrmock.mock_job_queue import MockJobQueue
from requests.exceptions import ReadTimeout
# from mirrmock.mock_redis import ReadyRedis  # BusyRedis


BASE_URL = 'http://work_server:8080'


@fixture(autouse=True)
def mock_env():
    os.environ['WORK_SERVER_HOSTNAME'] = 'work_server'
    os.environ['WORK_SERVER_PORT'] = '8080'
    os.environ['API_KEY'] = 'TESTING_KEY'
    os.environ['ID'] = '-1'


@fixture(name='mock_requests')
def fixture_mock_requests():
    return requests_mock.Mocker()


@fixture(name="path_generator")
def get_path():
    return PathGenerator()


@fixture(autouse=True)
def mock_disk_writing(mocker):
    """
    Mock tests that would be writing to disk
    """
    # patch _write_results and AttachmentSaver.save
    mocker.patch.object(
        Client,
        '_put_results',
        return_value=None
    )
    mocker.patch.object(
        Client,
        '_download_single_attachment',
        return_value=None
    )


def test_check_no_env_values():
    # Need to delete env variables set by mock_env fixture
    del os.environ['WORK_SERVER_HOSTNAME']
    del os.environ['WORK_SERVER_PORT']
    del os.environ['API_KEY']
    assert is_environment_variables_present() is False


def test_check_no_hostname():
    # Need to delete hostname env variable set by mock_env fixture
    del os.environ['WORK_SERVER_HOSTNAME']
    assert is_environment_variables_present() is False


def test_check_no_server_port():
    # Need to delete server port env variable set by mock_env fixture
    del os.environ['WORK_SERVER_PORT']
    assert is_environment_variables_present() is False


def test_check_no_api_key():
    # Need to delete api key env variable set by mock_env fixture
    del os.environ['API_KEY']
    assert is_environment_variables_present() is False


def test_client_has_no_id():
    # Need to delete id env variable set by mock_env fixture
    del os.environ['ID']
    assert is_environment_variables_present() is False


def test_generate_job_dict():
    client = Client(ReadyRedis(), MockJobQueue())
    job = {
        'job_id': 1,
        'url': 'regulations.gov',
        'job_type': 'comments'
    }
    job = client._generate_job_dict(job)
    final_job = {
        'job_id': 1,
        'url': 'regulations.gov',
        'job_type': 'comments',
        'reg_id': 'other_reg_id',
        'agency': 'other_agency'
    }
    assert job == final_job


def test_remove_plural_from_job():
    client = Client(ReadyRedis(), MockJobQueue())
    job = {'url': 'regulations.gov/comments/DOD-0001-0001'}
    job_without_plural = client._remove_plural_from_job_type(job)

    assert job_without_plural == 'comment/DOD-0001-0001'


def test_can_connect_to_database():
    client = Client(ReadyRedis(), MockJobQueue())

    assert client._can_connect_to_database()


def test_cannot_connect_to_database():
    client = Client(InactiveRedis(), MockJobQueue())
    assert not client._can_connect_to_database()


def test_job_queue_is_empty():
    client = Client(ReadyRedis(), MockJobQueue())
    # If no jobs are in the queue we will raise this Exception
    with pytest.raises(NoJobsAvailableException):
        client.job_operation()


def test_get_job_from_job_queue_gets_job():
    client = Client(ReadyRedis(), MockJobQueue())
    client.job_queue = MockJobQueue()
    client.job_queue.add_job({'job': 'This is a job'})
    assert client._get_job_from_job_queue() == {'job': 'This is a job'}


def test_get_job():
    client = Client(ReadyRedis(), MockJobQueue())
    client.job_queue = MockJobQueue()
    job = {
        'job_id': 1,
        'url': 'https://api.regulations.gov/v4/dockets/type_id',
        'job_type': 'comments',
        'reg_id': 'other_reg_id',
        'agency': 'other_agency'
    }
    client.job_queue.add_job(job)
    assert client._get_job() == job


def test_get_job_is_empty():
    client = Client(ReadyRedis(), MockJobQueue())
    job = {'error': 'No jobs available'}
    assert client._get_job() == job


def test_does_comment_have_attachment_has_attachment():
    client = Client(ReadyRedis(), MockJobQueue())
    comment_json = {'included': [0]}
    assert client._does_comment_have_attachment(comment_json)


def test_does_comment_have_attachment_does_have_attachment():
    client = Client(ReadyRedis(), MockJobQueue())
    comment_json = {'included': []}
    assert not client._does_comment_have_attachment(comment_json)


def test_client_hsets_redis_values():
    mock_redis = ReadyRedis()
    client = Client(mock_redis, MockJobQueue())
    mock_redis.set('jobs_in_progress', ['foo', 'var'])
    mock_redis.set('client_jobs', ['foo', 'bar'])
    job = {'job_id': 1,
           'url': 'fake.com'}
    client._set_redis_values(job)
    assert mock_redis.get('jobs_in_progress') == [1, 'fake.com']
    assert mock_redis.get('client_jobs') == [1, '-1']


def test_document_has_file_formats_does_not_have_data():
    client = Client(ReadyRedis(), MockJobQueue())
    json = {}
    assert not client._document_has_file_formats(json)


def test_document_has_file_formats_does_not_have_attributes():
    client = Client(ReadyRedis(), MockJobQueue())
    json = {'data': {}}
    assert not client._document_has_file_formats(json)


def test_document_has_file_formats_does_not_have_file_formats():
    client = Client(ReadyRedis(), MockJobQueue())
    json = {'data': {'attributes': []}}
    assert not client._document_has_file_formats(json)


def test_document_has_file_formats_ha_required_fields():
    client = Client(ReadyRedis(), MockJobQueue())
    json = {'data': {'attributes': {'fileFormats': {}}}}
    assert client._document_has_file_formats(json)


def test_get_document_htm_returns_link():
    client = Client(ReadyRedis(), MockJobQueue())
    json = {'data': {
                'attributes': {
                    'fileFormats': [{
                        'format': 'htm',
                        'fileUrl': 'fake.com'}]}}}
    assert client._get_document_htm(json) == 'fake.com'


def test_get_document_htm_returns_none():
    client = Client(ReadyRedis(), MockJobQueue())
    json = {'data': {
                'attributes': {
                    'fileFormats': [{
                        'format': 'pdf',
                        'fileUrl': 'fake.pdf'}]}}}
    assert client._get_document_htm(json) is None


def test_get_output_path_error(path_generator):
    results = {'error': 'error'}
    output_path = path_generator.get_path(results)

    assert output_path == "/unknown/unknown.json"


@responses.activate
def test_client_handles_read_timeout():
    mock_redis = ReadyRedis()
    client = Client(mock_redis, MockJobQueue())
    client.api_key = 1234
    client.job_queue.add_job({'job_id': 1,
                              'url': 'http://regulations.gov/job',
                              "job_type": "comments"})
    mock_redis.set('jobs_in_progress', [1, 'http://regulations.gov/job'])

    responses.get("http://regulations.gov/job",
                  body=ReadTimeout("Read Timeout"))
    client.job_operation()
    assert mock_redis.get('invalid_jobs') == [1, 'http://regulations.gov/job']


def test_client_handles_error_in_download_job():
    mock_redis = ReadyRedis()
    client = Client(mock_redis, MockJobQueue())
    mock_redis.set('jobs_in_progress', ['foo', 'var'])
    mock_redis.set('client_jobs', ['foo', 'bar'])
    job = {'job_id': 1,
           'url': 'fake.com',
           'job_type': "comments",
           "reg_id": "test_id",
           "agency": "test_agency"
           }
    job_result = {"error": "Timeout"}
    client._download_job(job, job_result)
    assert mock_redis.get('invalid_jobs') == [1, 'fake.com']


@responses.activate
def test_handles_nonetype_error(path_generator):
    """
    Test for handling of the NoneType Error caused by null fileformats
    """
    mock_redis = ReadyRedis()
    client = Client(mock_redis, MockJobQueue())
    client.api_key = 1234
    client.job_queue.add_job({'job_id': 1,
                              'url': 'http://regulations.gov/job',
                              "job_type": "comments"})
    mock_redis.set('jobs_in_progress', [1,
                                        'http://regulations.gov/job'])

    test_json = {
                "data": {
                    "id": "agencyID-001-0002",
                    "type": "comments",
                    "attributes": {
                        "agencyId": "agencyID",
                        "docketId": "agencyID-001"
                    }
                },
                "included": [{
                    "attributes": {
                        "fileFormats": None
                    },
                }]}
    responses.add(responses.GET, 'http://regulations.gov/job',
                  json=test_json, status=200)
    client.job_operation()
    assert mock_redis.get('jobs_in_progress') == [1,
                                                  'http://regulations.gov/job']
    assert mock_redis.get('client_jobs') == [1, '-1']

    attachment_paths = path_generator.get_attachment_json_paths(test_json)
    assert attachment_paths == []


@responses.activate
def test_downloading_htm_send_job(capsys, mocker):
    mocker.patch('mirrclient.saver.Saver.make_path', return_value=None)
    mocker.patch('mirrclient.saver.Saver.save_attachment', return_value=None)
    mock_redis = ReadyRedis()
    client = Client(mock_redis, MockJobQueue())
    client.api_key = 1234
    client.job_queue.add_job({'job_id': 1,
                              'url': 'http://regulations.gov/documents',
                              "job_type": "documents"})
    mock_redis.set('jobs_in_progress', [1, 'http://regulations.gov/documents'])

    test_json = {'data': {'id': '1', 'type': 'documents',
                                'attributes':
                                {'agencyId': 'USTR',
                                 'docketId': 'USTR-2015-0010',
                                    "fileFormats": [{
                                        "fileUrl":
                                            ("http://downloads.regulations."
                                                "gov/USTR-2015-0010-0001/"
                                             "content.htm"),
                                        "format": "htm",
                                        "size": 9709
                                    }]},
                                'job_type': 'documents'}}
    responses.add(responses.GET, 'http://regulations.gov/documents',
                  json=test_json, status=200)
    responses.add(responses.GET,
                  'http://downloads.regulations.gov/' +
                  'USTR-2015-0010-0001/content.htm',
                  json='\bx17', status=200)
    client.job_operation()
    captured = capsys.readouterr()
    print_data = [
        'Processing job from work server\n',
        'Attempting to get job\n',
        'Job received from job queue\n',
        'Job received: documents for client:  -1\n'
        'Regulations.gov link: http://regulations.gov/documents\n',
        'API URL: http://regulations.gov/documents\n',
        'Performing job\n',
        ('SAVED document HTM '
            '- http://downloads.regulations.gov/USTR-2015-0010-0001/'
            'content.htm to path:  '
            '/USTR/USTR-2015-0010/text-USTR-2015-0010/documents/'
            '1_content.htm\n'),
        'SUCCESS: http://regulations.gov/documents complete\n'
    ]
    assert captured.out == "".join(print_data)


def test_add_attachment_information_to_data():
    data = {}
    path = '/USTR/docket.json'
    filename = "docket.json"
    mock_redis = ReadyRedis()
    client = Client(mock_redis, MockJobQueue())
    data = client._add_attachment_information_to_data(data, path, filename)
    assert data['job_type'] == 'attachments'
    assert data['attachment_path'] == '/data/data/USTR/docket.json'
    assert data['attachment_filename'] == 'docket.json'


# def test_success_client_logging(capsys, mock_requests):
#     client = Client()
#     client.api_key = 1234

#     with mock_requests:
#         mock_requests.get(
#             'http://work_server:8080/get_job?client_id=-1',
#             json={'job_id': '1',
#                   'url': 'https://api.regulations.gov/v4/documents/type_id',
#                   'job_type': 'documents',
#                   'reg_id': '1',
#                   'agency': 'foo'},
#             status_code=200
#         )
#         mock_requests.get(
#             'https://api.regulations.gov/v4/documents/type_id?api_key=1234',
#             json={'data': {'id': '1', 'type': 'documents',
#                            'attributes':
#                          {'agencyId': 'NOAA', 'docketId': 'NOAA-0001-0001'},
#                            'job_type': 'documents'}},
#             status_code=200
#         )
#         mock_requests.put('http://work_server:8080/put_results', text='{}')
#         client.job_operation()
#     captured = capsys.readouterr()
#     print_data = [
#         'Processing job from work server\n',
#      'Regulations.gov link: https://www.regulations.gov/document/type_id\n',
#         'API URL: https://api.regulations.gov/v4/documents/type_id\n',
#         'Performing job\n',
#         'Sending Job 1 to Work Server\n',
#      'SUCCESS: https://api.regulations.gov/v4/documents/type_id complete\n'
#     ]
#     assert captured.out == "".join(print_data)


# def test_failure_job_results(capsys, mock_requests):
#     client = Client()
#     client.api_key = 1234

#     with mock_requests:
#         mock_requests.get(
#             'http://work_server:8080/get_job?client_id=-1',
#             json={'job_id': '1',
#                   'url': 'http://url.com',
#                   'job_type': 'documents',
#                   'reg_id': '1',
#                   'agency': 'foo'},
#             status_code=200
#         )
#         mock_requests.get(
#             'http://url.com?api_key=1234',
#             json={"error": 'foobar'},
#             status_code=200
#         )
#         mock_requests.get(
#             "https://downloads.regulations.gov",
#             json={"error": 'foobar'},
#             status_code=200
#         )
#         mock_requests.put('http://work_server:8080/put_results', text='{}')
#         client.job_operation()

#         print_data = {
#             'Processing job from work server\n'
#             'Regulations.gov link: https://www.regulations.gov//url.com\n'
#             'API URL: http://url.com\n'
#             'Performing job\n'
#             'Sending Job 1 to Work Server\n'
#             'FAILURE: Error in http://url.com\n'
#             'Error: foobar\n'
#         }

#         captured = capsys.readouterr()
#         assert captured.out == "".join(print_data)


# Client Attachments Tests
@responses.activate
def test_client_downloads_attachment_results(mocker, capsys):
    mocker.patch('mirrclient.saver.Saver.make_path', return_value=None)
    mocker.patch('mirrclient.saver.Saver.save_attachment', return_value=None)
    mock_redis = ReadyRedis()
    client = Client(mock_redis, MockJobQueue())
    client.api_key = 1234
    client.job_queue.add_job({'job_id': 1,
                              'url': 'http://regulations.gov/comments',
                              "job_type": "comments"})
    mock_redis.set('jobs_in_progress', [1, 'http://regulations.gov/comments'])

    test_json = {
                "data": {
                    "id": "FDA-2016-D-2335-1566",
                    "type": "comments",
                    "attributes": {
                        "agencyId": "FDA",
                        "docketId": "FDA-2016-D-2335"
                    }
                },
                "included": [{
                    "attributes": {
                        "fileFormats": [{
                            "fileUrl": ("http://downloads.regulations."
                                        "gov/FDA-2016-D-2335/"
                                        "attachment_1.pdf")
                        }]
                    }
                }]
            }
    responses.add(responses.GET, 'http://regulations.gov/comments',
                  json=test_json, status=200)
    responses.add(responses.GET,
                  ('http://downloads.regulations.gov/\
                   FDA-2016-D-2335/attachment_1.pdf'),
                  json='\bx17', status=200)
    client.job_operation()
    captured = capsys.readouterr()
    print_data = [
        'Processing job from work server\n',
        'Attempting to get job\n',
        'Job received from job queue\n',
        'Job received: comments for client:  -1\n'
        'Regulations.gov link: http://regulations.gov/comments\n',
        'API URL: http://regulations.gov/comments\n',
        'Performing job\n',
        'Found 1 attachment(s) for Comment - FDA-2016-D-2335-1566\n'
        'Downloaded 1/1 attachment(s) for Comment - FDA-2016-D-2335-1566\n'
        'SUCCESS: http://regulations.gov/comments complete\n'
    ]
    assert captured.out == "".join(print_data)

    client.job_operation()


# def test_handles_empty_attachment_list(mock_requests):
#     """
#     Test that handles empty attachment list from comments json being:
#     {
#         "relationships" : {
#                 "attachments" : {
#                     "data" : [ ]}
#                     }
#     }
#     """
#     client = Client()
#     client.api_key = 1234

#     with mock_requests:
#         mock_requests.get(
#             'http://work_server:8080/get_job?client_id=-1',
#             json={'job_id': '1',
#                   'url': 'http://regulations.gov/job',
#                   'job_type': 'comments',
#                   'reg_id': '1',
#                   'agency': 'foo'},
#             status_code=200
#         )
#         mock_requests.get(
#             'http://regulations.gov/job?api_key=1234',
#             json={
#                 "data": {
#                     "id": "agencyID-001-0002",
#                     "type": "comments",
#                     "attributes": {
#                         "agencyId": "agencyID",
#                         "docketId": "agencyID-001"
#                     }
#                 },
#                 "relationships": {
#                     "attachments": {
#                         "data": []
#                     }
#                 }
#             },
#             status_code=200
#         )

#         mock_requests.put('http://work_server:8080/put_results', text='{}')
#         client.job_operation()
#         put_request = mock_requests.request_history[2]
#         json_data = json.loads(put_request.json())
#         results = json_data['results']
#         assert json_data['job_type'] == "comments"
#         assert client.does_comment_have_attachment(results) is False


# def test_success_attachment_logging(capsys, mock_requests):
#     client = Client()
#     client.api_key = 1234

#     with mock_requests:
#         mock_requests.get(
#             'http://work_server:8080/get_job?client_id=-1',
#             json={'job_id': '1',
#                   'url': 'http://url.com',
#                   'job_type': 'comments',
#                   'reg_id': '1',
#                   'agency': 'foo'},
#             status_code=200
#         )
#         mock_requests.get(
#             'http://url.com?api_key=1234',
#             json={
#                 "data": {
#                     "id": "agencyID-001-0002",
#                     "type": "comments",
#                     "attributes": {
#                         "agencyId": "agencyID",
#                         "docketId": "agencyID-001"
#                     }
#                 },
#                 "included": [{
#                     "attributes": {
#                         "fileFormats": [{
#                             "fileUrl": "https://downloads.regulations.gov"
#                         }]
#                     }
#                 }]
#             },
#             status_code=200
#         )

#         mock_requests.get(
#             "https://downloads.regulations.gov",
#             json={"data": 'foobar'},
#             status_code=200
#         )
#         mock_requests.put('http://work_server:8080/put_results', text='{}')
#         client.job_operation()

#         print_data = {
#             'Processing job from work server\n'
#             'Regulations.gov link: https://www.regulations.gov//url.com\n'
#             'API URL: http://url.com\n'
#             'Performing job\n'
#             'Sending Job 1 to Work Server\n'
#             'Found 1 attachment(s) for Comment - agencyID-001-0002\n'
#             'Downloaded 1/1 attachment(s) for Comment - agencyID-001-0002\n'
#             'SUCCESS: http://url.com complete\n'
#         }

#         captured = capsys.readouterr()
#         assert captured.out == "".join(print_data)


# def test_success_no_attachment_logging(capsys, mock_requests):
#     client = Client()
#     client.api_key = 1234

#     with mock_requests:
#         mock_requests.get(
#             'http://work_server:8080/get_job?client_id=-1',
#             json={'job_id': '1',
#                   'url': 'http://url.com',
#                   'job_type': 'attachments',
#                   'reg_id': '1',
#                   'agency': 'foo'},
#             status_code=200
#         )
#         mock_requests.get(
#             'http://url.com?api_key=1234',
#             json={"data": []},
#             status_code=200
#         )

#         mock_requests.put('http://work_server:8080/put_results', text='{}')
#         client.job_operation()

#         print_data = {
#             'Processing job from work server\n'
#             'Regulations.gov link: https://www.regulations.gov//url.com\n'
#             'API URL: http://url.com\n'
#             'Performing job\n'
#             'Sending Job 1 to Work Server\n'
#             'SUCCESS: http://url.com complete\n'
#         }

#         captured = capsys.readouterr()
#         assert captured.out == "".join(print_data)


# def test_failure_attachment_job_results(capsys, mock_requests):
#     client = Client()
#     client.api_key = 1234

#     with mock_requests:
#         mock_requests.get(
#             'http://work_server:8080/get_job?client_id=-1',
#             json={'job_id': '1',
#                   'url': 'http://url.com',
#                   'job_type': 'comments',
#                   'reg_id': '1',
#                   'agency': 'foo'},
#             status_code=200
#         )
#         mock_requests.get(
#             'http://url.com?api_key=1234',
#             json={
#                 "data": {
#                     "id": "agencyID-001-0002",
#                     "type": "comments",
#                     "attributes": {
#                         "agencyId": "agencyID",
#                         "docketId": "agencyID-001"
#                     }
#                 },
#                 "included": [{
#                     "attributes": {
#                         "fileFormats": [{
#                             "fileUrl": "https://downloads.regulations.gov"
#                         }]
#                     }
#                 }]
#             },
#             status_code=200
#         )

#         mock_requests.get(
#             "https://downloads.regulations.gov",
#             json={"data": 'foobar'},
#             status_code=200
#         )
#         mock_requests.put('http://work_server:8080/put_results', text='{}')
#         client.job_operation()

#         print_data = {
#             'Processing job from work server\n'
#             'Regulations.gov link: https://www.regulations.gov//url.com\n'
#             'API URL: http://url.com\n'
#             'Performing job\n'
#             'Sending Job 1 to Work Server\n'
#             'Found 1 attachment(s) for Comment - agencyID-001-0002\n'
#             'Downloaded 1/1 attachment(s) for Comment - agencyID-001-0002\n'
#             'SUCCESS: http://url.com complete\n'
#         }

#         captured = capsys.readouterr()
#         assert captured.out == "".join(print_data)


# def test_download_htm(capsys, mocker, mock_requests):
#     mocker.patch('mirrclient.saver.Saver.make_path', return_value=None)
#     mocker.patch('mirrclient.saver.Saver.save_attachment', return_value=None)

#     client = Client()

#     pdf = "https://downloads.regulations.gov/USTR/content.pdf"
#     htm = "https://downloads.regulations.gov/USTR/content.htm"
#     htm_json = {
#             "data": {
#                 "attributes": {
#                     "fileFormats": [{
#                         "fileUrl": pdf,
#                         "format": "pdf",
#                         "size": 182010
#                         }, {
#                         "fileUrl": htm,
#                         "format": "htm",
#                         "size": 9709
#                         }
#                     ]
#                 }
#             }
#         }

#     with mock_requests:
#         mock_requests.get(
#             htm,
#             json={"data": 'foobar'},
#             status_code=200
#         )

#         client.download_htm(htm_json)
#         captured = capsys.readouterr().out
#         assert f"SAVED document HTM - {htm} to path:" in captured
