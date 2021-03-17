## ***API Documentation***

### **What a Job is**

A job is: {job_id, endpoint, variables}

Where job\_id is an integer, a job ID is mostly for the work server to use.

Endpoint is a string; either "dockets", "documents", or "comments".

Variables is a list of strings, each string representing an ID of a docket/document/comment in the regulations database, 
ex: "FMCSA-1997-2350-2476".

In our code we can represent this with a python dictionary, and we can easily convert said dictionary into a string with the JSON library for transferring between parts of our implementation.
	
### **How to receive all data**

To iterate through the first 5,000 items, we iterate through 250 items in each page, there are 20 pages per grouping which gives up a total of 5,000 items. 
We then note last item’s last modified date down to the second. 
Then iterate through the next 5,000 items starting with the last item noted as the parameter to filter everything after the parameter noted. Repeat. We are sorting by the last modified date.
	
### **Job Generator Endpoints**
***Three job generating endpoints***
	
Dockets - Parent of Documents
	
Documents - Parent of Comments
	
Comments - Child of Documents
	
### **Check data overlaps between endpoints**
*Comments* - Missing fields in detailed comments `lastModifieDdate` and `highlightedContent`

