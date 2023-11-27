import os
import socket
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import signal
import sys
import threading
import argparse

def find_index_file(directory):
    index_files = ['index.html', 'index.htm']
    for file in index_files:
        if os.path.exists(os.path.join(directory, file)):
            return file
    return None

def get_parent_directory(directory):
    return os.path.abspath(os.path.join(directory, os.pardir))

def get_local_ip():
    try:
        # This may not work on all systems, depending on the network configuration
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return '127.0.0.1'

def host_locally(directory, port=8000):
    os.chdir(directory)
    Handler = SimpleHTTPRequestHandler
    with TCPServer(("0.0.0.0", port), Handler) as httpd:
        local_ip = get_local_ip()
        print(f"Serving at http://{local_ip}:{port}")

        # Register a signal handler to gracefully shut down the server
        def signal_handler(sig, frame):
            print("Shutting down server...")
            httpd.shutdown()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Run the server in a separate thread
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.start()
        server_thread.join()

def main():
    parser = argparse.ArgumentParser(description="Simple HTTP Server with optional port specification.")
    parser.add_argument("-p", "--port", type=int, help="Port number to use. Default is 8000.", default=8000)
    args = parser.parse_args()

    current_directory = os.getcwd()
    parent_directory = get_parent_directory(current_directory)
    index_file = find_index_file(parent_directory)

    if index_file:
        host_locally(parent_directory, port=args.port)
    else:
        print("No index.html found in the parent directory.")

if __name__ == "__main__":
    main()
