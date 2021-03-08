import c21server.work_server as work_server
from work_server import WorkServer, create_server
from fakeredis import FakeStrictRedis
from flask import Flask, json, jsonify, request
from pytest import fixture
import c21server.work_server

@fixture
def mock_server():
    mock_db = FakeStrictRedis()
    work_server = WorkServer(mock_db)
    server = create_server(work_server)

'''Test to make sure the mock database is being created correctly'''
def test_create_server(mock_server):
    assert mock_server 
    
'''Test for correct data entry'''
def test_data_entry_in_db_is_correct(mock_server):
    assert True

'''Test to make sure that if the client calls Redis when there has been no data inputted into the DB'''
def test(mock_db):
	assert True
