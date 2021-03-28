import redis


def generate_jobs(database, job_filename, start_key=0):

    url_base = 'https://api.regulations.gov/v4/'

    print(f'I am generating work from this file: {job_filename}')
    with open(job_filename, "r") as job_file:

        for line in job_file:

            # Check for bad data
            if len(line.split("/")) != 2:
                print('Bad line in file! Line was: {line}')
                raise Exception

            # [:-1] is to remove the return character before making the call
            url = url_base + line[:-1]
            database.hset('jobs_waiting', start_key, url)
            start_key += 1
    print(f'I\'ve finished generating work from this file: {job_filename}')


if __name__ == '__main__':
    redis_database = redis.Redis()
    try:
        redis_database.ping()
        print('Successfully connected to redis')
        generate_jobs(redis_database, 'src/c21server/data/dockets_0.txt')
    except redis.exceptions.ConnectionError as r_con_error:
        print('Redis connection error:', r_con_error)
