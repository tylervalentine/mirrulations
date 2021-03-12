from c21server.dashboard.dashboard_server import create_server


def test_dashboard_returns_job_information():
    database = Database()
    server = create_server(database)
    server.app.config['TESTING'] = True
    client = server.app.test_client()

    response = client.get('/data')

    assert response.status_code == 200
    expected = {
        'num_jobs_waiting': 5,
        'num_jobs_in_progress': 4,
        'num_jobs_done': 3,
        'jobs_total': 12,
        'clients_total': 2
    }

    assert response.get_json() == expected


class Database:
    def __init__(self):
        self.data = {
            'jobs_waiting': 5,
            'jobs_in_progress': 4,
            'jobs_done': 3,
            'total_num_client_ids': 2
        }

    def hlen(self, key):
        return self.data[key]

    def get(self, key):
        return self.data[key]
