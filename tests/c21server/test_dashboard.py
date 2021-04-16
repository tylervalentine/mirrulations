from pytest import fixture
from c21server.dashboard.dashboard_server import create_server, get_jobs_stats
from .test_utils import mock_flask_server


@fixture(name='mock_server')
def fixture_mock_server():
    return mock_flask_server(create_server)


def add_mock_data_to_database(database):
    jobs_waiting = {i: i for i in range(1, 6)}
    database.hset('jobs_waiting', mapping=jobs_waiting)
    jobs_in_progress = {i: i for i in range(6, 10)}
    database.hset('jobs_in_progress', mapping=jobs_in_progress)
    jobs_done = {i: i for i in range(10, 13)}
    database.hset('jobs_done', mapping=jobs_done)
    database.set('total_num_client_ids', 2)


def test_get_jobs_stats(mock_server):
    add_mock_data_to_database(mock_server.redis)
    jobs_stats = get_jobs_stats(mock_server.redis)

    expected = {
        'num_jobs_waiting': 5,
        'num_jobs_in_progress': 4,
        'num_jobs_done': 3,
        'jobs_total': 12,
        'clients_total': 2
    }
    assert jobs_stats == expected


def test_dashboard_returns_job_information(mock_server):
    add_mock_data_to_database(mock_server.redis)
    response = mock_server.client.get('/data')

    assert response.status_code == 200
    expected = {
        'num_jobs_waiting': 5,
        'num_jobs_in_progress': 4,
        'num_jobs_done': 3,
        'jobs_total': 12,
        'clients_total': 2
    }
    assert response.get_json() == expected


def test_dashboard_returns_html(mock_server):
    add_mock_data_to_database(mock_server.redis)
    response = mock_server.client.get('/')

    assert response.status_code == 200
    expected = '<!DOCTYPE html>'
    assert response.data.decode().split('\n')[0] == expected
