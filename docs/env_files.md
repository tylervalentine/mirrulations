# .env Files
## Description
For clients to make calls to the Regulations.gov API, they each need a unique API key. The API key is sensitive information which SHOULD NOT be posted in the GitHub repository. Each client has a corresponding .env file in the `/env_files` directory on the server in this format:

	WORK_SERVER_HOSTNAME=___________
	WORK_SERVER_PORT=____
	API_KEY=_______________

## How to Add New Clients
To add a new client, create a new client.env file in the `env_files` directory with the next number for example: `client18.env` be sure to use the same variable names as described above or else the client will error. Next in the `docker-comose.yaml` file, add the client information in this format at the end of the file to create a new Docker container (client18 is used as an example, in any case use the next highest unused number).

	client18:
	    build:
	      context: .
	      dockerfile: mirrulations-client/Dockerfile
	    env_file: env_files/client18.env
	    restart: always

## Error Case
If a client does not have a corresponding env file the program prints `'need environment variables'` and then closes.
