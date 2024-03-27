import numpy as np
import csv
import pandas as pd
import time
import os
import psutil

HOME = '/home/xp'
time_interval = 1


# Standard deviation of packets (SDFP)
# i.e., number of packets in the T period.
# SDFP = sqrt((1/n) * sum((packets_i - mean_packets,2) ** 2))
# packets_i = number of packets of flow ith in T period
# mean_packets: mean of total packets of all flows in T period
packets_csv = np.genfromtxt('data/packets.csv', delimiter=",")
dt_packets = packets_csv[:, 0]
sdfp = np.std(dt_packets)

# Standard deviation of bytes (SDFB)
# i.e., number of bytes in the T period
# SDFB = sqrt((1/n) * sum((bytes_i - mean_bytes,2) ** 2))
# bytes_i: number of total bytes of flow ith in T period
# mean_bytes: mean of total bytes of all flows in T period
bytes_csv = np.genfromtxt('data/bytes.csv', delimiter=",")
dt_bytes = bytes_csv[:, 0]
sdfb = np.std(dt_bytes)

# Number of source IPs
# Speed of source IP (SSIP), number of source IPs per unit of time
# SSIP = Number of different IP sources / T period
with open('data/ipsrc.csv', newline='') as f:
    reader = csv.reader(f)
    ipsrc_csv = list(reader)
n_ip = len(np.unique(ipsrc_csv))      # Get number of different source IPs
# print(n_ip)
# Get number of IPs for every second by multiple interval - 4s
ssip = n_ip // time_interval
f.close()


# print(entropy.value)


# Number of Flow entries
# Speed of Flow entries (SFE), number of flow entries to the switch per unit of time
# SFE = Number of flow entries / T period
sfe = n_ip // time_interval

# Number of interactive flow entries
# Ratio of Pair-Flow Entries (RFIP)
# RFIP = Interactive flow entries / total number of flows in T period
fileone = None
filetwo = None

with open('data/ipsrc.csv', 'r') as t1, open('data/ipdst.csv', 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

# Check if the src_ip exists in the dst_ip,
# which indicates that source IP has two-way interaction with the destination IP.
# If not, append that one-way interaction IP into interactive flow file (intflow.csv)
with open('data/intflow.csv', 'w') as f:
    for line in fileone:
        if line not in filetwo:
            f.write(line)

# The cpu_percent increases dramatically when DDOS attack happens
# Get CPU utilization
cpu_percent = psutil.cpu_percent(interval=0.1)

# Count number of
with open('data/intflow.csv') as f:
    reader = csv.reader(f, delimiter=",")
    dt = list(reader)
    row_count_nonint = len(dt)
rfip = abs(float(n_ip - row_count_nonint) / n_ip)


with open('ARP_data/ARP_Reply_flowentries.csv', newline='') as f:
    reader = csv.reader(f)
    ARP_Reply = list(reader)
# count the number of ARP_Reply
ARP_Reply = len(ARP_Reply)
with open('ARP_data/ARP_Request_flowentries.csv', newline='') as f1:
    reader = csv.reader(f1)
    ARP_Request = list(reader)
# #check if the path /home/xuanphuc/MITM-Detection/ARP_Broadcast/arp_broadcast.csv exists do the following or not the a

path = HOME + '/Multi-Label-Attacks-Detection/ARP_Broadcast/arp_broadcast.csv'
with open(path, newline='') as f2:
    reader = csv.reader(f2)
    # format of arp_broadcast.csv: source Mac, time stamp
    arp_broadcast = list(reader)


arp_broadcast = len(arp_broadcast)
abps = arp_broadcast / time_interval

# count the number of ARP_Request
ARP_Request = len(ARP_Request)
ARP = ARP_Reply + ARP_Request

f.close()
f1.close()
f2.close()

aps = ARP / time_interval
subARP = ARP_Reply - ARP_Request

with open('mismatch.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader = list(reader)

if int(reader[-1][-1]) > 0:
    if subARP >= 1:
        miss_match = 1
    else:
        miss_match = 0
else:
    miss_match = 0
# time stamp with minute:second format
time_stamp = time.strftime("%H:%M:%S", time.localtime())
# APS: ARP per second, ABPS: ARP broadcast per second, SUBARP: ARP reply - ARP request, MISS_MAC: miss match

ddos = 1
slow_rate = 1
mitm = 0
tag_ddos = ''
tag_slow_rate = ''
tag_mitm = ''

if ddos != 0:
    tag_ddos = 'DDOS '
if slow_rate != 0:
    tag_slow_rate = 'Slow Rate '
if mitm != 0:
    tag_mitm = 'MITM '
if ddos == 0 and slow_rate == 0 and mitm == 0:
    tag = 'Normal'
else:
    tag = tag_ddos + tag_slow_rate + tag_mitm

headers = ["SSIP", "SDFP", "SDFB", "SFE", "RFIP",
           "CPU", "APS", "ABPS", "SUBARP", "MISS_MAC", "DDOS", "SLOW-RATE", "MITM", "TAGS"]

# headers = ["SSIP", "SDFP", "SDFB", "SFE", "RFIP",
#            "CPU", "APS", "ABPS", "SUBARP", "MISS_MAC", "TIME"]

features = [ssip, sdfp, sdfb, sfe, rfip, cpu_percent,
            aps, abps, subARP, miss_match, ddos, slow_rate, mitm, tag]
# features = [ssip, sdfp, sdfb, sfe, rfip, cpu_percent,
#             aps, abps, subARP, miss_match, time_stamp]

file_exists = os.path.isfile('features-file.csv')
with open('features-file.csv', 'a') as f:
    cursor = csv.writer(f, delimiter=",")
    # cursor.writerow(headers)
    if not file_exists:
        cursor.writerow(headers)
    cursor.writerow(features)

with open('realtime.csv', 'w') as f:
    cursor = csv.writer(f, delimiter=",")
    cursor.writerow(headers)
    cursor.writerow(features)

    f.close()
