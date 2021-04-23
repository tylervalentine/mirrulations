# Client Documentation


## Summary
The clients are their own objects that will connect to the work server, receive work, and send results back to the server by making the calls to [regulations.gov](https://www.regulations.gov/) for data downloads. 

## Description 
Multiple clients will be able to connect to the work server at once. A client will also try to get a `client_id` if it doesn't have one already. The goal is that the client will request and complete work in order to download data from [regulations.gov](https://www.regulations.gov/) to disk. 

## Set Up
Make sure you have the `dockets_0.txt.` file downloaded in order for the client to function properly. Additionally, you should have a `.env` file in `src/c21client` in order for the client to correctly make calls to [regulations.gov](https://www.regulations.gov/). Check the [README](https://github.com/cs334s21/capstone2021/blob/main/README.md) for more details on how to set this up. 

## Implmentation
The client will request work from the work server and the client will return the work when it is complete. If the work server cannot provide the client with work, the client will then sleep for a minute and then try to request work again. It will follow that cycle for as long it is connected to the work server.

For implementation, the client has been refactored to its own class with its own methods. In `client.py`, there are also helper functions and a `__main__`, which you can look over to understand the client's functionality. Error handling for interaction with the server is implemented.  

## Data Formatting
To see the how the data is formatted when the client recieves work or pushes back results, read [work server docs](https://github.com/cs334s21/capstone2021/blob/main/docs/work_server.md). You can also see the server's endpoints to get a better understanding. 

Additionally, check [regulations docs](https://github.com/cs334s21/capstone2021/blob/main/docs/regulations.md) for information on the structure of the data downloads and the api used. 

