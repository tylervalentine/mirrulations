# `.env Files`
## Description
For clients to make calls to the Regulations.gov API, they each need a unique API key. The API key is sensitive information which SHOULD NOT be posted in the GitHub repository. Each client has a corresponding `.env` file in the `/env_files` directory on the server in this format:

	WORK_SERVER_HOSTNAME=___________
	WORK_SERVER_PORT=____
	API_KEY=_______________
	ID=____
    PYTHONUNBUFFERED=TRUE

The `PYTHONUNBUFFERED=TRUE` tells Python to output immediately so that we can view logs in realtime.

## How to Add New Clients
To add a new client, 

1. In the `docker-compose.yaml` file, add the client information in this format at the end of the file to create a new Docker container (client18 is used as an example, in any case use the next highest unused number).

		client18:
		    build:
		      context: .
		      dockerfile: mirrulations-client/Dockerfile
		    env_file: env_files/client18.env
		    restart: always

2. Run dev_setup.py to add the new client into `env_files` folder.

## Error Case
If a client does not have a corresponding env file the program prints `'need environment variables'` and then closes.
