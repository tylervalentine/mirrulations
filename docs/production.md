

# Production Environment Documentation


## Summary
The Production Environment has been setup to establish a secure separation from server side and client functionality, and ensure requests are being received securely and asynchronously.

## Description
Nginx and Gunicorn have been implemented to provide efficient load balancing and asynchronous server connections from multiple clients.


The Vagrant File is designed to automatically create an instance of a virtual machine on the Capstone2021 Virtual Box.

## Usage

* Install Vagrant on your machine
* To create a vagrant file, run "**vagrant init**" in desired directory
* Use "**vagrant up**" to run the vagrant file and start the VM headless.
* Run "**vagrant ssh**" to ssh into the VM
* To stop the machine, run "**vagrant suspend**"
* To destroy (shutdown) the machine, run "**vagrant destroy -f**"
