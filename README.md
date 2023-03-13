
# Traffic-1-10
We understand that many users in Iran have severe restrictions from Iran's data centers, so we have decided to create a script based on the udp protocol, which can bypass the 1/10 limitation of Iran's servers.

Usage: python Traffic-1-10.py <ip> -p <port> -t <time> -s <size>

Only the IP is required.
If no port is specified, it will send packets on random ports.
If no time is specified, it will take forever. The time is in seconds.
Size defaults to 1024 bytes. The maximum value is 65530.
