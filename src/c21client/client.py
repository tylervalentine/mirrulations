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
	data = {work_id:int(work)}
	request = requests.put(url + end_point, data=dumps(data))
	request.raise_for_status()


if __name__ == "__main__":
	while(True):
		work_id, work = get_work(server_url())
		do_work(work)
		send_work(work_id, work, server_url())