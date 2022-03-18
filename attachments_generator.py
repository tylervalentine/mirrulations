

'''

- this sprint we need to generate these jobs (attachments)
- when jobs generate they also need to generate the attachments (most ikely will stay on generator side)
- there will be the one time 15m job script that we will run and we will deploy the process of keeping up (next sprint)
- For now envision a program that basically for count in range (some have attachments)
- its not about downlaod its about the download_job_type : attachments
- Coordinate with client team
- When it gets to client we need to coordinate with client of what we are generating 
- conseptually this demo script wont need to be tested
- if it becomes a blocker of 95% coleman can fix it
- we need a script that can excecute that many jobs. Write program that will generate job
- get job id, get job type: attachments, something to be determined of the field that is going to have a rand int (1-5)
- put together in a dict do a json dump s turn into string put that in job loading queue
- because we understand jobs waiting queue and the last_job_id you know what it is supposed to look like you can use that code to load it in a redis database
- interact with redis in that form
COLEMAN IDEA
- add another dockercontainer to the system that will encapsulate that little script 
- done in PR add DC
- make container then gets launched normal with devup and it runs and does its thing 
- that can work OR
- could be a standalone script and i beleive in the docker compsoe file we expose the port for docker 
- 6379 if you do a devup if you have it installed on your machine the redis port will be mapped from the redis port to the local host
- attachments generator
- attachment generator to port 6379 mapped to 6379
~/data/redis delete dump-rdb


'''
