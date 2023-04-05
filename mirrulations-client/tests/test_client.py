import os
# import json
# from unittest.mock import patch
from mirrcore.path_generator import PathGenerator
# import pytest
from pytest import fixture  # , raises
import requests_mock
from mirrclient.client import NoJobsAvailableException, Client
from mirrclient.client import is_environment_variables_present
from mirrmock.mock_redis import ReadyRedis, InactiveRedis
from mirrmock.mock_job_queue import MockJobQueue
# from requests.exceptions import Timeout, ReadTimeout
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
        'download_single_attachment',
        return_value=None
    )


def test_no_jobs_available_exception_message():
    try:
        raise NoJobsAvailableException
    except NoJobsAvailableException as exception:
        assert str(exception) == "There are no jobs available"


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
    client = Client(ReadyRedis())
    job = {
        'job_id': 1,
        'url': 'regulations.gov',
        'job_type': 'comments'
    }
    job = client.generate_job_dict(job)
    final_job = {
        'job_id': 1,
        'url': 'regulations.gov',
        'job_type': 'comments',
        'reg_id': 'other_reg_id',
        'agency': 'other_agency'
    }
    assert job == final_job


def test_remove_plural_from_job():
    client = Client(ReadyRedis())
    job = {'url': 'regulations.gov/comments/DOD-0001-0001'}
    job_without_plural = client.remove_plural_from_job_type(job)
    assert job_without_plural == 'comment/DOD-0001-0001'


def test_can_connect_to_database():
    client = Client(ReadyRedis())
    assert client.can_connect_to_database()


def test_cannot_connect_to_database():
    client = Client(InactiveRedis())
    assert not client.can_connect_to_database()


def test_job_queue_is_empty():
    client = Client(ReadyRedis())
    client.job_queue = MockJobQueue()
    job = {'error': 'No jobs available'}
    assert client.get_job_from_job_queue() == job


def test_get_job_from_job_queue_gets_job():
    client = Client(ReadyRedis())
    client.job_queue = MockJobQueue()
    client.job_queue.add_job({'job': 'This is a job'})
    assert client.get_job_from_job_queue() == {'job': 'This is a job'}


def test_does_comment_have_attachment_has_attachment():
    client = Client(ReadyRedis())
    comment_json = {'included': [0]}
    assert client.does_comment_have_attachment(comment_json)


def test_does_comment_have_attachment_does_have_attachment():
    client = Client(ReadyRedis())
    comment_json = {'included': []}
    assert not client.does_comment_have_attachment(comment_json)


# def test_client_gets_job():
#     client = Client()
#     link = 'https://api.regulations.gov/v4/type/type_id'

#     job_info = client.get_job()
#     assert {'job_id': '1',
#             'url': link,
#             'job_type': 'attachments',
#             'reg_id': '1',
#             'agency': 'foo'} == job_info


def test_get_output_path_error(path_generator):
    results = {'error': 'error'}
    output_path = path_generator.get_path(results)

    assert output_path == "/unknown/unknown.json"


# def test_handles_nonetype_error(mock_requests, path_generator):
#     """
#     Test for handling of the NoneType Error caused by null fileformats
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
#                 "included": [{
#                     "attributes": {
#                         "fileFormats": None
#                     },
#                 }]
#             },
#             status_code=200
#         )

#         mock_requests.put('http://work_server:8080/put_results', text='{}')
#         client.job_operation()
#         put_request = mock_requests.request_history[2]
#         json_data = json.loads(put_request.json())
#         assert json_data['job_type'] == "comments"
#         results = json_data['results']
#         attachment_paths = path_generator.get_attachment_json_paths(results)
#         assert attachment_paths == []


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


# # Client Attachments Tests
# def test_client_downloads_attachment_results(mock_requests):
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
#                     "id": "FDA-2016-D-2335-1566",
#                     "type": "comments",
#                     "attributes": {
#                         "agencyId": "FDA",
#                         "docketId": "FDA-2016-D-2335"
#                     }
#                 },
#                 "included": [{
#                     "attributes": {
#                         "fileFormats": [{
#                             "fileUrl": "https://fakeurl.gov"
#                         }]
#                     }
#                 }]
#             },
#             status_code=200
#         )
#         mock_requests.get(
#             "https://fakeurl.gov",
#             json={"data": 'foobar'},
#             status_code=200
#         )
#         mock_requests.put('http://work_server:8080/put_results', text='{}')

#         client.job_operation()
#         put_request = mock_requests.request_history[2]
#         json_data = json.loads(put_request.json())
#         assert json_data['job_id'] == "1"
#         assert json_data['job_type'] == "comments"


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


# def test_add_attachment_information_to_data():
#     data = {}
#     path = '/USTR/docket.json'
#     filename = "docket.json"
#     client = Client()
#     data = client.add_attachment_information_to_data(data, path, filename)
#     assert data['job_type'] == 'attachments'
#     assert data['attachment_path'] == '/data/data/USTR/docket.json'
#     assert data['attachment_filename'] == 'docket.json'


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


# def test_downloading_htm_send_job(capsys, mock_requests, mocker):
#     mocker.patch('mirrclient.saver.Saver.make_path', return_value=None)
#     mocker.patch('mirrclient.saver.Saver.save_attachment', return_value=None)
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
#                            {'agencyId': 'NOAA', 'docketId': 'NOAA-0001-0001',
#                             "fileFormats": [{
#                                "fileUrl": ("https://downloads.regulations."
#                                             "gov/USTR-2015-0010-0001/"
#                                             "content.htm"),
#                                "format": "htm",
#                                "size": 9709
#                             }]},
#                            'job_type': 'documents'}},
#             status_code=200
#         )
#         mock_requests.put('http://work_server:8080/put_results', text='{}')
#         mock_requests.get('https://downloads.regulations.gov/'
#                           'USTR-2015-0010-0001/content.htm')
#         client.job_operation()
#     captured = capsys.readouterr()
#     print_data = [
#         'Processing job from work server\n',
#      'Regulations.gov link: https://www.regulations.gov/document/type_id\n',
#         'API URL: https://api.regulations.gov/v4/documents/type_id\n',
#         'Performing job\n',
#         'Sending Job 1 to Work Server\n',
#         ('SAVED document HTM '
#             '- https://downloads.regulations.gov/USTR-2015-0010-0001/'
#             'content.htm to path:  '
#             '/NOAA/NOAA-0001-0001/text-NOAA-0001-0001/documents/'
#             '1_content.htm\n'),
#      'SUCCESS: https://api.regulations.gov/v4/documents/type_id complete\n'
#     ]
#     assert captured.out == "".join(print_data)
