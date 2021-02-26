# Redis Database Documentation

## Database Format

The database will have three lists, with the names:

`job_queue`, `in_progress`, and `done`.

Each of these lists will store jobs for clients to process.

An individual job will be represented as a dict:

{`job_id`: 5, `value`: 3}

with the keys shown here mapping to integers; 5 and 3 in this example, respectively.

Each queue will hold some number of dicts representing jobs.