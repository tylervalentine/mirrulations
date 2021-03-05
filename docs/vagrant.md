
## Overview

[Vagrant](https://www.vagrantup.com/) is a technology to automate 
the creation of virtual machines.  We will use it to create a
collection of machines we can use for *development* and *testing*.
We can use these machines for our end-of-sprint demos.

## Vagrantfile

The `Vagrantfile` specifies how to create each instance.  See
the [Vagrantfile documentation](https://www.vagrantup.com/docs/vagrantfile) 
for more details of the allowable language.

At a high level, our `Vagrantfile`:

* Creates virtual machines for the `workserver`, `client`(s), `workgenerator`
  and `dashboardserver`.
* All machines run on a private network that makes each machine accessible
  to each other
* We will clone the `capstone2021` repo on each virtual machine and then
  configure and start the appropriate portion of the project.

## Usage

See the [Vagrant documentation](https://www.vagrantup.com/docs) for complete
details of the available commands.

* To start the virtual machines, run `vagrant up`
* To connect to one of the virtual machines, run `vagrant ssh workserver`,
  `vagrant ssh client`, etc.
* To destroy (shutdown) all machines run `vagrant destroy -f`



