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
    # c1=net.addController(name='c1',
    #                   controller=RemoteController,
    #                   ip='127.0.0.1',
    #                   protocol='tcp',
    #                   port=6634)
    info('*** Add switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)

    info('*** Add hosts\n')
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8/8', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4/8', defaultRoute=None)
    h13 = net.addHost('h13', cls=Host, ip='10.0.0.13/8', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.11/8', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9/8', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5/8', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1/8', defaultRoute=None)
    h14 = net.addHost('h14', cls=Host, ip='10.0.0.14/8', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10/8', defaultRoute=None)
    h15 = net.addHost('h15', cls=Host, ip='10.0.0.15/8', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2/8', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7/8', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3/8', defaultRoute=None)
    h16 = net.addHost('h16', cls=Host, ip='10.0.0.16/8', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6/8', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='10.0.0.12/8', defaultRoute=None)

    info('*** Add links\n')
    net.addLink(s3, h5)
    net.addLink(h6, s3)
    net.addLink(s3, h7)
    net.addLink(h8, s3)
    net.addLink(h9, s4)
    net.addLink(s4, h10)
    net.addLink(h11, s4)
    net.addLink(s4, h12)
    net.addLink(s5, h13)
    net.addLink(s5, h14)
    net.addLink(s5, h15)
    net.addLink(s5, h16)
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s1, s4)
    net.addLink(s1, s5)
    net.addLink(s2, h1)
    net.addLink(h2, s2)
    net.addLink(s2, h3)
    net.addLink(h4, s2)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s1').start([c0])
    net.get('s5').start([c0])

    # net.get('s2').start([c1])
    # net.get('s3').start([c1])
    # net.get('s4').start([c1])
    # net.get('s1').start([c1])
    # net.get('s5').start([c1])
    # let the host run command in the background

    info('*** Post configure switches and hosts\n')
    p1 = Process(target=net.get('h1').cmd, args=(
        'python3.8 traffic.py -s 1 -e 16',))
    # p1 = Process(target=net.get('h1').cmd, args=('ettercap -T -i h1-eth0 -M ARP /10.0.0.3// /10.0.0.7//',))
    p1.start()

    p2 = Process(target=net.get('h2').cmd, args=(
        'python3.8 traffic.py -s 2 -e 16',))
    # p2 = Process(target=net.get('h2').cmd, args=('ettercap -T -i h2-eth0 -M ARP /10.0.0.5// /10.0.0.8//',))
    p2.start()

    p3 = Process(target=net.get('h3').cmd, args=(
        'python3.8 traffic.py -s 3 -e 16',))
    # p3= Process(target=net.get('h3').cmd, args=('ettercap -T -i h3-eth0 -M ARP /10.0.0.1// /10.0.0.8//',))
    p3.start()

    p4 = Process(target=net.get('h4').cmd, args=(
        'python3.8 traffic.py -s 4 -e 16',))
    p4.start()

    p5 = Process(target=net.get('h5').cmd, args=(
        'python3.8 traffic.py -s 5 -e 16',))
    p5.start()

    p6 = Process(target=net.get('h6').cmd, args=(
        'python3.8 traffic.py -s 6 -e 16',))
    p6.start()

    p7 = Process(target=net.get('h7').cmd, args=(
        'python3.8 traffic.py -s 7 -e 16',))
    p7.start()

    p8 = Process(target=net.get('h8').cmd, args=(
        'python3.8 traffic.py -s 8 -e 16',))
    p8.start()

    p9 = Process(target=net.get('h9').cmd, args=(
        'python3.8 traffic.py -s 9 -e 16',))
    p9.start()

    p10 = Process(target=net.get('h10').cmd, args=(
        'python3.8 traffic.py -s 10 -e 16',))
    p10.start()

    p11 = Process(target=net.get('h11').cmd, args=(
        'python3.8 traffic.py -s 11 -e 16',))
    p11.start()

    p12 = Process(target=net.get('h12').cmd, args=(
        'python3.8 traffic.py -s 12 -e 16',))
    p12.start()

    p13 = Process(target=net.get('h13').cmd, args=(
        'python3.8 traffic.py -s 13 -e 16',))
    p13.start()

    p14 = Process(target=net.get('h14').cmd, args=(
        'python3.8 traffic.py -s 14 -e 16',))
    p14.start()

    p15 = Process(target=net.get('h15').cmd, args=(
        'python3.8 traffic.py -s 15 -e 16',))
    p15.start()

    p16 = Process(target=net.get('h16').cmd, args=(
        'python3.8 traffic.py -s 16 -e 16',))
    p16.start()

    CLI(net)


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
