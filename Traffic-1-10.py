import argparse
import psutil
import time
import socket
from prettytable import PrettyTable

# Create ArgumentParser object
parser = argparse.ArgumentParser(description='Run up.py with specified protocol and multiplier.')

# Add arguments
parser.add_argument('-p', '--protocol', type=str, default='udp', choices=['tcp', 'udp'],
                    help='Protocol type (TCP or UDP)')
parser.add_argument('-z', '--multiplier', type=int, default=10,
                    help='Multiplier value for packet size')
parser.add_argument('-i', '--interface', type=str, default=None,
                    help='Network interface to use')

# Parse arguments from command line
args = parser.parse_args()

# Define the speed format string
speed_format = "Download: {:.2f} Mbps, Upload: {:.2f} Mbps, Total Download: {:.2f} MB, Total Upload: {:.2f} MB"

def get_download_speed(interface):
    old_value = psutil.net_io_counters(pernic=True)[interface].bytes_recv
    time.sleep(1)
    new_value = psutil.net_io_counters(pernic=True)[interface].bytes_recv
    download_speed = (new_value - old_value) / 1024 / 1024 * 8 # in Mbps
    return download_speed

def get_upload_speed(interface):
    old_value = psutil.net_io_counters(pernic=True)[interface].bytes_sent
    time.sleep(1)
    new_value = psutil.net_io_counters(pernic=True)[interface].bytes_sent
    upload_speed = (new_value - old_value) / 1024 / 1024 * 8 # in Mbps
    return upload_speed

def get_internet_connected_interface():
    gateways = psutil.net_if_addrs()
    for interface, addresses in gateways.items():
        for addr in addresses:
            if addr.family == socket.AF_INET and not addr.address.startswith("127.") and not addr.address.startswith("169.254."):
                return interface
    return None

# Select network interface
interface = args.interface
if interface is None:
    interface = get_internet_connected_interface()
    if interface is None:
        print("No network interface found with internet connection.")
        exit(1)

# Set the target address and port for sending packets based on the protocol type
if args.protocol == "tcp":
    ip = "178.22.122.100"
    port = 53
elif args.protocol == "udp":
    ip = "185.51.200.2"
    port = 53

# Ask for the packet size multiplier with default value
multiplier = args.multiplier

DEFAULT_DATA_SIZE = get_download_speed(interface) * multiplier
data_size_mbit = DEFAULT_DATA_SIZE

# Create a socket based on the protocol type
sock = None
if args.protocol == "tcp":
    sock = socket.socket()
    sock.connect((ip, port))
elif args.protocol == "udp":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create a table to show speed and data usage statistics
table = PrettyTable()
table.field_names = ["Time", "Download Speed (Mbps)", "Upload Speed (Mbps)", "Total Download (MB)", "Total Upload (MB)"]

start_time = time.time()

try:
    while True:
        download_speed = get_download_speed(interface)
        upload_speed = get_upload_speed(interface)

        total_download = psutil.net_io_counters().bytes_recv / 1024 / 1024
        total_upload = psutil.net_io_counters().bytes_sent / 1024 / 1024

        # Add new row to the table
        elapsed_time = round(time.time() - start_time, 2)
        table.add_row([elapsed_time, round(download_speed, 2), round(upload_speed, 2), round(total_download, 2), round(total_upload, 2)])

        # Truncate table if it gets too long
        if len(table._rows) > 20:
            table.del_row(0)

        # Print updated table
        print(table)

        # Send the data with the requested size
        data_size_byte = int(data_size_mbit * 1024 * 1024 / 8)
        mtu = 1400  # Change the value based on your network MTU
        num_packets = data_size_byte // mtu + 1
        for i in range(num_packets):
            start_idx = i * mtu
            end_idx = start_idx + mtu if i < num_packets - 1 else data_size_byte
            payload = b'a' * (end_idx - start_idx)
            if args.protocol == "tcp":
                sock.sendall(payload)
            elif args.protocol == "udp":
                sock.sendto(payload, (ip, port))

        print(f"Packet sent to {ip}:{port}")

        # Wait for some time before next calculation and packet transmission
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    if sock:
        sock.close()
