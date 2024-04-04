sudo ovs-ofctl add-flow s2 "table=0, priority=100, in_port=s2-eth1, dl_src=0a:33:f8:53:c5:21, dl_dst=8a:8d:75:e8:31:c8, nw_src=10.0.0.1, nw_dst=10.0.0.2, icmp, icmp_type=8, icmp_code=0, actions=drop"
