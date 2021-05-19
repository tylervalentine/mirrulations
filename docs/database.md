# Redis Database Documentation

## Database Format

The database has three "tables", with the names:

`jobs_waiting_queue`, `jobs_in_progress`, and `jobs_done`.

`jobs_waiting_queue` is a list, while 'jobs_in_progress' and 'jobs_done' are hashes.
Each stores jobs for clients to process.

Keys will be integers, the job ids of the jobs.
These keys will be mapped to integers, the values to be processed.

Additionally, the database has an integer value storing the number of clients:
`total_num_client_ids`.

## Redis Format
## `jobs_waiting_queue`

This list holds JSON strings representing each job (a job_id and a url) 

>['{"job_id" :[value], "url": [value] }',  '{"job_id" :[value], "url": [value] }', ... ]

## `jobs_in_progress`
> { [job_id] : [value] } 

## `jobs_done`
> { [job_id] : [result_value] }

## `client_jobs`
> { [job_id] : [client_id] } 


