import serial
import time

# Configure serial connection
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# Function to send AT command and return the response
def send_at_command(command, timeout=1):
    ser.write((command + '\r').encode())
    time.sleep(timeout)
    response = ser.read(ser.in_waiting).decode()
    return response

# Function to set local time on the NB-IoT device
def set_local_time():
    # Example: Set the local time and time zone, e.g., "24/07/01,14:57:10+02" for UTC+2
    local_time = time.strftime('%y/%m/%d,%H:%M:%S+02', time.localtime())
    response = send_at_command(f'AT+CCLK="{local_time}"')
    print(response)

# Set the local time once during initial setup
set_local_time()

