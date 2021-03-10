from c21server.work_server.work_server import WorkServer, create_server
from fakeredis import FakeStrictRedis
from flask import Flask, json, jsonify, request
import requests_mock
import requests
from pytest import fixture

'''Creation of mock work_server for testing'''
@fixture
def mock_server():
    mock_db = FakeStrictRedis()
    mock_db.app = Flask(__name__)
    server = create_server(mock_db)
    return server

@fixture
def mock_get_job_request():
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount('mock://', adapter)

    adapter.register_uri('GET', 'mock://0.0.0.0:8080/get_job')
    response = session.get('mock://0.0.0.0:8080/get_job')
    return response

'''Test to make sure the mock database is being created correctly'''
def test_create_server(mock_server):
    assert mock_server is not None

'''Test to see if mock database has no entries on creation'''
def test_new_database_is_empty(mock_server):
    assert mock_server.keys() == []

'''Test for correct data entry'''
def test_data_entry_in_db_is_correct(mock_server):
    mock_server.set('val1', 1)
    assert mock_server.get('val1').decode() == '1'

'''Test data changes in redis database'''
def test_data_entry_changes(mock_server):
    mock_server.set('val1', 1)
    mock_server.set('val1', 2)
    assert mock_server.get('val1').decode() is not '1'
    assert mock_server.get('val1').decode() == '2'

'''Test data deleted from the database is now nonexistent'''
def test_data_deleted_from_db_is_gone(mock_server):
    mock_server.set('val1', 1)
    assert mock_server.get('val1').decode() == '1'
    mock_server.delete('val1')
    assert mock_server.get('val1') == None

'''Test for the get_job endpoint'''
def test_get_job(mock_server, mock_get_job_request):
    mock_server.set('val1', 1)
    assert mock_server.get('val1').decode() == '1'

    assert mock_get_job_request.status_code == 200
    # assert mock_get_job_request.request.url == '1'


    # assert mock_get_job_request.get('0.0.0.0:8080/get_job') == requests.get('0.0.0.0:8080/get_job')



# '''Test to make sure that if the client calls Redis when there has been no data inputted into the DB'''
# def test(mock_db):
# 	assert True
