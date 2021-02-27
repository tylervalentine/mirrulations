# Redis Database Documentation

## Database Format

The database will have three hashes, with the names:

`jobs_waiting`, `in_progress`, and `done`.

Each of these hashes will store jobs for clients to process.

Keys in the hashes will be integers, the job ids of the jobs.
These keys will be mapped to integers, the values to be processed