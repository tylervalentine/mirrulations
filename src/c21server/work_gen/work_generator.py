import os
import time
from datetime import datetime, timedelta
import requests
import dotenv
import redis


dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


def make_request(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 429:
        time.sleep(3600)
        response = requests.get(url, params=params)
    response.raise_for_status()
    return response


def transform_date(response):
    """Expects date in this format yyyy-mm-dd hh:mm:ss"""
    date = response.json()['data'][-1]['attributes']['lastModifiedDate']
    date = date.replace("T", " ").replace("Z", "")

    return str(datetime.fromisoformat(date) + timedelta(hours=-4))


def update_filter(url, params):
    response = make_request(url, params)
    response.raise_for_status()
    params["filter[lastModifiedDate][ge]"] = transform_date(response)


def write_endpoints(endpoint, database):
    params = {
        "api_key": API_TOKEN,
        "sort": 'lastModifiedDate',
        "page[size]": 250
    }

    folder_path = f'regulations/{endpoint}'
    if not os.path.exists(f"{folder_path}"):
        os.makedirs(folder_path)

    url = f'https://api.regulations.gov/v4/{endpoint}'

    results = make_request(url, params=params)
    total_elements = int(results.json()['meta']['totalElements'])

    while total_elements > 0:

        try:
            for page in range(1, 21):
                params["page[number]"] = str(page)
                items = make_request(url, params).json()
                for item in items['data']:
                    temp_job = database.get('temp_job')
                    job = f"{endpoint}/{item['id']}"
                    job_id = int(temp_job) if temp_job is not None else 0
                    database.hset("jobs_waiting", job_id, job)
                    database.incr('temp_job')
                    total_elements -= 1
            update_filter(url, params)
        except IndexError:
            print("ran out of items to download")


def create_jobs(database):
    write_endpoints('dockets', database)
    write_endpoints('documents', database)
    write_endpoints('comments', database)


if __name__ == '__main__':
    redis = redis.Redis()
    try:
        redis.ping()
        print('Successfully connected to redis')
        create_jobs(redis)
    except redis.exceptions.ConnectionError as r_con_error:
        print('Redis connection error:', r_con_error)
