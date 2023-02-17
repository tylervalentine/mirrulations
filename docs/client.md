# Client Documentation


## Summary
The clients are their own objects that will connect to the work server, receive work, 
and send results back to the server by making the calls to [regulations.gov]
(https://www.regulations.gov/) for data downloads. 

## Description 
Multiple clients will be able to connect to the work server at once. The goal is 
that the client will request and complete work in order to download data from 
[regulations.gov](https://www.regulations.gov/) to disk. 


### `/get_job`
Makes a request to get a specific with an endpoint consisting of the Job's URL and the clients ID. Makes sure there is an available job and saves the Job's URL, ID and Type, i.e Attachment, Comment, Doc..

### `/execute_task`
Will be used to call get_job, printing updates along the way. Will eventually have an if statement to separate the calls for different job types. Is able to call perform_job, using the Job's url+endpoint, and then once the results have been find, the job results are sent back to the server.  



