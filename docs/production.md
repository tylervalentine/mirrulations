



## Production Environment Documentation

The system is Dockerized into a number of components:

* `nginx` - A reverse proxy that routes requests to the dashboard
* `redis` - Job management as well as permanent variable storage
* `mongo` - Storage of dockets, documents, comments and attachments(in parallel with disk storage)
* `work_generator` - Crawl through the regulations.gov results to find missing data
* `work_server` - Server jobs to clients and save results
* `rabbitmq` - Job Queue Management
* `extractor` - Text extractor for pdfs
* `dashboard` - Web-based user interface to observe progress 
* `client1` through `client27` - Clients that download data from regulations.gov

## Docker Compose commands

* `docker compose build` to build containers
* `docker compose up -d` to start all containers (`-d` to run in background)
* `docker compose logs` to see logs.  Optional, add a container name to see
  individual logs
* `docker compose down` to bring the system down
* `docker compose stop <name>` to stop a particular container
* `docker compose ps` list all of the docker containers and their states
