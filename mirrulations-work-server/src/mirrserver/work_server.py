import os
from flask import Flask, json, jsonify, request
import redis
from mirrcore.data_storage import DataStorage
from mirrcore.attachment_saver import AttachmentSaver
from mirrserver.put_results_validator import PutResultsValidator
from mirrserver.exceptions import InvalidResultsException
from mirrserver.exceptions import InvalidClientIDException
from mirrserver.exceptions import MissingClientIDException
from mirrserver.exceptions import NoJobsException
from mirrserver.get_client_id_validator import GetClientIDValidator
from mirrserver.get_job_validator import GetJobValidator


class WorkServer:
    def __init__(self, redis_server):
        self.app = Flask(__name__)
        self.redis = redis_server
        self.data = DataStorage()
        self.attachment_saver = AttachmentSaver()
        self.put_results_validator = PutResultsValidator()
        self.get_client_id_validator = GetClientIDValidator()
        self.get_job_validator = GetJobValidator()


def check_for_database(workserver):
    '''This will either succeed or raise an exception'''
    workserver.redis.ping()


def check_valid_request_client_id(workserver, client_id):
    if not check_client_id_is_valid(workserver, client_id):
        return False, jsonify({'error': 'Invalid client ID'}), 401
    return (True,)


def decrement_count(workserver, job_type):
    if job_type == 'attachments':
        workserver.redis.lpop('num_jobs_attachments_waiting')
    elif job_type == 'comments':
        workserver.redis.lpop('num_jobs_comments_waiting')
    elif job_type == 'documents':
        workserver.redis.lpop('num_jobs_documents_waiting')
    elif job_type == 'dockets':
        workserver.redis.lpop('num_jobs_dockets_waiting')


def get_job(workserver):
    '''Takes client's put endpoints validates wheter or not its a usable job...
    if so it returns the job with an ID, URL and a Type'''
    check_for_database(workserver)
    client_id = request.args.get('client_id')
    if client_id is None:
        return False, jsonify({'error': 'Client ID was not provided'}), 401
    success, *values = check_valid_request_client_id(workserver, client_id)
    if not success:
        return False, values[0], values[1]
    if workserver.redis.llen('jobs_waiting_queue') == 0:
        return False, jsonify({'error': 'No jobs available'}), 403
    job = json.loads(workserver.redis.lpop('jobs_waiting_queue'))
    job_id = job['job_id']
    url = job['url']
    job_type = job.get('job_type', 'other')
    workserver.redis.hset('jobs_in_progress', job_id, url)
    workserver.redis.hset('client_jobs', job_id, client_id)

    decrement_count(workserver, job_type)

    return True, job_id, url, job_type


def check_results(workserver, data, client_id):
    directory = data.get('directory')
    if directory is not None:
        filename_start = directory.rfind('/')
    if directory is None or filename_start == -1:
        error = {'error': 'No directory was included or was incorrect'}
        return False, jsonify(error), 403
    job_id = data.get('job_id', -1)
    expected_client_id = workserver.redis.hget('client_jobs', job_id)
    if (workserver.redis.hget('jobs_in_progress', job_id) is None or
            expected_client_id is None):
        error = {'error': 'The job being completed was not in progress'}
        return False, jsonify(error), 403
    if client_id != int(expected_client_id):
        error = {'error': 'The client ID was incorrect'}
        return False, jsonify(error), 403
    return (True, directory[:filename_start])


def write_results(directory, path, data):
    try:
        os.makedirs(f'/data/{directory}')
    except FileExistsError:
        print(f'Directory already exists in root: /data/{directory}')
    with open(f'/data/{path}', 'w+', encoding='utf8') as file:
        file.write(json.dumps(data))


def put_results(workserver, data):
    check_for_database(workserver)
    client_id = request.args.get('client_id')
    success, *values = check_valid_request_client_id(workserver, client_id)
    if not success:
        return False, values[0], values[1]
    if 'error' in data['results'] or 'errors' in data['results']:
        job_id = data['job_id']
        result = workserver.redis.hget('jobs_in_progress', job_id)
        workserver.redis.hdel('jobs_in_progress', job_id)
        workserver.redis.hset('invalid_jobs', job_id, result)
        return (True,)
    success, *results = check_results(workserver, data, int(client_id))
    if not success:
        return (success, *results)
    job_id = data['job_id']
    workserver.redis.hdel('jobs_in_progress', job_id)
    write_results(results[0], data['directory'], data['results'])
    workserver.data.add(data['results'])
    return (True,)


def put_attachment_results(workserver, data):
    check_for_database(workserver)
    client_id = request.args.get('client_id')
    success, *values = check_valid_request_client_id(workserver, client_id)
    if not success:
        return False, values[0], values[1]
    job_id = data['job_id']
    workserver.redis.hdel('jobs_in_progress', job_id)
    if data.get('results') is not None:
        workserver.attachment_saver.save(data)
    workserver.data.add(data['results'])
    return (True,)


def get_client_id(workserver):
    check_for_database(workserver)
    workserver.redis.incr('total_num_client_ids')
    return True, int(workserver.redis.get('total_num_client_ids'))


def check_client_id_is_valid(workserver, client_id):
    check_for_database(workserver)
    num_ids = workserver.redis.get('total_num_client_ids')
    total_ids = 0 if num_ids is None else int(num_ids)
    # if not client_id.isdigit():
    #     return False
    client_id = int(client_id)
    return 0 < client_id <= total_ids


def create_server(database):
    '''Create server, add endpoints, and return the server'''
    workserver = WorkServer(database)

    @workserver.app.route('/get_job', methods=['GET'])
    def _get_job():
        try:
            success, *values = get_job(workserver)
            if not success:
                return tuple(values)
            client_id = request.args.get('client_id')
            workserver.get_job_validator.check_get_jobs(client_id)
        except (MissingClientIDException, NoJobsException) as error:
            return jsonify(error.message), error.status_code
        except redis.exceptions.ConnectionError:
            return jsonify({'error': 'Cannot connect to the database'}), 500
        return jsonify({'job': {str(values[0]): values[1],
                        'job_type': values[2]}}), 200

    @workserver.app.route('/put_results', methods=['PUT'])
    def _put_results():
        data = json.loads(request.get_json())
        try:
            validator = workserver.put_results_validator.\
                check_put_results(data, request.args.get('client_id'))
        except (InvalidResultsException, InvalidClientIDException,
                MissingClientIDException) as invalid_result:
            return jsonify(invalid_result.message), invalid_result.status_code
            # REPLACE THIS LINE WITH if attachment_job(): when can check easily
            # '1234_0 is the key of an attachment in an attachment job test
        if '1234_0' in data.get('results').keys():
            success, *values = put_attachment_results(workserver, data)
        else:
            success, *values = put_results(workserver, data)
        if not success:
            return tuple(values)
        return jsonify(validator[0]), validator[1]

    @workserver.app.route('/get_client_id', methods=['GET'])
    def _get_client_id():
        try:
            success, *values = get_client_id(workserver)
            if not success:
                return tuple(values)
            return jsonify({'client_id': values[0]}), 200
        except redis.exceptions.ConnectionError:
            return jsonify({'error': 'Cannot connect to the database'}), 500

    return workserver


if __name__ == '__main__':
    try:
        r = redis.Redis('redis')
        r.keys('*')
        server = create_server(r)
        server.app.run(host='0.0.0.0', port=8080, debug=False)
    except redis.exceptions.ConnectionError:
        print('There is no Redis database to connect to.')
