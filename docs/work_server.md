# Work Server Documentation

## Summary
The work server interacts with a Redis database and clients.
The clients call the endpoints of the work server which either returns a job for them to complete or accepts the results of a job.


## Work Server Endpoints
It is required that the values `job_id`, `value`, and `result_value` are integers.

### `/get_job`
* Gets a job from the Redis database stored in the `jobs_waiting` hash to return to a client
* Returns JSON in the body of the HTTP response
* If there is not a job in the database or there is no database to connect to, then it returns 400 and the JSON
``` {"error": "There are no jobs available"} ```
and 
```{"error": "There is no database available"}```, respectively.
* Otherwise if there is a job, then it returns 200 and the JSON
```
{
    "client_id": [client_id]
    "job": {[job_id]: [value]}
}
```

### `/put_results`
* Accepts the results of a job from a client
* Expects a request with a body of the form
```
{
    "client_id": [client_id]
    "results": {[job_id]: [value]}
}
```
* If the body is incorrect it returns a 400 and an empty body
* Otherwise it returns a 200 and an empty body
