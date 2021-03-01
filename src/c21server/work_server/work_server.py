from flask import Flask, json, jsonify, request
from redis import Redis


class WorkServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.redis = Redis()


def create_server(server=WorkServer()):
    '''Create server, add endpoints, and return the server'''

    def get_first_key(data):
        '''Checks to make sure JSON has at least one entry and that its key-value pair are both integers
           Returns the first key value if the data is valid, otherwise returns -1
        '''
        keys = list(data.keys())
        if len(keys) > 0 and keys[0].isdigit() and data[keys[0]]:
            return keys[0]
        return -1

    @server.app.route('/get_job', methods=['GET'])
    def get_job():
        keys = server.redis.hkeys("jobs_waiting")
        if len(keys) == 0:
            return jsonify({"error": "There are no jobs available"}), 400 
        value = server.redis.hget("jobs_waiting", keys[0])
        server.redis.hdel("jobs_waiting", keys[0])
        return jsonify({keys[0].decode(): value.decode()}), 200

    @server.app.route('/put_results', methods=['PUT'])
    def put_results():
        data = json.loads(request.data)
        key = get_first_key(data)
        if (key == -1):
            return '', 400            
        print("job_id: %s, value: %s" % (key, data[key]))
        return '', 200

    return server


if __name__ == '__main__':
    server = create_server()
    server.app.run(host='0.0.0.0', port=8080, debug=False)
