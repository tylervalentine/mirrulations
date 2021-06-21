# Client Documentation


## Summary
The clients are their own objects that will connect to the work server, receive work, 
and send results back to the server by making the calls to [regulations.gov]
(https://www.regulations.gov/) for data downloads. 

## Description 
Multiple clients will be able to connect to the work server at once. A client 
will also try to get a `client_id` if it doesn't have one already. The goal is 
that the client will request and complete work in order to download data from 
[regulations.gov](https://www.regulations.gov/) to disk. 



