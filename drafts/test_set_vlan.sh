#!/bin/bash
ovs-vsctl add-br br0

ovs-vsctl del-port s1-eth1
ovs-vsctl del-port s1-eth2
ovs-vsctl del-port s1-eth3
ovs-vsctl del-port s1-eth4
ovs-vsctl del-port s1-eth5
ovs-vsctl del-port s1-eth6

sudo ovs-vsctl add-port br0 s1-eth1 tag=10
sudo ovs-vsctl add-port br0 s1-eth2 tag=10
sudo ovs-vsctl add-port br0 s1-eth3 tag=20
sudo ovs-vsctl add-port br0 s1-eth4 tag=20
sudo ovs-vsctl add-port br0 s1-eth5 tag=30
sudo ovs-vsctl add-port br0 s1-eth6 tag=30


ovs-vsctl add-port br0 vlan10 tag=10 -- set interface vlan10 type=internal
ovs-vsctl add-port br0 vlan20 tag=20 -- set interface vlan20 type=internal
ovs-vsctl add-port br0 vlan30 tag=30 -- set interface vlan30 type=internal

ovs-vsctl set-controller br0 tcp:127.0.0.1:6633 


# Xóa các cổng và thêm lại chúng


ifconfig vlan10 192.168.10.254 netmask 255.255.255.0
ifconfig vlan20 192.168.20.254 netmask 255.255.255.0
ifconfig vlan30 192.168.30.254 netmask 255.255.255.0

# Đặt controller cho cầu


sysctl -w net.ipv4.ip_forward=1
# sysctl -w net.ipv6.conf.all.forwarding=1