from flask import Flask, jsonify, render_template
from flask_cors import CORS
from redis import Redis


class Dashboard:
    def __init__(self, redis_server):
        self.app = Flask(__name__)
        self.redis = redis_server
        CORS(self.app, resources={r'/data': {'origins': '*'}})


def get_jobs_stats(database):
    jobs_waiting = int(database.hlen('jobs_waiting'))
    jobs_in_progress = int(database.hlen('jobs_in_progress'))
    jobs_done = int(database.hlen('jobs_done'))
    jobs_total = jobs_waiting + jobs_in_progress + jobs_done
    client_ids = database.get('total_num_client_ids')
    clients_total = int(client_ids) if client_ids is not None else 0
    return {
        'num_jobs_waiting': jobs_waiting,
        'num_jobs_in_progress': jobs_in_progress,
        'num_jobs_done': jobs_done,
        'jobs_total': jobs_total,
        'clients_total': clients_total
    }


def create_server(database):
    dashboard = Dashboard(database)

    @dashboard.app.route('/dashboard', methods=['GET'])
    def _index():
        job_information = get_jobs_stats(dashboard.redis)
        return render_template(
            'index.html',
            jobs_waiting=job_information['num_jobs_waiting'],
            jobs_in_progress=job_information['num_jobs_in_progress'],
            jobs_done=job_information['num_jobs_done'],
            jobs_total=job_information['jobs_total'],
            clients_total=job_information['clients_total']
        )

    @dashboard.app.route('/data', methods=['GET'])
    def _get_dashboard_data():
        job_information = get_jobs_stats(dashboard.redis)
        return jsonify(job_information), 200

    return dashboard


if __name__ == '__main__':
    server = create_server(Redis())
    server.app.run(port=5000)
