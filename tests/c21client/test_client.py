from c21server.work_server.work_server import WorkServer, create_server
from fakeredis import FakeStrictRedis
from flask import Flask, json, jsonify, request
from c21client.client import server_url
from pytest import fixture


@fixture
def mock_db():
    mock_db = FakeStrictRedis()
    server = create_server(mock_db)


def test_server_url():
    assert server_url() == "http://localhost:8080"
