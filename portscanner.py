# A very loud TCP scanner

# Import socket module for port scanning functionality
import socket
# Import module for regular expressions
import re
# Import datetime class for timestamps
from datetime import datetime

def isBlank():
    input('Invalid input, please re-enter: ')

# Define host or domain name and store it to a variable
host = input('Enter the domain or IP address of the target: ')

if host:
    host = host
else:
    host = isBlank()

# Get scan timestamp
time = datetime.now().strftime('%d-%m-%Y at %H:%M')

# Define port range. If empty, revert to 1-1023 as default (can only be opened by privileged users)
portRange = input('Define port range that you want to scan (leave blank for well-known ports 1-1023): ')
portRange = portRange if portRange else '1-1023'

# Ensure the given ports fall between 1-65535 - does not compare each value in the range
if re.match(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])[-]([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$', portRange):
    portRange = portRange
else:
    portRange = isBlank()

# Output scan start date/time
print('Started scan on', time)

# Output scan host
print('Scan report for', host)

# Create socket object
socket = socket.socket()
