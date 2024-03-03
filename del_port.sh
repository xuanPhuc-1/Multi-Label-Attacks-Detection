#!/bin/bash
ovs-vsctl add-br br0


# Xóa các cổng và thêm lại chúng
for i in {1..48}; do
    ovs-vsctl del-port s1-eth$i
    ovs-vsctl add-port br0 s1-eth$i

    if [ $i -ge 1 ] && [ $i -le 8 ]; then
        ovs-vsctl set port s1-eth$i tag=10
    elif [ $i -ge 9 ] && [ $i -le 16 ]; then
        ovs-vsctl set port s1-eth$i tag=20
    elif [ $i -ge 17 ] && [ $i -le 24 ]; then
        ovs-vsctl set port s1-eth$i tag=30
    elif [ $i -ge 25 ] && [ $i -le 32 ]; then
        ovs-vsctl set port s1-eth$i tag=40
    elif [ $i -ge 33 ] && [ $i -le 40 ]; then
        ovs-vsctl set port s1-eth$i tag=50
    elif [ $i -ge 41 ] && [ $i -le 48 ]; then
        ovs-vsctl set port s1-eth$i tag=60
    fi
done

# Đặt controller cho cầu
ovs-vsctl set-controller br0 tcp:127.0.0.1:6633 

# Thêm các cổng VLAN với các tag tương ứng
ovs-vsctl add-port br0 vlan10 tag=10 -- set Interface vlan10 type=internal
ifconfig vlan10 10.10.0.254 netmask 255.255.255.0
ovs-vsctl add-port br0 vlan20 tag=20 -- set Interface vlan20 type=internal
ifconfig vlan20 10.20.0.254 netmask 255.255.255.0
ovs-vsctl add-port br0 vlan50 tag=50 -- set Interface vlan50 type=internal
ifconfig vlan50 10.50.0.254 netmask 255.255.255.0
ovs-vsctl add-port br0 vlan60 tag=60 -- set Interface vlan60 type=internal
ifconfig vlan60 10.60.0.254 netmask 255.255.255.0


sysctl -w net.ipv4.ip_forward=1