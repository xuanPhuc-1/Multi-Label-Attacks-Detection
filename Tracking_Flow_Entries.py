import subprocess
import time
import os
import threading
from colorama import Fore
import csv

from FlowEntry import FlowEntry

banned_address = ""
br = "br0"
br_real = "tcp:10.9.0.254:6633"


def ParseEntries(input_str: str) -> list:
    entries = []
    for entry in input_str.split("\n"):
        if "actions" in entry:
            entries.append(FlowEntry(entry))
    return entries


def main():
    timeInterval = 1
    MacToIpDict = {}
    bridges = (
        subprocess.check_output(
            ["/usr/bin/sudo", "ovs-vsctl", "list-br"], stderr=subprocess.STDOUT
        )
        .decode("utf-8")
        .split("\n")
    )

    while True:
        # get Data Link Source (dl_src) address from MitM_Ban_List.csv
        with open("MitM_Ban_List.csv", mode="r") as file:
            csvFile = csv.reader(file)
            # get the first row
            banned_address = [rows[0] for rows in csvFile]
            # get value from list
            banned_address = banned_address[0]
        for bridge in bridges:
            try:
                output = subprocess.check_output(
                    ["/usr/bin/sudo", "ovs-ofctl", "dump-flows", br],
                    stderr=subprocess.STDOUT,
                )
                outputMessage = output.decode("utf-8")
            except subprocess.CalledProcessError as e:
                errorMessage = e.output.decode("utf-8")
                if errorMessage.strip():
                    print(errorMessage)
                time.sleep(1)
                continue
            entries = ParseEntries(outputMessage)

            for flowEntry in entries:
                try:
                    # in ra toàn bộ các flow có dl_src là banned_address
                    if (
                        flowEntry.dl_src == banned_address
                        and flowEntry.actions != "drop"
                    ):
                        if flowEntry.icmp_type == None:
                            blockARPpackets(flowEntry)
                        # add flow với câu lệnh sudo ovs-ofctl add-flow với action drop đối với các flow có dl_src là banned_address
                        # sudo ovs-ofctl add-flow s2 "table=0, priority=100, in_port=s2-eth1, dl_src=0a:33:f8:53:c5:21, dl_dst=8a:8d:75:e8:31:c8, nw_src=10.0.0.1, nw_dst=10.0.0.2, icmp, icmp_type=8, icmp_code=0, actions=drop"
                        else:
                            os.system(
                                f'sudo ovs-ofctl add-flow {br} "table={flowEntry.table}, priority={flowEntry.priority}, in_port={flowEntry.in_port}, dl_src={flowEntry.dl_src}, dl_dst={flowEntry.dl_dst}, nw_src={flowEntry.nw_src}, nw_dst={flowEntry.nw_dst}, icmp, icmp_type={flowEntry.icmp_type}, icmp_code={flowEntry.icmp_code}, actions=drop"'
                            )
                            # in ra toàn bộ các flow có dl_src là banned_address
                            print("Banned flow icmp: ", flowEntry)
                except ValueError as e:
                    print(str(e))
                except:
                    pass
        time.sleep(timeInterval)


def blockARPpackets(flowEntry):
    # duration=1.337, n_packets=1, n_bytes=42, arp=True, dl_src=26:1a:f9:fc:c6:66, dl_dst=c2:77:59:f9:85:04, arp_spa=10.10.0.2, arp_tpa=10.10.0.3, arp_op=2, actions=output:3
    print("Banned ARP packets: ", flowEntry)
    os.system(
        f'sudo ovs-ofctl add-flow br0 "in_port={flowEntry.in_port}, actions=drop"'
    )
    os.system(
        f'sudo ovs-ofctl add-flow {br} "table={flowEntry.table}, in_port={flowEntry.in_port}, dl_src={flowEntry.dl_src}, dl_dst={flowEntry.dl_dst}, arp_spa={flowEntry.arp_spa}, arp_tpa={flowEntry.arp_tpa}, arp_op={flowEntry.arp_op}, actions=drop"'
    )


def repeatClearScreen(interval: int):
    os.system("clear")
    threading.Timer(interval, repeatClearScreen, args=[interval]).start()


if __name__ == "__main__":
    repeatClearScreen(3)
    main()
    # end the program if user press Ctrl + C
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print(Fore.RED + "Program is terminated")
        exit(0)
