from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import argparse
import ssl
import re
from datetime import datetime
import os

class GenericHoneypotHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config', {})
        super().__init__(*args, **kwargs)

    def version_string(self):
        return self.config.get('server_name', 'GenericServer/1.0')

    def log_request_info(self, method):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'client_address': self.client_address[0],
            'method': method,
            'path': self.path,
            'headers': dict(self.headers),
            'post_data': None
        }

        if method == 'POST':
            content_length = int(self.headers.get('Content-Length', 0))
            log_data['post_data'] = self.rfile.read(content_length).decode('utf-8')

        log_filename = f"honeypot_log_{datetime.now().strftime('%Y-%m-%d')}.json"
        
        with open(log_filename, 'a') as log_file:
            json.dump(log_data, log_file)
            log_file.write('\n')  # Add a newline for readability

    def handle_request(self, method):
        self.log_request_info(method)

        path = self.path.strip('/')
        responses = self.config.get('responses', {})

        matching_path = next((p for p in responses if re.match(p, path)), None)
        if matching_path:
            response = responses[matching_path].get(method, {})
        else:
            response = {}

        if response.get('auth_required', False):
            auth_header = self.headers.get('Authorization')
            if not self.check_auth(auth_header):
                self.send_error(401, 'Unauthorized')
                return

        status_code = response.get('status_code', 200)
        headers = response.get('headers', {})
        body = response.get('body', '').encode('utf-8')

        self.send_response(status_code)
        
        for header, value in headers.items():
            self.send_header(header, value)
        
        self.end_headers()
        self.wfile.write(body)

    def check_auth(self, auth_header):
        if not auth_header:
            return False
        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':')
        return username == self.config.get('auth', {}).get('username') and password == self.config.get('auth', {}).get('password')

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def do_PUT(self):
        self.handle_request('PUT')

    def do_DELETE(self):
        self.handle_request('DELETE')

def load_config(config_path):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def run_server(port, config, use_ssl=False):
    server_address = ('', port)
    handler = lambda *args, **kwargs: GenericHoneypotHandler(*args, config=config, **kwargs)
    httpd = HTTPServer(server_address, handler)

    if use_ssl:
        httpd.socket = ssl.wrap_socket(httpd.socket,
                                       keyfile=config.get('ssl', {}).get('keyfile'),
                                       certfile=config.get('ssl', {}).get('certfile'),
                                       server_side=True)

    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a generic honeypot server')
    parser.add_argument('-p', '--port', type=int, default=8080, help='Port to run the server on (default: 8080)')
    parser.add_argument('-c', '--config', type=str, required=True, help='Path to the configuration file')
    parser.add_argument('--ssl', action='store_true', help='Enable SSL')
    args = parser.parse_args()

    config = load_config(args.config)
    run_server(args.port, config, args.ssl)
