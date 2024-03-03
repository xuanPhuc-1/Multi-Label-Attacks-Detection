import argparse
import threading
import time
import random
import socket


def send_ping(host):
    while True:
        # Simulate random ping intervals
        time.sleep(random.randint(1, 30))

        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Send a ping request to the specified host
        try:
            sock.sendto(b"PING", (host, 80))
            print(f"Sent ping to {host}")
        except socket.error as e:
            print(f"Error sending ping to {host}: {e}")

        # Receive a response from the host
        try:
            data, addr = sock.recvfrom(1024)
        except socket.error:
            print(f"No response from {host}")
        else:
            print(f"Received ping response from {addr}: {data}")

        # Close the socket
        sock.close()


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", type=int,
                        default=1, help="Starting host index")
    parser.add_argument("-e", "--end", type=int,
                        default=48, help="Ending host index")
    args = parser.parse_args()

    # Get the list of hosts based on the specified range
    hosts = []
    for i in range(args.start, args.end + 1):
        # j is random integer from 10 to 60 withh step 10 and not equal to 30 and 40
        j = random.choice([10, 20, 50, 60])
        hosts.append(f"10.{j}.0.{i}")

    while True:
        # Create and start threads for each host
        threads = []
        for host in hosts:
            thread = threading.Thread(target=send_ping, args=(host,))
            threads.append(thread)
            thread.start()

        # Sleep for a while before restarting the pinging process
        time.sleep(60)


if __name__ == "__main__":
    main()
