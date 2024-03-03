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


# Dictionary chứa thông tin về các hosts và command tương ứng
# host_commands = {
#     f'h{i}': f'python3.8 traffic.py -s {i} -e 64' for i in range(1, 65)
# }


config_vlan = 'ovs-vsctl add-port s1 s1-vlan1 tag=1'
host_ips = []
# List chứa các quy trình
processes = []
hosts = []
switches = []


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
    for i in range(1, 65):

        # for host in hosts:
        #     info(f"Adding {host} to network\n")
        if (i >= 1 and i <= 8):
            host_ips.append(f'10.10.0.{i}')
            hosts.append(net.addHost(f'h{i}', cls=Host,
                                     ip=f'10.10.0.{i}/24'))
            # h{i} run cmd "route add default gw 10.9.0.254"
            net.get(f'h{i}').cmd('route add default gw 10.10.0.254')
            hostToSwitch(net, s1, hosts[i-1])
        elif (i >= 9 and i <= 16):
            host_ips.append(f'10.20.0.{i}')
            hosts.append(net.addHost(f'h{i}', cls=Host,
                                     ip=f'10.20.0.{i}/24'))
            net.get(f'h{i}').cmd('route add default gw 10.20.0.254')
            hostToSwitch(net, s1, hosts[i-1])
        elif (i >= 17 and i <= 24):
            host_ips.append(f'10.30.0.{i}')
            hosts.append(net.addHost(f'h{i}', cls=Host,
                                     ip=f'10.30.0.{i}/24'))
            hostToSwitch(net, s1, hosts[i-1])
        elif (i >= 25 and i <= 33):
            host_ips.append(f'10.40.0.{i}')
            hosts.append(net.addHost(f'h{i}', cls=Host,
                                     ip=f'10.40.0.{i}/24'))
            hostToSwitch(net, s1, hosts[i-1])
        elif (i >= 33 and i <= 40):
            host_ips.append(f'10.50.0.{i}')
            hosts.append(net.addHost(f'h{i}', cls=Host,
                                     ip=f'10.50.0.{i}/24'))
            net.get(f'h{i}').cmd('route add default gw 10.40.0.254')
            hostToSwitch(net, s1, hosts[i-1])
        elif (i >= 41 and i <= 48):
            host_ips.append(f'10.60.0.{i}')
            hosts.append(net.addHost(f'h{i}', cls=Host,
                                     ip=f'10.60.0.{i}/24'))
            net.get(f'h{i}').cmd('route add default gw 10.50.0.254')
            hostToSwitch(net, s1, hosts[i-1])

    info('*** Add links\n')
    # connect switch 1 to other switches in switch array

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')

    net.get('s1').start([c0])
    info('*** Post configure switches and hosts\n')
    # for host, command in host_commands.items():
    #     p = Process(target=net.get(host).cmd, args=(command,))
    #     p.start()
    #     info(f"Starting process for {host} \n")
    #     processes.append(p)
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
