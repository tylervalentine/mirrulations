import time
from json import dumps, loads
import requests


def server_url():
    return "http://localhost:8080"


def request_job(url):
    request = requests.get(url)
    if request.status_code != 400:
        request.raise_for_status()
    work_id, work = list(loads(request.text).items())[0]
    return work_id, work


def handle_error(j_id, work, url):
    while j_id == "error":
        print(work)
        print("I'm sleeping a minute.")
        time.sleep(60)
        j_id, work = request_job(url)
    return j_id, work


def get_job(url):
    full_url = f"{url}/get_job"
    j_id, work = request_job(full_url)
    if j_id == "error":
        j_id, work = handle_error(j_id, work, full_url)
    return j_id, work


def perform_job(j):
    print(f"I am working for {j} seconds.")
    time.sleep(int(j))


def send_job_results(j_id, job_result, url):
    end_point = "/put_results"
    data = {j_id: int(job_result)}
    request = requests.put(url + end_point, data=dumps(data))
    request.raise_for_status()


def read_client_id():
    try:
        with open("client.cfg", "r") as file:
            return int(file.readline())
    except FileNotFoundError:
        return -1


def write_client_id(c_id):
    with open("client.cfg", "w") as file:
        file.write(str(c_id))


def request_client_id(url):
    end_point = "/get_client_id"
    request = requests.get(url + end_point)

    # Check if status code is 200 type code: successful GET
    if request.status_code // 100 == 2:
        c_id = int(request.json())
        write_client_id(c_id)
        return c_id
    return -1


# Reads from file, or requests if nothing there
def get_client_id():
    c_id = read_client_id()
    if c_id == -1:
        c_id = request_client_id(server_url())
    if c_id == -1:
        print("Could not get client ID!")
    return c_id


if __name__ == "__main__":
    client_id = get_client_id()
    print("ID of this client: ", client_id)

    while True:
        job_id, job = get_job(server_url())
        perform_job(job)
        send_job_results(job_id, job, server_url())
