from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def myNetwork():

    net = Mininet(topo=None, build=False)

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='127.0.0.1',
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info('*** Add hosts\n')

    h1 = net.addHost('h1', cls=Host, ip='192.168.10.1/24')
    h2 = net.addHost('h2', cls=Host, ip='192.168.10.2/24')
    h3 = net.addHost('h3', cls=Host, ip='192.168.20.3/24')
    h4 = net.addHost('h4', cls=Host, ip='192.168.20.4/24')
    h5 = net.addHost('h5', cls=Host, ip='192.168.30.5/24')
    h6 = net.addHost('h6', cls=Host, ip='192.168.30.6/24')
    # h7 = net.addHost('h7', cls=Host, ip='10.10.0.7/24')
    # h8 = net.addHost('h8', cls=Host, ip='10.10.0.8/24')

    info('*** Add links\n')
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s1, h4)
    net.addLink(s1, h5)
    net.addLink(s1, h6)
    # net.addLink(s1, h7)
    # net.addLink(s1, h8)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')

    net.get('s1').start([c0])

    # Add VLANs
    # s1.cmd('ovs-vsctl add-br s1_vlan1')
    # s1.cmd('ovs-vsctl add-br s1_vlan2')
    # s1.cmd('ovs-vsctl del-port s1-eth1')
    # s1.cmd('ovs-vsctl del-port s1-eth2')
    # s1.cmd('ovs-vsctl del-port s1-eth3')
    # s1.cmd('ovs-vsctl del-port s1-eth4')
    # s1.cmd('ovs-vsctl add-port s1_vlan1 s1-eth1')
    # s1.cmd('ovs-vsctl add-port s1_vlan1 s1-eth2')
    # s1.cmd('ovs-vsctl add-port s1_vlan2 s1-eth3')
    # s1.cmd('ovs-vsctl add-port s1_vlan2 s1-eth4')

    # # # Assign ports to VLANs
    # s1.cmd('ovs-vsctl set port s1_vlan1 tag=9')
    # s1.cmd('ovs-vsctl set port s1_vlan2 tag=10')
    # s1.cmd('ovs-vsctl set port s1-eth1 tag=9')
    # s1.cmd('ovs-vsctl set port s1-eth2 tag=9')
    # s1.cmd('ovs-vsctl set port s1_eth3 tag=10')
    # s1.cmd('ovs-vsctl set port s1-eth4 tag=10')

    # # # Set IP for VLAN interfaces
    # s1.cmd('ifconfig s1_vlan1 192.168.1.1 netmask 255.255.255.0')
    # s1.cmd('ifconfig s1_vlan2 192.168.2.1 netmask 255.255.255.0')

    # # # Set IP for hosts
    # h1.cmd('ip addr add 192.168.1.2/24 dev h1-eth0')
    # h2.cmd('ip addr add 192.168.1.3/24 dev h2-eth0')
    # h3.cmd('ip addr add 192.168.2.2/24 dev h3-eth0')
    # h4.cmd('ip addr add 192.168.2.3/24 dev h4-eth0')

    # # # Enable forwarding on the switch
    # s1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Post configure switches and hosts\n')
    CLI(net)


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
