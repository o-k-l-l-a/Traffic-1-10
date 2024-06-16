#!/bin/bash

# Variables
REPO_URL="https://github.com/o-k-l-l-a/Traffic-1-10.git"
SERVICE_NAME="traffic_monitor"
SCRIPT_NAME="Traffic-1-10.py"
INSTALL_DIR="/opt/traffic-monitor"

# Function to install packages on Debian-based systems (Ubuntu, Debian)
install_packages_debian() {
    sudo apt-get update -y
    sudo apt-get install -y git python3 python3-pip prometheus git
}

# Function to install packages on RHEL-based systems (AlmaLinux, CentOS)
install_packages_rhel() {
    sudo yum install -y epel-release
    sudo yum install -y git python3 python3-pip
    # Installing Prometheus using the binary
    PROMETHEUS_VERSION="2.31.1"
    cd /tmp
    curl -LO https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz
    tar xvf prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz
    sudo mv prometheus-${PROMETHEUS_VERSION}.linux-amd64/prometheus /usr/local/bin/
    sudo mv prometheus-${PROMETHEUS_VERSION}.linux-amd64/promtool /usr/local/bin/
    sudo mv prometheus-${PROMETHEUS_VERSION}.linux-amd64/{consoles,console_libraries} /etc/prometheus/
}

# Check the OS and call the appropriate function
if [ -f /etc/debian_version ]; then
    install_packages_debian
elif [ -f /etc/redhat-release ]; then
    install_packages_rhel
else
    echo "Unsupported OS"
    exit 1
fi

# Clone the repository
sudo git clone $REPO_URL $INSTALL_DIR

# Change directory to the cloned repository
cd $INSTALL_DIR

# Create a requirements.txt file if it doesn't exist
if [ ! -f requirements.txt ]; then
    echo "psutil" > requirements.txt
    echo "prettytable" >> requirements.txt
fi

# Install required Python packages
sudo pip3 install -r requirements.txt

# Create a systemd service file
sudo bash -c "cat > /etc/systemd/system/$SERVICE_NAME.service <<EOL
[Unit]
Description=Network Speed Monitor and Packet Sender
After=network.target

[Service]
ExecStart=/usr/bin/python3 $INSTALL_DIR/$SCRIPT_NAME -p udp -z 10
WorkingDirectory=$INSTALL_DIR
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOL"

# Reload systemd to apply the new service
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "Service $SERVICE_NAME has been installed and started."
