import os
from datetime import datetime, timedelta
import requests
import dotenv
import redis


def get_api_key():
    dotenv.load_dotenv()
    return os.getenv('API_TOKEN')


def create_jobs(database):
    get_jobs('dockets', database)
    get_jobs('documents', database)
    get_jobs('comments', database)


def get_jobs(endpoint, database):
    params = {
        'api_key': get_api_key(),
        'sort': 'lastModifiedDate',
        'page[size]': 250
    }

    if database.exists('last_modified_date'):
        date = database.get('last_modified_date')
        params['filter[lastModifiedDate][ge]'] = date

    url = f'https://api.regulations.gov/v4/{endpoint}'
    items = make_request(url, params=params)
    total_elements = int(items.json()['meta']['totalElements'])

    while total_elements > 0:
        for page in range(1, int(items.json()['meta']['totalPages']) + 1):
            params['page[number]'] = str(page)
            items = make_request(url, params).json()
            total_elements -= write_endpoints(endpoint, database, items)
        update_filter(url, params)


def make_request(url, params):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response


def write_endpoints(endpoint, database, items):
    counter = 0
    for item in items['data']:
        database.incr('next_job_id')
        job_id = database.get('next_job_id')
        job = f'{endpoint}/{item["id"]}'
        database.hset('jobs_waiting', job_id, job)
        date = item['attributes']['lastModifiedDate']
        database.set('last_modified_date', transform_date(date))
        counter += 1
    return counter


def update_filter(url, params):
    response = make_request(url, params)
    response.raise_for_status()
    date = response.json()['data'][-1]['attributes']['lastModifiedDate']
    params['filter[lastModifiedDate][ge]'] = transform_date(date)


def transform_date(date):
    date = date.replace('T', ' ').replace('Z', '')
    return str(datetime.fromisoformat(date) + timedelta(hours=-4))


if __name__ == '__main__':
    redis_database = redis.Redis()
    try:
        redis_database.ping()
        print('Successfully connected to redis!\nGetting new jobs...')
        create_jobs(redis_database)
        print('Done!')
    except redis.exceptions.ConnectionError as r_con_error:
        print('Redis connection error:', r_con_error)
