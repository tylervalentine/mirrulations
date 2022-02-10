# .env Files
## Description
For clients to make calls to the Regulations.gov API, they each need a unique API key. The API key is sensitive information which SHOULD NOT be posted in the GitHub repository. Each client has a corresponding .env file in the `/env_files` directory on the server in this format:

	WORK_SERVER_HOSTNAME=___________
	WORK_SERVER_PORT=____
	API_KEY=_______________

## How to Add New Clients
To add a new client, create a new client.env file in the `env_files` directory with the next number for example: `client18.env` be sure to use the same variable names as described above or else the client will error.

## Error Case
If a client does not have a corresponding env file it should print `'need environment variables'` and then close.
