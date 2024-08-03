# Traffic-1-10

This Python script monitors network download and upload speeds and sends packets to a specified IP and port using either TCP or UDP protocol. It displays real-time speed and data usage statistics in a neatly formatted table and can also send alert emails if network speeds fall below a specified threshold.

## Features

- Monitors and displays download and upload speeds in Mbps.
- Shows total data downloaded and uploaded in MB.
- Sends packets to a specified IP and port using either TCP or UDP protocol.
- Adjustable packet size multiplier.
- Automatically selects the network interface with an active internet connection.
- Real-time statistics display using `PrettyTable`.
- Logs network data to a CSV file.
- Sends alert emails if network speed drops below a specified threshold.
- Plots graphs of download and upload speeds after execution.

## Requirements

- Python 3.x
- psutil
- prettytable
- matplotlib (for plotting graphs)
- smtplib (for sending emails)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/o-k-l-l-a/Traffic-1-10.git
    cd Traffic-1-10
    ```

2. Install the required Python packages:
    ```bash
    pip install psutil prettytable matplotlib
    ```

## Usage

Run the script with the following command:

```bash
python Traffic-1-10.py [-p PROTOCOL] [-z MULTIPLIER] [-i interface] [-f FILE] [-l LOGFILE] [-e EMAIL] [-t THRESHOLD]
```

### Arguments

- `-p`, `--protocol`: Protocol type for sending packets. Choices are `tcp` or `udp`. Default is `udp`.
- `-z`, `--multiplier`: Multiplier value for packet size. Default is `10`.
- `-i`, `--interface`: Network interface to use.
- `-f`, `--file`: File containing the list of IP addresses.
- `-l`, `--logfile`: File to log network data.
- `-e`, `--email`: Email address to send alerts to.
- `-t`, `--threshold`: Speed threshold in Mbps for sending alerts. Default is `1.0`.

### Example

To run the script using UDP protocol, a packet size multiplier of 20, logging to `network_log.csv`, and sending alerts to an email address:

```bash
python3 Traffic-1-10.py -p udp -z 20 -i eno1 -f IP.txt -l network_log.csv -e your_email@example.com -t 2.0
```

## How It Works

1. The script identifies the network interface with an active internet connection.
2. It calculates download and upload speeds by measuring the bytes received and sent over a one-second interval.
3. It sends packets to the specified IP and port using the chosen protocol (TCP or UDP) with a data size determined by the download speed and multiplier.
4. It logs network data to a CSV file and displays real-time speed and data usage statistics in a formatted table.
5. Sends alert emails if network speed falls below the specified threshold.
6. Plots a graph of download and upload speeds after execution.

## Code Structure

- `get_download_speed(interface)`: Measures the download speed for the specified network interface.
- `get_upload_speed(interface)`: Measures the upload speed for the specified network interface.
- `get_internet_connected_interface()`: Finds and returns the network interface with an active internet connection.
- `send_alert(email, message)`: Sends an alert email to the specified address.
- `monitor_network()`: Main loop to monitor network speed and update the statistics table.
- `send_packets()`: Sends packets to the specified IP and port.
- `plot_graph(data)`: Plots the graph of download and upload speeds.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Author

- Your Name (okila@telegmail.com)
