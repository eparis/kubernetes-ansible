# Kubernetes-ansible

This playbook helps you to set up a Kubernetes cluster on a number of Fedora or
RHEL machines. Doesn't matter how or where or whatever.  Real hardware, VMs,
honey badger don't care.

Follow [AWS.md](AWS.md) if you want to install Kubernetes, which is aware of AWS
and e.g. can download list of minions from AWS itself instead of static
configuration file.

## Usage

Record the IP address of which machine you want to be your master
Record the IP address of the machine you want to be your etcd server
Record the IP addresses of the machines you want to be your minions.

Stick the system information into the 'inventory' file.

###  Set up ssh access via public keys

See the `pre-setup/` directory.

### Set up the services IP addresses

Kubernetes services have fake IP addresses.  You must specify a range of IP
addresses which will not conflict with anything in your infrastructure which
kube can use for services. These addresses do not need to be routable and must
just be an unused block of space. To do so edit `group_vars/all.yml`.

### Set up the actual kubernetes cluster

You already did the config!  Just run the setup::

    $ ansible-playbook -i inventory setup.yml

This works on RHEL7, Atomic, F20, F21 and rawhide.

For RHEL7 it will set up rhn subscriptions.  Put your username in a file named
`~/rhn_username`.  Put your rhn password into a file named `~/rhn_password`.

### Set up flannel, a network overlay (optional)

Again, you need to edit `group_vars/all.yml`.

Assign the entire address space which flannel should use for an overlay
network. Again, your network infrastructure does not need to know about and
should not use any addresses in this range. Pods will be assigned addresses
in this range, but the routing between pods will be over the flannel controlled
overlay network, NOT your network infrastructure.
