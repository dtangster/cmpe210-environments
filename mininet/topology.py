#!/usr/bin/env python

from time import sleep

import docker
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def simple_topology():
    docker_client = docker.from_env()
    ip = None

    for c in docker_client.containers.list():
        for network in c.attrs['NetworkSettings']['Networks'].values():
            if 'ryu' in network['Aliases']:
                ip = network['IPAddress']
                break
        if ip:
            break

    if not ip:
        raise Exception('Failed to get controller IP')

    net = Mininet(controller=RemoteController, autoSetMacs=True)

    info('*** Adding controller\n')
    net.addController('ryu', ip=ip, port=6653)

    info('*** Adding hosts\n')
    h2 = net.addHost('h2', ip='10.0.0.12')
    h3 = net.addHost('h3', ip='10.0.0.13')
    h4 = net.addHost('h4', ip='10.0.0.14')

    info('*** Adding switch\n')
    s1 = net.addSwitch('s1', switch='ovsk', protocols='OpenFlow13')

    info('*** Creating links\n')
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)

    info('*** Starting network\n')
    net.start()

    while True:
        info('*** Pinging all ***\n')
        net.pingAll()
        sleep(30)


if __name__ == '__main__':
    setLogLevel( 'info' )
    simple_topology()
