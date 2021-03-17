***API Documentation***

What a job looks like
**To Be Added**
	
**How to receive all data**
	To iterate through the first 5,000 items, we iterate through 250 items in each page, there are 20 pages per grouping which gives up a total of 5,000 items. We then note last item’s last modified date down to the second. Then iterate through the next 5,000 items starting with the last item noted as the parameter to filter everything after the parameter noted. Repeat. We are sorting by the last modified date.
	
**Job Generator Endpoints**
	*Three job generating endpoints*
	
	Dockets - Parent of Documents
	
	Documents - Parent of Comments
	
	Comments - Child of Documents
	
**Check data overlaps between endpoints**
	*Comments* - Missing fields in detailed comments `lastModifieDdate` and `highlightedContent`

