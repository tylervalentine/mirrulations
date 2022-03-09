# Work Generator Documentation

## Summary
The work generator interacts with the redis database and the mirrulations core.
The work generator generates jobs for clients to complete.

### '/download'
* Gets the timestamp of the last job in the queue
* Utilizes the SearchIterator class to find a job

### '/generate_work'
* Gets an api key from local env files.
* Checks if redis database is available.
* If redis database is unavailable, sleeps for 30 seconds to give it time to load.
* Downloads dockets, documents, and comments from all jobs in the job queue.

## Main Function
* Calls the generate_work function, then sleeps for six hours