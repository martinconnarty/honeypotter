# HoneyPotter

A flexible and configurable HTTP honeypot server designed to mimic various web services and log all interactions. Full disclosure - This Readme and the tool were created using AI

## Features

- Highly configurable through JSON configuration files
- Mimics any HTTP-based service (e.g., Exchange Server, Apache, Nginx)
- Supports custom routing with regex path matching
- Logs all requests, including headers and POST data, in structured JSON format
- Daily log rotation for easy management
- Optional SSL support
- Basic authentication support

## Requirements

- Python 3.6+
- No external dependencies

## Installation

1. Clone this repository or download the `generic_honeypot.py` script.
2. Ensure you have Python 3.6 or higher installed.

## Usage

Run the honeypot server using the following command:

```
python generic_honeypot.py -p <port> -c <config_file> [--ssl]
```

Arguments:

- `-p, --port`: Port to run the server on (default: 8080)
- `-c, --config`: Path to the configuration file (required)
- `--ssl`: Enable SSL (optional)

Example:

```
python honeypotter.py -p 443 -c exchange.json --ssl
```

## Configuration

Create a JSON configuration file to define the behavior of your honeypot. Here's a basic structure:

```json
{
    "server_name": "Your-Server-Name",
    "auth": {
        "username": "admin",
        "password": "password123"
    },
    "ssl": {
        "keyfile": "path/to/your/key.pem",
        "certfile": "path/to/your/cert.pem"
    },
    "responses": {
        "^path/to/match$": {
            "GET": {
                "status_code": 200,
                "headers": {
                    "Content-Type": "text/html"
                },
                "body": "<html><body>Hello, World!</body></html>"
            }
        }
    }
}
