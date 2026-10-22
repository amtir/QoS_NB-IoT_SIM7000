import serial
import time
import re
from datetime import datetime, timedelta
import os

# Configure serial connection
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# Function to send AT command and return the response
def send_at_command(command, timeout=1):
    ser.write((command + '\r').encode())
    time.sleep(timeout)
    response = ser.read(ser.in_waiting).decode()
    return response

# Function to get UTC date and time from the NB-IoT device
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

# Function to synchronize the Raspberry Pi's time with the NB-IoT device
def sync_time_with_device():
    utc_datetime = get_utc_datetime()
    if utc_datetime:
        # Use timedatectl to set the system time
        os.system(f'sudo timedatectl set-time "{utc_datetime}"')
        print(f"Synchronized UTC Date and Time: {utc_datetime}")
    else:
        print("Failed to get UTC date and time")

# Main loop to synchronize time after booting
sync_time_with_device()

