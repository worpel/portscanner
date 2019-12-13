# A very loud TCP port scanner

# Import socket module for port scanning functionality
import socket
# Import module for regular expressions
import re
# Import datetime class for timestamps
from datetime import datetime

# Prompt user for hostname. If it is a domain, resolve its IP address
host = input('Enter the hostname or IP address of the target: ')
host = socket.gethostbyname(host)

# Basic validation for the host (still allows other forms of invalid input)
while True:
    if host == '':
        host = input('Please enter a valid host: ')
    elif host == '0.0.0.0':
        host = input('Please enter a valid host: ')
    else:
        break

# Get scan timestamp
time = datetime.now().strftime('%d-%m-%Y at %H:%M')

# Define port range. If empty, revert to 1-1023 as default (these ports can only be opened by privileged users)
portRange = input('Define port range that you want to scan (leave blank for well-known ports 1-1023): ')
portRange = portRange if portRange else '1-1023'

# Ensure the given ports fall between 1-65535 (does not compare each value in the range)
if re.match(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])[-]([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$', portRange):
    portRange = portRange
else:
    portRange = input('Please enter a valid port range')

# Format the port range for passing through to socket
portRange = portRange.replace('-', ', ')

# Output scan start date/time
print('Started scan on', time)

# Output scan host
print('Scan report for', host)

# TODO: Pass port range in as int as opposed to str - maybe split(',')
for port in range(portRange):
    # Establish socket for IPv4 TCP scanning
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Prevent timeout on socket connection
    s.settimeout(5)

    while True:
        try:
            # Convert port to integer before passing it into socket
            port = int(port)
            # Open socket TCP connection
            connection = s.connect_ex((host, port))
            # If connection successful, return open port and close socket
            if connection == '0':
                print(f'Discovered {port} open at', time)
                socket.close()
            else:
                print(port)
        # Close socket if a system-related error occurs
        except socket.error:
            print('Connection attempt unsuccessful')
            socket.close()
        # Close socket if an address-related error occurs
        except socket.gaierror:
            print('Unable to connect to host')
            socket.close()
        # Close socket is an unintended timeout occurs
        except socket.timeout:
            print('Connection attempt timed out')
            socket.close()
