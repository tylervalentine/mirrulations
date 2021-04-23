from json import dumps
from fakeredis import FakeRedis, FakeServer
from pytest import fixture
from c21server.work_server.work_server import create_server
from .test_utils import mock_flask_server


@fixture(name='mock_server')
def fixture_mock_server():
    return mock_flask_server(create_server)


def test_create_server_not_connected():
    redis_server = FakeServer()
    mock_db = FakeRedis(server=redis_server)
    redis_server.connected = False
    assert create_server(mock_db) is None


def test_create_mock_database(mock_server):
    assert mock_server.redis is not None


def test_create_mock_server(mock_server):
    assert mock_server.app is not None


def test_new_mock_database_is_empty(mock_server):
    assert mock_server.redis.keys() == []


def test_data_entry_in_mock_database_is_correct(mock_server):
    mock_server.redis.set('val1', 1)
    assert mock_server.redis.get('val1').decode() == '1'


def test_data_entry_changes_in_mock_database(mock_server):
    mock_server.redis.set('val1', 1)
    mock_server.redis.set('val1', 2)
    assert mock_server.redis.get('val1').decode() != '1'
    assert mock_server.redis.get('val1').decode() == '2'


def test_data_deleted_from_mock_database_is_gone(mock_server):
    mock_server.redis.set('val1', 1)
    assert mock_server.redis.get('val1').decode() == '1'
    mock_server.redis.delete('val1')
    assert mock_server.redis.get('val1') is None


def test_get_job_without_client_id_is_unauthorized(mock_server):
    response = mock_server.client.get('/get_job')
    assert response.status_code == 401
    expected = {'error': 'Client ID was not provided'}
    assert response.get_json() == expected


def test_get_job_with_invalid_client_id_is_unauthorized(mock_server):
    mock_server.redis.incr('total_num_client_ids')
    params = {'client_id': 2}
    response = mock_server.client.get('/get_job', query_string=params)
    assert response.status_code == 401
    expected = {'error': 'Invalid client ID'}
    assert response.get_json() == expected


def test_get_job_has_no_available_job(mock_server):
    mock_server.redis.incr('total_num_client_ids')
    params = {'client_id': 1}
    response = mock_server.client.get('/get_job', query_string=params)
    assert response.status_code == 400
    expected = {'error': 'There are no jobs available'}
    assert response.get_json() == expected


def test_get_job_returns_single_job(mock_server):
    mock_server.redis.incr('total_num_client_ids')
    params = {'client_id': 1}
    mock_server.redis.hset('jobs_waiting', 1, 2)
    response = mock_server.client.get('/get_job', query_string=params)
    assert response.status_code == 200
    expected = {'job': {'1': '2'}}
    assert response.get_json() == expected


def test_get_waiting_job_is_now_in_progress_and_not_waiting(mock_server):
    mock_server.redis.incr('total_num_client_ids')
    params = {'client_id': 1}
    mock_server.redis.hset('jobs_waiting', 2, 3)
    mock_server.client.get('/get_job', query_string=params)
    keys = mock_server.redis.hkeys('jobs_waiting')
    assert keys == []
    keys = mock_server.redis.hkeys('jobs_in_progress')
    assert mock_server.redis.hget('jobs_in_progress', keys[0]).decode() == '3'


def test_put_results_message_body_contains_no_results(mock_server):
    response = mock_server.client.put("/put_results", json=dumps({}))
    assert response.status_code == 400
    assert response.json['error'] == 'The body does not contain the results'


def test_put_results_with_zero_jobs_in_progress(mock_server):
    mock_server.redis.incr('total_num_client_ids')
    mock_server.redis.hset('jobs_in_progress', 2, '')
    data = {'results': {'': ''}}
    params = {'client_id': 1}
    response = mock_server.client.put('/put_results',
                                      json=data, query_string=params)
    assert mock_server.redis.hget('jobs_in_progress', 2).decode() == ''
    assert response.status_code == 400


def test_put_results_returns_directory_error(mock_server):
    data = dumps({'results': {'': ''}, 'directory': None})
    response = mock_server.client.put('/put_results', data=data)
    assert response.status_code == 400
    expected = {'error': 'No directory was included or was incorrect'}
    assert response.get_json() == expected


def test_put_results_returns_correct_job(mock_server, mocker):
    mock_write_results(mocker)
    mock_server.redis.hset('jobs_in_progress', 2, 3)
    mock_server.redis.set('total_num_client_ids', 1)
    data = {'job_id': 2, 'directory': 'dir/dir',
            'results': {2: 3}}
    params = {'client_id': 1}
    response = mock_server.client.put('/put_results', json=data, query_string=params) # might need dumps?
    print(response.get_json())
    assert mock_server.redis.hget('jobs_done', 2).decode() == '3'
    assert response.status_code == 200
    expected = {'success': 'The job was successfully completed'}
    assert response.get_json() == expected
    assert mock_server.redis.hget('jobs_done', 2).decode() == '3'


def test_total_num_client_ids_is_increased_on_get_client_id_call(mock_server):
    previous_number_of_ids = mock_server.redis.get('total_num_client_ids')
    assert previous_number_of_ids is None
    mock_server.client.get('/get_client_id')
    assert int(mock_server.redis.get('total_num_client_ids')) == 1


def test_get_client_id_sends_correct_id(mock_server):
    mock_server.redis.set('total_num_client_ids', 1)
    assert int(mock_server.redis.get('total_num_client_ids')) == 1
    response = mock_server.client.get('/get_client_id')
    assert response.json['client_id'] == 2


def test_database_returns_error_when_database_does_not_exist(mock_server):
    params = {'client_id': 1}
    mock_server.redis_server.connected = False
    response = mock_server.client.get('/get_job', query_string=params)
    assert response.json['error'] == 'Cannot connect to the database'
    assert response.status_code == 500


def test_get_client_id_returns_tuple_when_no_success(mock_server):
    mock_server.redis_server.connected = False
    response = mock_server.client.get('/get_client_id')
    assert response.json['error'] == 'Cannot connect to the database'
    assert response.status_code == 500


def mock_write_results(mocker):
    mocker.patch(
        'c21server.work_server.work_server.write_results',
        return_value=None
    )
