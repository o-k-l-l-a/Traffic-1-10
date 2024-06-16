#!/bin/bash

# Variables
REPO_URL="https://github.com/o-k-l-l-a/Traffic-1-10.git"
SERVICE_NAME="traffic_monitor"
SCRIPT_NAME="Traffic-1-10.py"
INSTALL_DIR="/opt/traffic-monitor"

# Update and install necessary packages
sudo apt-get update
sudo apt-get install -y git python3 python3-pip

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
