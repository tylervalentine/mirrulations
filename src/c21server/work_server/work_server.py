from flask import Flask, json, jsonify, request
from redis import Redis


class WorkServer:
    def __init__(self, redis_server):
        self.app = Flask(__name__)
        self.redis = redis_server


def create_server(database):
    '''Create server, add endpoints, and return the server'''
    workserver = WorkServer(database)

    def _get_first_key(data):
        '''Checks to make sure JSON has at least one entry and that its
           key-value pair are both integers. Returns the first key value
           if the data is valid, otherwise returns -1.
        '''
        keys = list(data.keys())
        is_key_digit = len(keys) > 0 and keys[0].isdigit()
        if is_key_digit and isinstance(data[keys[0]], int):
            return keys[0]
        return -1

    @workserver.app.route('/get_job', methods=['GET'])
    def _get_job():
        keys = workserver.redis.hkeys("jobs_waiting")
        if len(keys) == 0:
            return jsonify({"error": "There are no jobs available"}), 400
        value = workserver.redis.hget("jobs_waiting", keys[0])
        workserver.redis.hset("jobs_in_progress", keys[0], value)
        workserver.redis.hdel("jobs_waiting", keys[0])
        return jsonify({keys[0].decode(): value.decode()}), 200

    @workserver.app.route('/put_results', methods=['PUT'])
    def _put_results():
        data = json.loads(request.data)
        key = _get_first_key(data)
        value = workserver.redis.hget("jobs_in_progress", key)
        if key == -1 or value is None:
            return '', 400
        workserver.redis.hdel("jobs_in_progress", key)
        workserver.redis.hset("jobs_done", key, data[key])
        'print("job_id: %s, value: %s" % (key, data[key]))''
        return '', 200

    @workserver.app.route('/get_client_id', methods=['GET'])
    def get_client_id():
        client_id = server.redis.get('total_num_client_ids')
        if client_id is None:
            client_id = 0
        server.redis.incr('total_num_client_ids')
        return client_id, 200

    return workserver


if __name__ == '__main__':
    server = create_server(Redis())
    server.app.run(host='0.0.0.0', port=8080, debug=False)
