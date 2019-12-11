# A very loud TCP scanner

# Import socket module
import socket
# Import datetime class
from datetime import datetime

# Define host or domain name and store it to a variable
host = input('Enter the domain or IP of target: ')
# Get scan timestamp
time = datetime.now()
# Format timestamp
time = time.strftime("%d-%m-%Y at %H:%M")
# Create socket object
socket = socket.socket()
# Define port range
portRange = input('Define port range that you want to scan (leave blank for 1-1024)')

# Output scan start date/time
print('Started scan on', time)
# Output scan host
print('Scan report for', host)

print(host)
