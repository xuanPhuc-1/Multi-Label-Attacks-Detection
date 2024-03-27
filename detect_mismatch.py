import subprocess
import time
import os
import threading
from colorama import Fore
import csv

from FlowEntry import FlowEntry


def ParseEntries(input_str: str) -> list:
    entries = []
    for entry in input_str.split('\n'):
        if ('actions' in entry):
            entries.append(FlowEntry(entry))
    return entries


def main():
    timeInterval = 1
    MacToIpDict = {}
    bridges = subprocess.check_output(
        ['/usr/bin/sudo', 'ovs-vsctl', 'list-br'], stderr=subprocess.STDOUT).decode('utf-8').split('\n')

    # check if file is not exist
    if not os.path.isfile('mismatch.csv'):
        file = open('mismatch.csv', 'w')
        file.close()
    else:
        # clear file
        open('mismatch.csv', 'w').close()

    while True:
        suspiciousPackets = 0
        print(MacToIpDict)
        for bridge in bridges:
            try:
                output = subprocess.check_output(
                    ['/usr/bin/sudo', 'ovs-ofctl', 'dump-flows', "tcp:10.9.0.254:6633"], stderr=subprocess.STDOUT)
                outputMessage = output.decode('utf-8')
            except subprocess.CalledProcessError as e:
                errorMessage = e.output.decode('utf-8')
                if errorMessage.strip():
                    print(errorMessage)
                time.sleep(1)
                continue
            entries = ParseEntries(outputMessage)

            for flowEntry in entries:
                try:
                    # check if flowEntry is type FlowEntry
                    if isinstance(flowEntry, FlowEntry):
                        if (flowEntry.arp):
                            # print(flowEntry)
                            if flowEntry.dl_src not in MacToIpDict:
                                MacToIpDict[flowEntry.dl_src] = flowEntry.arp_spa
                                print(
                                    f"Added {flowEntry.dl_src}-> {flowEntry.arp_spa} to MacToIpDict")
                            if flowEntry.arp_op == 2 and flowEntry.dl_src in MacToIpDict and MacToIpDict[flowEntry.dl_src] != flowEntry.arp_spa:
                                print(
                                    f"{Fore.RED}WARNING!{Fore.RESET} {bridge}: {flowEntry.dl_src} is trying to impersonate {flowEntry.arp_spa}!")
                                suspiciousPackets += flowEntry.n_packets
                except ValueError as e:
                    print(str(e))
                except:
                    pass
        if suspiciousPackets > 0:
            print(
                f"{Fore.RED}WARNING!{Fore.RESET} {suspiciousPackets} suspicious packets detected!")
        # write to to csv file
        with open('mismatch.csv', 'w') as f:
            # write binary_prediction to result.csv
            writer = csv.writer(f)
            writer.writerow([suspiciousPackets])
            f.close()
        time.sleep(timeInterval)


def repeatClearScreen(interval: int):
    os.system('clear')
    threading.Timer(interval, repeatClearScreen, args=[interval]).start()


if __name__ == "__main__":
    # repeatClearScreen(10)
    main()
