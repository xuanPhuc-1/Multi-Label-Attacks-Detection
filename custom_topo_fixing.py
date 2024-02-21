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

number_of_switches = 5
number_of_hosts = 16


# Dictionary chứa thông tin về các hosts và command tương ứng
host_commands = {
    f'h{i}': f'python3.8 traffic.py -s {i} -e 16' for i in range(1, 17)
}


config_vlan = 'ovs-vsctl add-port s1 s1-vlan1 tag=1'
host_ips = []
# List chứa các quy trình
processes = []
hosts = []
switches = []


def myNetwork():
    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/8')

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='127.0.0.1',
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    for i in range(1, 5):
        switches.append(net.addSwitch(f's{i}', cls=OVSKernelSwitch))

    for switch in switches:
        info(f"Adding {switch} to network\n")

    info('*** Add hosts\n')
    for i in range(1, 17):
        host_ips.append(f'10.0.0.{i}')

        # Thêm các host vào mạng bằng list comprehension
        hosts.append(net.addHost(f'h{i}', cls=Host,
                     ip=f'10.0.0.{i}', defaultRoute=None))
        # for host in hosts:
        #     info(f"Adding {host} to network\n")
        if (i >= 1 and i <= 4):
            hostToSwitch(net, switches[1], hosts[i - 1])
        elif (i >= 5 and i <= 8):
            hostToSwitch(net, switches[2], hosts[i - 1])
        elif (i >= 9 and i <= 12):
            hostToSwitch(net, switches[3], hosts[i - 1])
        elif (i >= 13 and i <= 16):
            hostToSwitch(net, switches[4], hosts[i - 1])

    info('*** Add links\n')
    # connect switch 1 to other switches in switch array
    for i in range(1, 5):
        switchToSwitch(net, switches[0], switches[i])

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    for switch in switches:
        net.get(str(switch)).start([c0])

    info('*** Post configure switches and hosts\n')
    for host, command in host_commands.items():
        p = Process(target=net.get(host).cmd, args=(command,))
        p.start()
        info(f"Starting process for {host} \n")
        processes.append(p)
    CLI(net)


def hostToSwitch(net, switch, host):
    net.addLink(switch, host)


def switchToSwitch(net, switch1, switch2):
    net.addLink(switch1, switch2)


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
    # kill all the processes if the CLI is exited
    for p in processes:
        p.terminate()
