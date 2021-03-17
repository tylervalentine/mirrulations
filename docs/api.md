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

The syntax for a single call to actually do this is as follows:
```
https://api.regulations.gov/v4/END_POINT?page[size]=250&page[number]=PAGE_NUMBER&sort=lastModifiedDate,documentId&api_key=API_KEY
```


Where `END_POINT`, `PAGE_NUMBER`, and `API_KEY` are variables you put in. The max value for the page number is 20, and since each page only holds 250 items you can only get 5000 items with this format.

Once you hit those 5000 items, you'll need to add the last modified date filter, using the oldest (last) date in the set of 5000:
`filter[lastModifiedDate][ge]=2020-08-10 11:58:52 `

To basically cut off the first 5000 items you got and then continue the same way from there.

```
Added onto the first example URL/call:
https://api.regulations.gov/v4/END_POINT?filter[lastModifiedDate][ge]=2020-08-10 11:58:52&page[size]=250&page[number]=PAGE_NUMBER&sort=lastModifiedDate,documentId&api_key=API_KEY
```
	
### **Job Generator Endpoints**
***Three job generating endpoints***
	
Dockets - Parent of Documents
	
Documents - Parent of Comments
	
Comments - Child of Documents
	
### **Check data overlaps between endpoints**
*Comments* - Missing fields in detailed view for comments `lastModifieDate` and `highlightedContent`

*Documents* - Missing fields in detailed view for Documents `lastModifieDate` and `highlightedContent`

*Dockets* - Missing fields in detailed view for Dockets `lastModifieDate` and `highlightedContent`


***Additional Notes***
`lastModifiedDate` and `ModifyDate` have the same values. Non-detailed view for all types have `modifyDate` instead of `lastModifiedDate`