# A very loud TCP port scanner

# Import socket module for port scanning functionality
import socket
# Import datetime class for timestamps
from datetime import datetime
# Import scapy for packet manipulation
from scapy.all import *
import sys

# Close application if script is not running as root
if not os.geteuid() == 0:
    sys.exit('Root is required')

# Prompt user for host
host = input('Enter the hostname or IP address of the target: ')
scanType = input('Choose scan type: TCP or SYN (stealthy): ')

# Check given host is online
def pingHost(host):
    if scanType == 'TCP':
        while True:
            try:
                # Resolve host using socket
                socket.gethostbyname(host)
                host = socket.gethostbyname(host)
                break
            except Exception:
                # If unable to connect, re-prompt
                print('Unable to connect to', host)
                host = input('Enter the hostname or IP address of the target: ')
    elif scanType == 'SYN':
        while True:
            try:
                # Craft ICMP packet to ping host using Scapy
                packet = sr1(IP(dst=host)/ICMP(), timeout=5)
                break
            except Exception:
                # If unable to connect, re-prompt
                print('Unable to connect to', host)
                host = input('Enter another host: ')
    else:
        sys.exit('Invalid scan type provided, exiting...')

pingHost(host)

# Define port range. If empty, revert to 1-1023 as default (these ports can only be opened by privileged users)
portRange = input(
    'Define port range that you want to scan (leave blank for well-known ports 1-1023): '
)
portRange = portRange if portRange else '1-1023'

while True:
    # Format the port range for passing through to socket
    portRange = portRange.split('-')
    startPort = int(portRange[0])
    endPort = int(portRange[1])

    # Check port range is valid
    if startPort >= 0 and startPort < endPort:
        if endPort > startPort and endPort <= 65535:
            portRange = portRange
            break
    else:
        portRange = input('Please enter a valid port range: ')

# Output scan start date/time
print('Started scan on', datetime.now().strftime(f'%d-%m-%Y at %H:%M:%S'))

# Output scan host
print('Scan report for', host)

# Craft packet
# sendPacket = sr1(IP(dst=host) / TCP(dport=(startPort, endPort)))

# print(sendPacket)

if scanType == 'TCP':
    for port in range(startPort, endPort + 1):
        # Establish socket for IPv4 TCP scanning
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout on socket connection
        s.settimeout(1)

        try:
            # Open socket TCP connection
            connection = s.connect_ex((host, port))
            # If connection successful, return open port
            if connection == 0:
                print(datetime.now().strftime('%H:%M:%S') +
                      f': Port {port} is open')
        # Handle socket exceptions
        except socket.error:
            print('Connection attempt unsuccessful')
        except socket.gaierror:
            print('Unable to connect to host')
        except socket.timeout:
            print('Connection attempt timed out')
elif scanType == 'SYN':
    print('Handle SYN scan here')

print('Scan completed on', datetime.now().strftime(f'%d-%m-%Y at %H:%M:%S'))
