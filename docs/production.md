

# Production Environment Documentation


## Summary
The Production Environment has been setup to establish a secure separation from server side and client functionality, and ensure requests are being received securely and asynchronously.

## Description
Nginx and Gunicorn have been implemented to provide efficient load balancing and asynchronous server connections from multiple clients.


The Vagrant File is designed to automatically create an instance of a virtual machine on the Capstone2021 Virtual Box.

This Vagrant File can also be used for testing new features on your local machine.

## Usage

* Install Vagrant and Virtualbox on your machine

* Use `sudo vagrant up` to run the vagrant file and start the VM headless.

* Run `sudo vagrant ssh` to ssh into the VM

* To stop the machine, run `sudo vagrant suspend`

* To destroy the machine, run `sudo vagrant destroy -f`

## Setup of Demo

* In your local repo, create the folder `src/c21server/data` as well as `src/c21server/work_server/data`
* Place the `dockets_0.txt` file in the `src/c21server/data` directory so that the work generator has the necessary Docket IDs

* At this point, check the [Client Documentation](https://github.com/cs334s21/capstone2021/blob/main/docs/client.md) for information on how to run clients.

	* **Make sure to delete your `client.cfg` file each time you destroy and rebuild your Vagrant instance**
	* **Set your client `self.url` to `localhost/work`**

* If you are testing locally, results will appear on **localhost**

* If it is run on the virtual machine, it will appear on **capstone.cs.moravian.edu**

* With both URL's, the work server can be accessed using `/work/{endpoint}` and dashboard can be accessed using `/dashboard/{endpoint}`
