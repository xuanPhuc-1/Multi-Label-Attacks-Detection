#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from multiprocessing import Process

number_of_switches = 9
number_of_hosts = 64

host_ips = []
# List chứa các quy trình
processes = []
hosts = []
switches = []


def hostToSwitch(net, switch, host):
    net.addLink(switch, host)


def switchToSwitch(net, switch1, switch2):
    net.addLink(switch1, switch2)


def setup_gateway(net, host_name, gateway):
    print(f"Setting up gateway for {host_name} with gateway {gateway}")
    Process(target=net.get(host_name).cmd, args=(
        f'route add default gw {gateway}',)).start()


def start_traffic(net, host_name, source, end):
    command = f'python3.8 traffic.py -s {source} -e {end}'
    Process(target=net.get(host_name).cmd, args=(command,)).start()


def myNetwork():
    net = Mininet(topo=None,
                  build=False)

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='127.0.0.1',
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info('*** Add hosts\n')
    for i in range(1, 49):
        if i >= 1 and i <= 8:
            ip_address = f'10.10.0.{i}'
            gateway = '10.10.0.254'
        elif i >= 9 and i <= 16:
            ip_address = f'10.20.0.{i}'
            gateway = '10.20.0.254'
        elif i >= 17 and i <= 24:
            ip_address = f'10.30.0.{i}'
            gateway = '10.30.0.254'
        elif i >= 25 and i <= 32:
            ip_address = f'10.40.0.{i}'
            gateway = '10.40.0.254'
        elif i >= 33 and i <= 40:
            ip_address = f'10.50.0.{i}'
            gateway = '10.50.0.254'
        elif i >= 41 and i <= 48:
            ip_address = f'10.60.0.{i}'
            gateway = '10.60.0.254'

        host_ips.append(ip_address)
        host = net.addHost(f'h{i}', cls=Host, ip=f'{ip_address}/24')
        # hosts.append(host)

        # Liên kết máy chủ với switch
        hostToSwitch(net, s1, host)

    info('*** Add links\n')
    # connect switch 1 to other switches in switch array

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')

    net.get('s1').start([c0])
    # print(hosts)

    info('*** Post configure switches and hosts\n')
    p_s1 = Process(target=net.get('s1').cmd, args=(
        'source del_port.sh',))
    # p1 = Process(target=net.get('h1').cmd, args=('ettercap -T -i h1-eth0 -M ARP /10.0.0.3// /10.0.0.7//',))
    p_s1.start()
    info('*** Configuring gateway for hosts\n')
    for i in range(1, 49):
        if i >= 1 and i <= 8:
            gateway = '10.10.0.254'
        elif i >= 9 and i <= 16:
            gateway = '10.20.0.254'
        elif i >= 17 and i <= 24:
            gateway = '10.30.0.254'
        elif i >= 25 and i <= 32:
            gateway = '10.40.0.254'
        elif i >= 33 and i <= 40:
            gateway = '10.50.0.254'
        elif i >= 41 and i <= 48:
            gateway = '10.60.0.254'

        setup_gateway(net, f'h{i}', gateway)

    info('*** Running Traffic\n')
    for i in range(1, 49):
        start_traffic(net, f'h{i}', i, 48)
    info('*** Done\n')
    CLI(net)


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
    # kill all the processes if the CLI is exited
    for p in processes:
        p.terminate()
