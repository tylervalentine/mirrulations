from redis import Redis
from flask import Flask, jsonify

r = Redis()
app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_dashboard_data():
    return jsonify({'num_jobs_waiting' : int(r.hlen('jobs_waiting'))}), 200


if __name__ == '__main__':
    app.run(port=5000)
