# Doc for Basic form of an Attachment Job

Work generator creates an API call for comments. 

An example of an API call to comments is:
- https://api.regulations.gov/v4/comments/CMS-2022-0012-0392/?api_key=<API_KEY>

The returned json object may or may not contain an attachment.

### After all jobs are completed

Create jobs for all comments in the work generator, this time with the addition of the 'attachments' endpoint at the end of each call.

Create a separate download function in the WorkGenerator since we are going through our own stored API calls. You won't need the SearchIterator either.

Add an 'attachments' endpoint at the end of each comment api calls.
For example:
- https://api.regulations.gov/v4/comments/CMS-2022-0012-0392/attachments?api_key=<API_KEY>

Add api call to the job_queue.

Note:
The resulting json object from an api call with comments and attachments will contain a name "data".
If the value is an empty list that means there are no attachments for that comment.