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


def check_results(workserver, data):
    directory = data.get('directory')
    if directory is not None:
        filename_start = directory.rfind('/')
    if directory is None or filename_start == -1:
        error = {'error': 'No directory was included or was incorrect'}
        return False, jsonify(error), 400
    job_id = data.get('job_id', -1)
    value = workserver.redis.hget('jobs_in_progress', job_id)
    if value is None:
        error = {'error': 'The job being completed was not in progress'}
        return False, jsonify(error), 400
    expected_client_id = int(workserver.redis.get('total_num_client_ids'))
    if data.get('client_id') != expected_client_id:
        error = {'error': 'The client ID was incorrect'}
        return False, jsonify(error), 400
    return (True, directory[:filename_start])


def write_results(directory, path, data):
    try:
        os.makedirs(f'../../../data/{directory}')
    except FileExistsError:
        print(f'Directory already exists in root: data/{directory}')
    with open(f'../../../data/{path}', 'w+') as file:
        file.write(json.dumps(data))


@check_for_database
def put_results(workserver, data):
    path = data.get('directory')
    success, *results = check_results(workserver, data)
    if not success:
        return (success, *results)
    job_id = data.get('job_id', -1)
    result = workserver.redis.hget('jobs_in_progress', job_id)
    workserver.redis.hdel('jobs_in_progress', job_id)
    workserver.redis.hset('jobs_done', job_id, result)
    write_results(results[0], path, data.get('results'))
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
        print(request)
        data = json.loads(request.get_data())
        if data is None or data.get('results') is None:
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
