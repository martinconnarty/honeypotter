# HoneyPotter

##  Full disclosure - Most of this Readme and the tool were created using AI

A flexible and configurable HTTP honeypot server designed to mimic various web services and log all interactions. 

It is designed more for bots that are scanning than it is to trick a human, to do this we would need to host a variety of JS/CSS files etc which could without careful implementation lead to security issues of its own. 

## Future Plan

- Test for vulnerabilities in this tool itself! Although, as a honeypot it would be advisable to treat this as something which will get pwned.

- I want to add more config files that more accurately imitate the behaviours of various services. 

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

1. Clone this repository or download the `honeypotter.py` script.
2. Ensure you have Python 3.6 or higher installed.

## Usage

Run the honeypot server using the following command:

```
python honeypotter.py -p <port> -c <config_file> [--ssl]
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
