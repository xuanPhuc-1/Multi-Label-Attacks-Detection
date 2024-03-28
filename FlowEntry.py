import re

class FlowEntry:
# cookie=0x0, duration=5.045s, table=0, n_packets=1, n_bytes=42, idle_timeout=10, hard_timeout=30, priority=65535,arp,in_port="s1-eth3",vlan_tci=0x0000,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:01,arp_spa=10.0.0.3,arp_tpa=10.0.0.1,arp_op=2 actions=output:"s1-eth1"
# cookie=0x0, duration=5.045s, table=0, n_packets=5, n_bytes=490, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s1-eth1",vlan_tci=0x0000,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:03,nw_src=10.0.0.1,nw_dst=10.0.0.3,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"s1-eth3"
# cookie=0x0, duration=5.044s, table=0, n_packets=5, n_bytes=490, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s1-eth3",vlan_tci=0x0000,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:01,nw_src=10.0.0.3,nw_dst=10.0.0.1,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"s1-eth1"
    def __init__(self, entryStr: str):
        self.cookie = FlowEntry.tryParse("cookie=(.*?),", entryStr)
        self.duration = FlowEntry.tryParseFloat("duration=(.*?)s,", entryStr)
        self.table = FlowEntry.tryParseInt("table=(.*?),", entryStr)
        self.n_packets = FlowEntry.tryParseInt("n_packets=(.*?),", entryStr)
        self.n_bytes = FlowEntry.tryParseInt("n_bytes=(.*?),", entryStr)
        self.idle_timeout = FlowEntry.tryParseInt("idle_timeout=(.*?),", entryStr)
        self.hard_timeout = FlowEntry.tryParseInt("hard_timeout=(.*?),", entryStr)
        self.priority = FlowEntry.tryParseInt("priority=(.*?),", entryStr)
        self.arp = FlowEntry.tryParseBool("arp", entryStr)
        self.in_port = FlowEntry.tryParse("in_port=\"(.*?)\"", entryStr)
        self.vlan_tci = FlowEntry.tryParse("vlan_tci=(.*?),", entryStr)
        self.dl_src = FlowEntry.tryParse("dl_src=(.*?),", entryStr)
        self.dl_dst = FlowEntry.tryParse("dl_dst=(.*?),", entryStr)
        self.arp_spa = FlowEntry.tryParse("arp_spa=(.*?),", entryStr)
        self.arp_tpa = FlowEntry.tryParse("arp_tpa=(.*?),", entryStr)
        self.arp_op = FlowEntry.tryParseInt("arp_op=(.*?)\s", entryStr)
        self.icmp = FlowEntry.tryParseBool("icmp", entryStr)
        self.nw_src = FlowEntry.tryParse("nw_src=(.*?),", entryStr)
        self.nw_dst = FlowEntry.tryParse("nw_dst=(.*?),", entryStr)
        self.nw_tos = FlowEntry.tryParse("nw_tos=(.*?),", entryStr)
        self.icmp_type = FlowEntry.tryParseInt("icmp_type=(.*?),", entryStr)
        self.icmp_code = FlowEntry.tryParseInt("icmp_code=(.*?)\s", entryStr)
        self.actions = FlowEntry.tryParse("actions=(.*?)$", entryStr)

    def __str__(self):
        # return f"cookie={self.cookie}, duration={self.duration}, table={self.table}, n_packets={self.n_packets}, n_bytes={self.n_bytes}, idle_timeout={self.idle_timeout}, hard_timeout={self.hard_timeout}, priority={self.priority}, arp={self.arp}, in_port={self.in_port}, vlan_tci={self.vlan_tci}, dl_src={self.dl_src}, dl_dst={self.dl_dst}, arp_spa={self.arp_spa}, arp_tpa={self.arp_tpa}, arp_op={self.arp_op}, icmp={self.icmp}, nw_src={self.nw_src}, nw_dst={self.nw_dst}, nw_tos={self.nw_tos}, icmp_type={self.icmp_type}, icmp_code={self.icmp_code}, actions={self.actions}"
        if(self.arp):
            return f"duration={self.duration}, n_packets={self.n_packets}, n_bytes={self.n_bytes}, arp={self.arp}, dl_src={self.dl_src}, dl_dst={self.dl_dst}, arp_spa={self.arp_spa}, arp_tpa={self.arp_tpa}, arp_op={self.arp_op}, actions={self.actions}"
        elif(self.icmp):
            return f"duration={self.duration}, n_packets={self.n_packets}, n_bytes={self.n_bytes}, icmp={self.icmp}, dl_src={self.dl_src}, dl_dst={self.dl_dst}, nw_src={self.nw_src}, nw_dst={self.nw_dst}, nw_tos={self.nw_tos}, icmp_type={self.icmp_type}, icmp_code={self.icmp_code}, actions={self.actions}"
    def __repr__(self):
        return self.__str__()
    
    def tryParse(patternStr : str, text: str) -> str:
        pattern = re.compile(patternStr)
        match = pattern.search(text)
        if match:
            return match.group(1)
        else:
            return None
    def tryParseInt(patternStr : str, text: str) -> int:
        pattern = re.compile(patternStr)
        match = pattern.search(text)
        if match:
            return int(match.group(1))
        else:
            return None
    def tryParseFloat(patternStr : str, text: str) -> float:
        pattern = re.compile(patternStr)
        match = pattern.search(text)
        if match:
            return float(match.group(1))
        else:
            return None
    def tryParseBool(patternStr : str, text: str) -> bool:
        pattern = re.compile(patternStr)
        match = pattern.search(text)
        if match:
            return True
        else:
            return False