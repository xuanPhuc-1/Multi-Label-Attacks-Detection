#!/bin/bash
for i in {1..10000}
do
    echo "Collecting flow on switch br0 turn $i"
    # extract essential data from raw data
    # sudo ovs-ofctl -O OpenFlow13 dump-flows s"$j" > data/raw.txt
    sudo ovs-ofctl -O OpenFlow13 dump-flows br0 > data/raw.txt
    # sudo ovs-ofctl dump-flows tcp:10.9.0.254:6633 > data/raw.txt #uncomment to run in real environment
    grep "nw_src" data/raw.txt > data/flowentries.csv
    grep "arp_op=1" data/raw.txt > ARP_data/ARP_Request_flowentries.csv
    grep "arp_op=2" data/raw.txt > ARP_data/ARP_Reply_flowentries.csv


    packets=$(awk -F "," '{split($4,a,"="); print a[2]","}' data/flowentries.csv)
    bytes=$(awk -F "," '{split($5,b,"="); print b[2]","}' data/flowentries.csv)
    # ipsrc=$(awk -F "," '{split($15,c,"="); print c[2]","}' data/flowentries.csv)    #14 cho l3
    # ipdst=$(awk -F "," '{split($16,d,"="); print d[2]","}' data/flowentries.csv)    #15 cho l3

    ipsrc=$(awk -F "," '{split($14,c,"="); print c[2]","}' data/flowentries.csv)    
    ipdst=$(awk -F "," '{split($15,d,"="); print d[2]","}' data/flowentries.csv)    
    ethsrc=$(awk -F "," '{split($12,e,"="); print e[2]","}' data/flowentries.csv)   
    ethdst=$(awk -F "," '{split($13,f,"="); print f[2]","}' data/flowentries.csv)   

    eth_src_reply=$(awk -F "," '{split($12,e,"="); print e[2]","}' ARP_data/ARP_Reply_flowentries.csv)   
    ip_dst_reply=$(awk -F "," '{split($15,d,"="); print d[2]","}' ARP_data/ARP_Reply_flowentries.csv)    


    if test -z "$packets" || test -z "$bytes" || test -z "$ipsrc" || test -z "$ipdst" 
    then
        state=0
    else
        echo "$packets" > data/packets.csv
        echo "$bytes" > data/bytes.csv

        echo "$ipsrc" > data/ipsrc.csv
        echo "$ipdst" > data/ipdst.csv
        echo "$ethsrc" > data/ethsrc.csv
        echo "$ethdst" > data/ethdst.csv
        echo "$eth_src_reply" > ARP_data/eth_src_reply.csv
        echo "$ip_dst_reply" > ARP_data/ip_dst_reply.csv
    fi
    python3.8 computeTuples.py
    truncate -s 0 ARP_Broadcast/arp_broadcast.csv
    truncate -s 0 f1.csv
    # python3.11 inspector.py
    # python3.11 inspector.py
    sleep 1

done


#  cookie=0x0, duration=10.903s, table=classifier, n_packets=1, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="6",dl_vlan=58,dl_vlan_pcp=0,dl_src=38:60:77:89:e6:72,dl_dst=38:60:77:89:f1:49,nw_src=10.58.0.6,nw_dst=10.58.0.5,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"5"
#  cookie=0x0, duration=14.599s, table=classifier, n_packets=2, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="4",dl_vlan=14,dl_vlan_pcp=0,dl_src=38:60:77:8a:49:b2,dl_dst=38:60:77:89:f5:e4,nw_src=10.14.0.4,nw_dst=10.14.0.3,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"3"
#  cookie=0x0, duration=9.009s, table=classifier, n_packets=0, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="6",dl_vlan=58,dl_vlan_pcp=0,dl_src=38:60:77:89:e6:72,dl_dst=38:60:77:89:f1:49,nw_src=10.58.0.6,nw_dst=10.58.0.5,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"5"
#  cookie=0x0, duration=11.172s, table=classifier, n_packets=2, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="3",dl_vlan=14,dl_vlan_pcp=0,dl_src=38:60:77:89:f5:e4,dl_dst=38:60:77:8a:49:b2,nw_src=10.14.0.3,nw_dst=10.14.0.4,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"4"
#  cookie=0x0, duration=14.873s, table=classifier, n_packets=2, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="1",dl_vlan=14,dl_vlan_pcp=0,dl_src=38:60:77:89:f1:47,dl_dst=38:60:77:89:f5:3e,nw_src=10.14.0.1,nw_dst=10.14.0.2,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"2"
#  cookie=0x0, duration=5.611s, table=classifier, n_packets=0, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="2",dl_vlan=14,dl_vlan_pcp=0,dl_src=38:60:77:89:f5:3e,dl_dst=38:60:77:89:f5:e4,nw_src=10.14.0.2,nw_dst=10.14.0.3,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"3"
#  cookie=0x0, duration=8.840s, table=classifier, n_packets=0, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="2",dl_vlan=14,dl_vlan_pcp=0,dl_src=38:60:77:89:f5:3e,dl_dst=38:60:77:89:f1:47,nw_src=10.14.0.2,nw_dst=10.14.0.1,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"1"
#  cookie=0x0, duration=5.169s, table=classifier, n_packets=0, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="4",dl_vlan=14,dl_vlan_pcp=0,dl_src=38:60:77:8a:49:b2,dl_dst=38:60:77:89:f5:e4,nw_src=10.14.0.4,nw_dst=10.14.0.3,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"3"
#  cookie=0x0, duration=13.927s, table=classifier, n_packets=1, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="5",dl_vlan=58,dl_vlan_pcp=0,dl_src=38:60:77:89:f1:49,dl_dst=38:60:77:89:e6:72,nw_src=10.58.0.5,nw_dst=10.58.0.6,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"6"
#  cookie=0x0, duration=4.890s, table=classifier, n_packets=0, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="5",dl_vlan=58,dl_vlan_pcp=0,dl_src=38:60:77:89:f1:49,dl_dst=38:60:77:89:e6:72,nw_src=10.58.0.5,nw_dst=10.58.0.6,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"6"
#  cookie=0x0, duration=8.620s, table=classifier, n_packets=0, n_bytes=0, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="3",dl_vlan=14,dl_vlan_pcp=0,dl_src=38:60:77:89:f5:e4,dl_dst=38:60:77:8a:49:b2,nw_src=10.14.0.3,nw_dst=10.14.0.4,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"4"
