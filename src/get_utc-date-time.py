import serial
import time
import re
from datetime import datetime, timedelta

# Configure serial connection
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# Function to send AT command and return the response
def send_at_command(command, timeout=1):
    ser.write((command + '\r').encode())
    time.sleep(timeout)
    response = ser.read(ser.in_waiting).decode()
    return response

# Function to set local time (use this function to set the time initially)
def set_local_time():
    # Set the local time and time zone, e.g., "24/07/01,14:57:10+02" for UTC+2
    local_time = time.strftime('%y/%m/%d,%H:%M:%S+02', time.localtime())
    response = send_at_command(f'AT+CCLK="{local_time}"')
    print(response)

# Function to get UTC date and time
def get_utc_datetime():
    response = send_at_command('AT+CCLK?')
    match = re.search(r'\+CCLK: "(\d+/\d+/\d+,\d+:\d+:\d+)([+-]\d+)"', response)
    if match:
        datetime_str = match.group(1)
        tz_offset = int(match.group(2))
        # Parse the datetime string
        local_datetime = datetime.strptime(datetime_str, '%y/%m/%d,%H:%M:%S')
        # Calculate UTC time by subtracting the offset
        utc_datetime = local_datetime - timedelta(hours=tz_offset)
        return utc_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return None

# Main loop to check the UTC date and time
while True:
    print("Getting UTC date and time...")
    utc_datetime = get_utc_datetime()
    if utc_datetime:
        print(f"UTC Date and Time: {utc_datetime}")
    else:
        print("Failed to get UTC date and time")
    
    # Wait for a minute before checking again
    time.sleep(5)

