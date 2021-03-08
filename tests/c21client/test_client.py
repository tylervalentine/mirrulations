from c21client.client import try_to_get_work
from c21server.work_server.work_server import WorkServer, create_server
from fakeredis import FakeStrictRedis
from flask import Flask, json, jsonify, request

@fixture
def mock_db():
    mock_db = FakeStrictRedis()
    server = create_server(mock_db)

