#!/bin/bash

# Default port
port=8126

# Check if the -p option is provided to set a custom port
while getopts ":p:" opt; do
  case $opt in
    p)
      port=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# Find and kill existing Python processes using the specified port
pkill -f "python3 -m http.server $port"

# Navigate to the directory where your website files are located
cd ../ 

# Start a simple HTTP server on the specified port
python3 -m http.server $port &

# Get the local IP address of your machine
ip_address=$(hostname -I | cut -d' ' -f1)

# Print the IP address and port to access the website
echo "Your website is available at: http://${ip_address}:${port}"

# Keep the script running
read -p "Press Enter to stop the server" && pkill -f "python3 -m http.server $port"
