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

# Set the target address and port for sending packets
ip = "1.1.1.1"
port = 443

interface = input("Enter network interface name (e.g. en0): ")
DEFAULT_DATA_SIZE = get_download_speed(interface) * 10
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

    # Create a TCP socket
    sock = socket.socket()
    sock.connect((ip, port))

    # Send the data with the requested size
    data_size_byte = int(data_size_mbit * 1024 * 1024 / 8)
    payload = b'a' * data_size_byte
    sock.sendall(payload)

    print("Packet sent to {}:{}".format(ip, port))
    
    # Wait for some time before next calculation and packet transmission
    time.sleep(1)
# pip install psutil
# pip install prettytable
