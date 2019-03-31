# CMPE210 Environments

This project was created to more easily spin up environments we commonly use in class.

It allows you to spin up an environment for Ryu, Floodlight, Mininet, and Flowvisor.

The default application currently spins up an arbitrary Mininet topology and does a
`pingall` every 30 seconds while connected to the Ryu controller.

Included is also a Docker environment that allows you to try out the Flowvisor Exercise
found at: https://github.com/onstutorial/onstutorial/wiki/Flowvisor-Exercise

The image/container name is `onstutorial`. This image has the following:

1. Mininet
2. Flowvisor
3. The Flowvisor exercise cloned into /onstutorial

# Doing the Flowvisor Exercise

There seem to be issues with the `beacon` binary and you cannot execute it. As a workaround,
you can use the `ryu` and `floodlight` controllers to finish the tutorial. In order to do this,
perform the following:

1. We only want to spin up the `onstutorial` container when doing this exercise.
```bash
docker-compose up --build onstutorial
```

2. All repositories are checked out at `/`. When starting the Mininet network, run the
following instead:
```bash
mn --custom /onstutorial/flowvisor_scripts/flowvisor_topo.py \
   --topo fvtopo --link tc --controller remote --mac --arp
```

3. Start following the tutorial from the following command
```bash
sudo /etc/init.d/flowvisor start
```

Whenever you see errors like `/root/.pyenv/libexec/pyenv: line 44: cd: fvctl-json: Not a directory`,
ignore it.

4. Replace steps that require you to start up the controller.

When you run the commands below you might see errors like `error: [Errno 98] Address already in use`.
You can ignore this error.

Replace
```bash
cd ~/onstutorial/beacon-fvexercise-controller1
./beacon
```
with
```bash
cd /ryu
PYTHONPATH=. bin/ryu-manager ryu/app/simple_switch.py &
```

Replace
```bash
cd ~/onstutorial/beacon-fvexercise-controller2
./beacon
```
with
```bash
cd /ryu2
PYTHONPATH=. bin/ryu-manager ryu/app/simple_switch.py &
```

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
docker-compose up --build
```

If you want to only run one services listed in `docker-compose.yml` instead of all
of them, run:

```bash
docker-compose up --build < ryu | floodlight | mininet | flowvisor >
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

## Connect Mininet to a different controller

By default, Mininet connects to Ryu. If you would like it to use Floodlight instead, run:
```bash
CONTROLLER=floodlight docker-compose up --build
```

## Navigating the controller UI via a browser

We are binding the host port to the container port. Since this project starts up Ryu and
Floodlight and they both occupy the same port for the UI, we cannot use the same ports for
both on the host.

Ryu port mapping:  8080 -> 8080  
Flowlight port mapping:  8090 -> 8080

The above means that if you want to access the UI, you will need to type in one of the
following in the browser:

<HOST_IP>:8080/<REMAINING_URL>

or

<HOST_IP>:8090/<REMAINING_URL>

## Overriding the UI port for the controller

You can override one or both of the host ports that bind to the containers.
```bash
# With the following example you will need to use port 10000 in the browser to access Ryu's UI
RYU_PORT=10000 docker-compose up --build

# With the following example you will need to use:
# port 9000 to access Ryu's UI
# port 9999 to access Floodlight's UI
RYU_PORT=9000 FLOODLIGHT_PORT=9999 docker-compose up --build
```

## Making changes to example code

If you want to make changes to the Ryu controller or Mininet topology code, feel
free to do so. The next time you try to start the containers, it will automatically
pull in the new code and try to run it as long as you provide it `--build`.

For instance:

```bash
docker-compose up --build
```
