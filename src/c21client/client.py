import requests
import time
from json import dumps, loads


def server_url():
    return "http://localhost:8080"


def try_to_get_work(url):
    request = requests.get(url)
    if(request.status_code != 400):
        request.raise_for_status()
    work_id, work = list(loads(request.text).items())[0]
    return work_id, work


def handle_error(work_id, work, url):
    while work_id == "error":
        print(work)
        print("I'm sleeping a minute.")
        time.sleep(60)
        work_id, work = try_to_get_work(url)
    return work_id, work


def get_work(url):
    full_url = f"{url}/get_job"
    work_id, work = try_to_get_work(full_url)
    if work_id == "error":
        work_id, work = handle_error(work_id, work, full_url)
    return work_id, work


def do_work(work):
    print(f"I am working for {work} seconds.")
    time.sleep(int(work))


def send_work(work_id, work, url):
    end_point = "/put_results"
    data = {work_id: int(work)}
    request = requests.put(url + end_point, data=dumps(data))
    request.raise_for_status()


def read_client_id():
    try:
        with open("client.cfg", "r") as file:
            return int(file.readline())
    except FileNotFoundError:
        return -1


def write_client_id(id):
    with open("client.cfg", "w") as file:
        file.write(str(id))


def request_client_id(url):
    end_point = "/get_id"
    request = requests.get(url + end_point)

    # Check if status code is 200 type code: successful GET
    if request.status_code // 100 == 2:
        id = int(request.json())
        write_client_id(id)
        return id
    else:
        return -1


# Reads from file, or requests if nothing there
def get_client_id():
    id = read_client_id()
    if id == -1:
        id = request_client_id(server_url())
    if id == -1:
        print("Could not get client ID!")
    return id


if __name__ == "__main__":
    client_id = get_client_id()
    print("ID of this client: ", client_id)

    while(True):
        work_id, work = get_work(server_url())
        do_work(work)
        send_work(work_id, work, server_url())
