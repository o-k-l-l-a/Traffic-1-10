import argparse
import psutil
import time
import socket
from prettytable import PrettyTable
import random
import csv
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt
from threading import Thread

# تنظیمات اولیه
parser = argparse.ArgumentParser(description='Network Speed Monitor and Packet Sender')

# افزودن آرگومان‌ها
parser.add_argument('-p', '--protocol', type=str, default='udp', choices=['tcp', 'udp', 'icmp'],
                    help='Protocol type (TCP, UDP, or ICMP)')
parser.add_argument('-z', '--multiplier', type=int, default=10,
                    help='Multiplier value for packet size')
parser.add_argument('-i', '--interface', type=str, default=None,
                    help='Network interface to use')
parser.add_argument('-f', '--file', type=str, required=True,
                    help='File containing IP addresses')
parser.add_argument('-l', '--logfile', type=str, default='network_log.csv',
                    help='File to log network data')
parser.add_argument('-e', '--email', type=str,
                    help='Email address to send alerts to')
parser.add_argument('-t', '--threshold', type=float, default=1.0,
                    help='Threshold speed in Mbps for sending alerts')

args = parser.parse_args()

# خواندن لیست IP‌ها از فایل
with open(args.file, 'r') as f:
    ip_list = [line.strip() for line in f.readlines()]

# تابع برای دریافت سرعت دانلود
def get_download_speed(interface):
    old_value = psutil.net_io_counters(pernic=True)[interface].bytes_recv
    time.sleep(1)
    new_value = psutil.net_io_counters(pernic=True)[interface].bytes_recv
    download_speed = (new_value - old_value) / 1024 / 1024 * 8  # in Mbps
    return download_speed

# تابع برای دریافت سرعت آپلود
def get_upload_speed(interface):
    old_value = psutil.net_io_counters(pernic=True)[interface].bytes_sent
    time.sleep(1)
    new_value = psutil.net_io_counters(pernic=True)[interface].bytes_sent
    upload_speed = (new_value - old_value) / 1024 / 1024 * 8  # in Mbps
    return upload_speed

# تابع برای انتخاب رابط شبکه متصل به اینترنت
def get_internet_connected_interface():
    gateways = psutil.net_if_addrs()
    for interface, addresses in gateways.items():
        for addr in addresses:
            if addr.family == socket.AF_INET and not addr.address.startswith("127.") and not addr.address.startswith("169.254."):
                return interface
    return None

# تابع برای ارسال ایمیل هشدار
def send_alert(email, message):
    try:
        smtp_server = 'smtp.example.com'  # سرور SMTP خود را وارد کنید
        smtp_port = 587  # پورت SMTP
        smtp_username = 'your_email@example.com'  # ایمیل شما
        smtp_password = 'your_password'  # رمز عبور ایمیل شما

        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = 'Network Speed Alert'

        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send alert email: {e}")

# تنظیمات لاگینگ
logging.basicConfig(filename=args.logfile, level=logging.INFO, format='%(asctime)s,%(message)s')

# انتخاب رابط شبکه
interface = args.interface
if interface is None:
    interface = get_internet_connected_interface()
    if interface is None:
        print("No network interface found with internet connection.")
        exit(1)

# تنظیم پورت هدف برای ارسال بسته‌ها بر اساس نوع پروتکل
port = 53

# نمایش گرافیکی داده‌ها
def plot_graph(data):
    times = [row[0] for row in data]
    download_speeds = [row[1] for row in data]
    upload_speeds = [row[2] for row in data]

    plt.figure(figsize=(10, 5))
    plt.plot(times, download_speeds, label='Download Speed (Mbps)')
    plt.plot(times, upload_speeds, label='Upload Speed (Mbps)')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (Mbps)')
    plt.legend()
    plt.grid(True)
    plt.show()

# تنظیمات جدول نمایش
table = PrettyTable()
table.field_names = ["Time", "Download Speed (Mbps)", "Upload Speed (Mbps)", "Total Download (MB)", "Total Upload (MB)"]

start_time = time.time()
data_log = []

# حلقه اصلی برای اندازه‌گیری و ارسال بسته‌ها
def monitor_network():
    try:
        while True:
            download_speed = get_download_speed(interface)
            upload_speed = get_upload_speed(interface)

            total_download = psutil.net_io_counters().bytes_recv / 1024 / 1024
            total_upload = psutil.net_io_counters().bytes_sent / 1024 / 1024

            elapsed_time = round(time.time() - start_time, 2)
            table.add_row([elapsed_time, round(download_speed, 2), round(upload_speed, 2), round(total_download, 2), round(total_upload, 2)])

            if len(table._rows) > 20:
                table.del_row(0)

            print(table)
            data_log.append([elapsed_time, download_speed, upload_speed])

            logging.info(f"{elapsed_time},{download_speed},{upload_speed},{total_download},{total_upload}")

            if download_speed < args.threshold or upload_speed < args.threshold:
                if args.email:
                    send_alert(args.email, f"Low network speed detected. Download: {download_speed} Mbps, Upload: {upload_speed} Mbps")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting...")
        plot_graph(data_log)
    finally:
        if sock:
            sock.close()

# تابع برای ارسال بسته‌ها
def send_packets():
    DEFAULT_DATA_SIZE = get_download_speed(interface) * args.multiplier
    data_size_mbit = DEFAULT_DATA_SIZE

    sock = None
    if args.protocol == "tcp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif args.protocol == "udp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            ip = random.choice(ip_list)
            data_size_byte = int(data_size_mbit * 1024 * 1024 / 8)
            mtu = 1400  # Change the value based on your network MTU
            num_packets = data_size_byte // mtu + 1
            for i in range(num_packets):
                start_idx = i * mtu
                end_idx = start_idx + mtu if i < num_packets - 1 else data_size_byte
                payload = b'a' * (end_idx - start_idx)
                if args.protocol == "tcp":
                    if sock is None or sock.fileno() == -1:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((ip, port))
                    sock.sendall(payload)
                elif args.protocol == "udp":
                    sock.sendto(payload, (ip, port))

            print(f"Packet sent to {ip}:{port}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if sock:
            sock.close()

# اجرای چندنخی برای مانیتورینگ و ارسال بسته‌ها
monitor_thread = Thread(target=monitor_network)
packet_thread = Thread(target=send_packets)

monitor_thread.start()
packet_thread.start()

monitor_thread.join()
packet_thread.join()
