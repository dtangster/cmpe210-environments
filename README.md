# CMPE210 Environments

This project was created to more easily spin up environments we commonly use in class.

It allows you to spin up an environment for Ryu, Mininet, and Flowvisor.

## Prerequisites

The machine you plan to use to run these instructions on must be Linux based. Although
containers are often advertised as write once run anywhere, that is not completely true.

Mac OSX and Windows version of docker-ce uses an emulated linux kernel. By chance,
Mininet happens to require a kernel module and it won't be able to find what it needs.

If you are not running Linux, consider spinning up a Linux distribution in a VM.

## Environment Setup

1. Install docker-ce. Follow the instructions from one of the following links:

https://docs.docker.com/install/linux/docker-ce/debian/
https://docs.docker.com/install/linux/docker-ce/ubuntu/
https://docs.docker.com/install/linux/docker-ce/fedora/

2. Install docker-compose

```bash
pip install docker-compose
```

## Starting the containers

```bash
docker-compose up
```

If you want to only run one services listed in `docker-compose.yml` instead of all
of them, run:

```bash
docker-compose up < ryu | mininet | flowvisor >
```

## Going inside a container

Find out what the container id is by running:
```bash
docker ps
```
Once you have found the container id, run:
```bash
docker exec -it <CONTAINER ID> bash
```

## Communicating among containers

When you are inside a container, you can refer to another container by its service name
rather than IP address. For instance:
```bash
docker exec -it <MININET_ID> bash
# You should get a bash prompt inside the container
ping ryu
```

## Making changes to example code

If you want to make changes to the Ryu controller or Mininet topology code, feel
free to do so. The next time you try to start the containers, it will automatically
pull in the new code and try to run it as long as you provide it `--build`.

For instance:

```bash
docker-compose up --build
```
