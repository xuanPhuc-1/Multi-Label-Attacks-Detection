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
