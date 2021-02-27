# Redis Database Documentation

## Database Format

The database will have three hash maps, with the names:

`jobs_waiting`, `in_progress`, and `done`.

Each of these lists will store jobs for clients to process.

Keys in the hash sets will be integers, the job ids of the jobs.
These keys will be mapped to integers, the valuese