from flask import Flask, json, jsonify, request
import redis


class WorkServer:
    def __init__(self, redis_server):
        self.app = Flask(__name__)
        self.redis = redis_server


def get_first_key(data):
    '''
    Checks to make sure JSON has at least one entry and that its
        key-value pair are both integers. Returns the first key value
        if the data is valid, otherwise returns -1.
    '''
    if data is not None:
        keys = list(data.keys())
        is_key_digit = len(keys) > 0 and keys[0].isdigit()
        if is_key_digit and isinstance(data[keys[0]], int):
            return keys[0]
    return -1


def check_for_database(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except redis.exceptions.ConnectionError:
            body = {'error': 'Cannot connect to the database'}
            return False, jsonify(body), 500
    return wrapper


def check_request_had_valid_client_id(workserver, data):
    if data is None or 'client_id' not in data:
        return False, jsonify({'error': 'Client ID was not provided'}), 401
    if not check_client_id_is_valid(workserver, data['client_id']):
        return False, jsonify({'error': 'Invalid client ID'}), 401
    return (True,)


@check_for_database
def get_job(workserver, data):
    success, *values = check_request_had_valid_client_id(workserver, data)
    if not success:
        return False, values[0], values[1]
    keys = workserver.redis.hkeys('jobs_waiting')
    if len(keys) == 0:
        return False, jsonify({'error': 'There are no jobs available'}), 400
    value = workserver.redis.hget('jobs_waiting', keys[0])
    workserver.redis.hset('jobs_in_progress', keys[0], value)
    workserver.redis.hset('client_jobs', keys[0], data['client_id'])
    workserver.redis.hdel('jobs_waiting', keys[0])
    return True, keys[0].decode(), value.decode()


@check_for_database
def put_results(workserver, data):
    success, *values = check_request_had_valid_client_id(workserver, data)
    if not success:
        return False, values[0], values[1]
    key = get_first_key(data)
    value = workserver.redis.hget('jobs_in_progress', key)
    if value is None:
        body = {'error': 'The job being completed was not in progress'}
        return False, jsonify(body), 400
    workserver.redis.hdel('jobs_in_progress', key)
    workserver.redis.hset('jobs_done', key, value)
    return (True,)


@check_for_database
def get_client_id(workserver):
    workserver.redis.incr('total_num_client_ids')
    return True, int(workserver.redis.get('total_num_client_ids'))


@check_for_database
def check_client_id_is_valid(workserver, client_id):
    num_ids = workserver.redis.get('total_num_client_ids')
    total_ids = 0 if num_ids is None else int(num_ids)
    return isinstance(client_id, int) and 0 < client_id <= total_ids


def create_server(database):
    '''Create server, add endpoints, and return the server'''
    workserver = WorkServer(database)
    try:
        workserver.redis.keys('*')
    except redis.exceptions.ConnectionError:
        return None

    @workserver.app.route('/get_job', methods=['GET'])
    def _get_job():
        data = request.get_json()
        success, *values = get_job(workserver, data)
        if not success:
            return tuple(values)
        return jsonify({'job': {values[0]: values[1]}}), 200

    @workserver.app.route('/put_results', methods=['PUT'])
    def _put_results():
        data = request.get_json()
        if data is None or 'results' not in data:
            body = {'error': 'The body does not contain the results'}
            return jsonify(body), 400
        success, *values = put_results(workserver, data)
        if not success:
            return tuple(values)
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
