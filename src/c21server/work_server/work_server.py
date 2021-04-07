import os
from flask import Flask, json, jsonify, request
import redis


class WorkServer:
    def __init__(self, redis_server):
        self.app = Flask(__name__)
        self.redis = redis_server


def check_for_database(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except redis.exceptions.ConnectionError:
            body = {'error': 'Cannot connect to the database'}
            return False, jsonify(body), 500
    return wrapper


@check_for_database
def get_job(workserver):
    keys = workserver.redis.hkeys('jobs_waiting')
    if len(keys) == 0:
        return False, jsonify({'error': 'There are no jobs available'}), 400
    url = workserver.redis.hget('jobs_waiting', keys[0])
    workserver.redis.hset('jobs_in_progress', keys[0], url)
    workserver.redis.hdel('jobs_waiting', keys[0])
    return True, keys[0].decode(), url.decode()


@check_for_database
def put_results(workserver, data):
    client_id = data.get('client_id')
    directory = data.get('directory')
    job_id = data.get('job_id', -1)
    results = data.get('results')
    filename_start = directory.rfind('/')
    if directory is None or filename_start == -1:
        body = {'error': 'No directory was included or directory was incorrect'}
        return False, jsonify(body), 400
    value = workserver.redis.hget('jobs_in_progress', job_id)
    if value is None:
        body = {'error': 'The job being completed was not in progress'}
        return False, jsonify(body), 400
    expected_client_id = workserver.redis.hget('client_jobs', job_id)
    if not client_id == expected_client_id:
        body = {'error': 'The client ID was incorrect'}
        return False, jsonify(body), 400
    workserver.redis.hdel('jobs_in_progress', job_id)
    workserver.redis.hset('jobs_done', job_id, value)
    os.makedirs(directory[:filename_start])
    with open(directory, 'w+') as file:
        file.write(json.dumps(results))
    return (True,)


@check_for_database
def get_client_id(workserver):
    workserver.redis.incr('total_num_client_ids')
    return True, int(workserver.redis.get('total_num_client_ids'))


def create_server(database):
    '''Create server, add endpoints, and return the server'''
    workserver = WorkServer(database)
    try:
        workserver.redis.keys('*')
    except redis.exceptions.ConnectionError:
        return None

    @workserver.app.route('/get_job', methods=['GET'])
    def _get_job():
        success, *values = get_job(workserver)
        if not success:
            return tuple(values)
        return jsonify({'job': {values[0]: values[1]}}), 200

    @workserver.app.route('/put_results', methods=['PUT'])
    def _put_results():
        data = request.get_json()
        if data is None:
            body = {'error': 'The body does not contain the results'}
            return jsonify(body), 400
        error = put_results(workserver, data)
        if not error[0]:
            return tuple(error[1:])
        return jsonify({'success': 'The job was successfully completed'}), 200

    @workserver.app.route('/get_client_id', methods=['GET'])
    def _get_client_id():
        success, *values = get_client_id(workserver)
        if not success:
            return tuple(values)
        return jsonify({'client_id': values[0]}), 200

    return workserver


if __name__ == '__main__':
    server = create_server(redis.Redis())
    if server is None:
        print('There is no Redis database to connect to.')
    else:
        server.app.run(host='0.0.0.0', port=8080, debug=False)
