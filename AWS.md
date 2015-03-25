#Kubernetes on Amazon EC2 cloud

The difference between installation using [README.md](README.md) and this guide
is that with this guide the installed Kubernetes **knows** it's running under AWS
and e.g. downloads list of nodes from it instead of using static configuration
file. Using [README.md](README.md) is perfectly fine if you don't need such
features.

Unlike official `cluster/kube-up.sh` script, which creates AWS networks, subnets,
routing tables, security groups, keys and whatnot from scratch (and messes up
your AWS configuration pretty much), this playbook installs and configures
Kubernetes on already running instances. You should set up your account
accordingly before. This playbook does not take any assumption about your AWS
networking and security, use whatever you find appropriate. Even the defaults
should be fine.

## Prerequisites

1. Create your AWS instances as usual, using any networking and settings. Make
   sure these conditions are met:
    * The instances can 'see' each other and there is no firewall between them.
      Of course, you should set up firewall between the instances and the
      Internet.
    * The instances are based on a Fedora image (Fedora 21 was tested).
    * `kubernetes-0.12` or newer is available through `yum` or `dnf`. At the
      time of writing this document, it was necessary to enable `updates-testing`
      repository:

          $ yum install yum-utils
          $ yum-config-manager --enable updates-testing

    * Choose an unique name of your Kubernetes cluster and add following tags
      to your AWS instances:

      Master:

          Role=<clustername>-master
          Name=<clustername>-master

      Minions, where `N` is a sequence number:

          Role=<clustername>-minion
          Name=<clustername>-minion-<N>

2. Edit `group_vars/all.yml` and configure your remote ssh account name. It's
   usually 'fedora':

        ansible_ssh_user: fedora


3. Edit `group_vars/all.yml` and configure your cluster name. The name must be
   the same as the `<clustername>` used for tags above!

        kube_aws_cluster_name: <clustername>

4. Depending on your network setup inside AWS, you may need to set up proper
   `/etc/hosts`. Make sure your instances can resolve their internal hostnames
   (such as `ip-10-3-88-220.ec2.internal`) and ping each other using them. If
   they cannot, this playbook can create appropriate `/etc/hosts` for you.
   Just enable hosts setup in `group_vars/all.yml`:

        kube_create_etc_hosts: true

5. Configure your AWS CLI according to
   http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html.
   What we really need are `~/.aws/config` and `~/.aws/credentials` files. The
   playbook will copy these files to `/etc/aws.conf` and `/etc/aws/credentials`
   on your Kubernetes master in order to download list of minios from AWS instead
   of a static configuration file.

## Network-specific configuration
This playbook can run either inside AWS (i.e. on an AWS instance with installed
ansible) or outside it (i.e. on a machine in your home / company network).

### Outside AWS
Follow these steps if you want to run this playbook on a machine outside AWS
network, for example on your home or company computer. As AWS assigns public IP
addresses of your instances dynamically, you have to edit `inventory` file every
time you (re)start your AWS instances.

1. Set up your SSH so `/bin/ssh` does not need any special arguments to access
   your instances. For example, my `~/.ssh/config` looks like:

        Host *.amazonaws.com
        IdentityFile ~/.ssh/my-aws-key.pem

2. Add external hostnames of your instances into `inventory` file. These
   hostnames are **not** stable and change with each reboot!

        [masters]
        ec2-52-1-61-250.compute-1.amazonaws.com

        [etcd]
        ec2-52-1-61-250.compute-1.amazonaws.com

        [minions]
        ec2-52-1-61-251.compute-1.amazonaws.com
        ec2-52-1-61-252.compute-1.amazonaws.com

### Inside AWS
Follow these steps if you have an AWS instance with Ansible and you want to run
this playbook there. This way, your don't need to edit your `inventory` file all
the time.

 1. Set up you ~/.ssh/config in similar way:

        Host *
        IdentityFile ~/.ssh/my-aws-key.pem

2. Add internal IP addresses of your instances into the inventory file. These IP
   addresses are stable.

        [masters]
        10.3.88.220

        [etcd]
        10.3.88.220

        [minions]
        10.3.88.221
        10.3.88.222

## Deploy
When everything is ready, you can finally run the playbook:

    $ ansible-playbook -i inventory setup.yml.

Sometimes, reboot helps to start everything in the right orded. To test your
setup, check that kubernetes knows all mininons:

    $ kubectl get nodes

