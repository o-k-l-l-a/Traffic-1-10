import psutil
import time
import socket
from prettytable import PrettyTable

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

# Ask for the network interface name and protocol type
interface = input("Enter network interface name (e.g. en0): ")
protocol_type = input("Enter the protocol type (TCP/UDP): ")

# Set the target address and port for sending packets based on the protocol type
if protocol_type.lower() == "tcp":
    ip = "178.22.122.100"
    port = 53
elif protocol_type.lower() == "udp":
    ip = "185.51.200.2"
    port = 53

# Ask for the packet size multiplier
multiplier = int(input("Enter multiplier value (e.g. 20): "))
DEFAULT_DATA_SIZE = get_download_speed(interface) * multiplier
data_size_mbit = DEFAULT_DATA_SIZE

# Create a table to show speed and data usage statistics
table = PrettyTable()
table.field_names = ["Time", "Download Speed (Mbps)", "Upload Speed (Mbps)", "Total Download (MB)", "Total Upload (MB)"]

start_time = time.time()

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

    print(table)

    # Create a socket based on the protocol type
    if protocol_type.lower() == "tcp":
        sock = socket.socket()
        sock.connect((ip, port))
    elif protocol_type.lower() == "udp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the data with the requested size
    data_size_byte = int(data_size_mbit * 1024 * 1024 / 8)
    mtu = 1400 # Change the value based on your network MTU
    num_packets = data_size_byte // mtu + 1
    for i in range(num_packets):
        start_idx = i * mtu
        end_idx = start_idx + mtu if i < num_packets - 1 else data_size_byte
        payload = b'a' * (end_idx - start_idx)
        if protocol_type.lower() == "tcp":
            sock.sendall(payload)
        elif protocol_type.lower() == "udp":
            sock.sendto(payload, (ip, port))

    print("Packet sent to {}:{}".format(ip, port))
    
    # Wait for some time before next calculation and packet transmission
    time.sleep(1)
