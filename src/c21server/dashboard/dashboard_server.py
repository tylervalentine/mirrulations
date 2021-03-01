from flask import Flask, jsonify
from job_stats import get_jobs_stats

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_dashboard_data():
    job_information = get_jobs_stats();
    return jsonify(job_information), 200

if __name__ == '__main__':
    app.run(port=5000)
