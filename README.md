فایل `README.md` به‌روزرسانی شده برای پروژه‌ی شما با توجه به لینک گیت‌هاب و نام فایل:

```markdown
# Traffic-1-10

This Python script monitors network download and upload speeds and sends packets to a specified IP and port using either TCP or UDP protocol. It displays real-time speed and data usage statistics in a neatly formatted table.

## Features

- Monitors and displays download and upload speeds in Mbps.
- Shows total data downloaded and uploaded in MB.
- Sends packets to a specified IP and port using either TCP or UDP protocol.
- Adjustable packet size multiplier.
- Automatically selects the network interface with an active internet connection.
- Real-time statistics display using `PrettyTable`.

## Requirements

- Python 3.x
- psutil
- prettytable

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/o-k-l-l-a/Traffic-1-10.git
    cd Traffic-1-10
    ```

2. Install the required Python packages:
    ```bash
    pip install psutil prettytable
    ```

## Usage

Run the script with the following command:

```bash
python Traffic-1-10.py [-p PROTOCOL] [-z MULTIPLIER]
```

### Arguments

- `-p`, `--protocol`: Protocol type for sending packets. Choices are `tcp` or `udp`. Default is `udp`.
- `-z`, `--multiplier`: Multiplier value for packet size. Default is `10`.

### Example

To run the script using UDP protocol and a packet size multiplier of 20:

```bash
python Traffic-1-10.py -p udp -z 20
```

## How It Works

1. The script determines the network interface with an active internet connection.
2. It calculates download and upload speeds by measuring the bytes received and sent over a one-second interval.
3. It sends packets to a specified IP and port using the chosen protocol (TCP or UDP) with a data size determined by the download speed and multiplier.
4. It displays real-time speed and data usage statistics in a formatted table.

## Code Structure

- `get_download_speed(interface)`: Measures the download speed for the specified network interface.
- `get_upload_speed(interface)`: Measures the upload speed for the specified network interface.
- `get_internet_connected_interface()`: Finds and returns the network interface with an active internet connection.
- Argument parsing and setup: Parses command-line arguments and sets up the protocol, IP, port, and packet size.
- Main loop: Continuously measures speed, sends packets, and updates the statistics table.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Author

- Your Name (okila@telegmail.com)

```
