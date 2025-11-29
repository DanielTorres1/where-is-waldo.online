#!/usr/bin/env python3
"""
Simple HTTP Server for Where's Waldo Website
Serves the website on the public IP address
"""

import http.server
import socketserver
import os

# Configuration
PORT = 80
HOST = '0.0.0.0'  # Listen on all interfaces including public IP
DIRECTORY = '/home/daniel/imgur/sites/where-is-waldo.online'

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers if needed
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def main():
    # Change to the website directory
    os.chdir(DIRECTORY)
    
    # Create the server
    with socketserver.TCPServer((HOST, PORT), MyHTTPRequestHandler) as httpd:
        print(f"Server started successfully!")
        print(f"Serving directory: {DIRECTORY}")
        print(f"Listening on: {HOST}:{PORT}")
        print(f"Access the website at: http://173.249.26.59:{PORT}")
        print(f"\nPress Ctrl+C to stop the server\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    main()
