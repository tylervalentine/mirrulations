# Work Generator Documentation

## Summary
The work generator interacts with Regulations.gov directly. It uses a personal API key to check to see if anything new has been posted on the website. If there is something new-- meaning if the gathered link(s) are not in Redis-- the work genrator will generate jobs for the client to complete.

### `def download()`
* Gets the timestamp of the last known job in the queue
* Utilizes the `SearchIterator` class to find a job, from the timestamp of the last known job, and returns a URL for the specific element.
* Takes up to 250 jobs at a time.
* If the jobs are not in Redis, it will add the URL to the `jobs_queue` in the Redis server.

### `def generate_work()`
* Gets an API key from local env files.
* Checks if Redis database is available.
* If Redis database is unavailable, sleeps for 30 seconds to give it time to load.
* Downloads dockets, documents, and comments from all jobs in the job queue.

## Main Function
* Contains the `generate_work` function
* Checks Regulations.gov every six hours