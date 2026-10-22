import serial
import time
import re

# Configure serial connection
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# Function to send AT command and return the response
def send_at_command(command, timeout=1):
    ser.write((command + '\r').encode())
    time.sleep(timeout)
    response = ser.read(ser.in_waiting).decode()
    return response

# Function to print AT command details and responses
def print_at_command(command):
    response = send_at_command(command, 1)
    print(f"{command}\n{response}")
    return response

# Function to check GPRS attachment
def check_gprs_attachment():
    response = send_at_command('AT+CGATT?', 1)
    return '+CGATT: 1' in response

# Function to get the IP address
def get_ip_address():
    response = send_at_command('AT+CIFSR', 1)
    return response.strip() if response else None

# Function to setup PDP context
def setup_pdp_context():
    send_at_command('AT+CGDCONT=1,"IP","shared.m2m.ch"', 1)
    send_at_command('AT+CSTT="shared.m2m.ch"', 1)
    send_at_command('AT+CIICR', 1)
    return get_ip_address()

# Function to get CSQ value
def get_signal_quality():
    response = send_at_command('AT+CSQ', 1)
    match = re.search(r'\+CSQ: (\d+\,\d+)', response)
    if match:
        return match.group(1)
    else:
        return None

# Function to send data
def send_data(json_data):
    response = send_at_command('AT+CIPSTART="UDP","18.217.31.126","8182"', 1)
    if 'CONNECT OK' in response:
        send_at_command('AT+CIPSEND={}'.format(len(json_data)), 1)
        ser.write(json_data.encode())
        send_at_command('', 1)  # Finish the command after the prompt
        send_at_command('AT+CIPCLOSE', 1)


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


# Function to set local time on the NB-IoT device
def set_local_time():
    # Example: Set the local time and time zone, e.g., "24/07/01,14:57:10+02" for UTC+2
    local_time = time.strftime('%y/%m/%d,%H:%M:%S+02', time.localtime())
    response = send_at_command(f'AT+CCLK="{local_time}"')
    print(response)


# Main loop
while True:
    # Check modem connection
    print("Checking modem connection...")
    if 'OK' in print_at_command('AT'):
        print("[+] Modem connection OK")
    else:
        print("[-] Modem connection failed")
        time.sleep(10)
        continue
    
    # Check signal quality
    signal_quality = get_signal_quality()
    if signal_quality is not None:
        print(f"Signal Quality: {signal_quality}")
    else:
        print("Failed to get signal quality")
    
    # Print GPRS attachment status
    print_at_command('AT+CGATT?')
    
    # Print the current mode
    print_at_command('AT+CPSI?')
    
    # Print PDP context
    print_at_command('AT+CSTT?')
    
    # Print network registration status
    print_at_command('AT+CREG?')
    
    # Print IP address
    ip_address = get_ip_address()
    if ip_address:
        print("IP Address: ", ip_address)
    else:
        print("Failed to get IP address")
    
    # Check GPRS attachment
    if not check_gprs_attachment():
        print("Not attached to GPRS. Retrying...")
        time.sleep(10)
        continue
    
    # Setup PDP context
    ip_address = setup_pdp_context()
    if ip_address:
        print("PDP context established with IP: ", ip_address)
    else:
        print("Failed to establish PDP context. Retrying...")
        time.sleep(10)
        continue
    
    # Prepare JSON data
    json_data = f'{{"s": {signal_quality}}}'
    
    # Send data
    send_data(json_data)
    print("**Data sent: ", json_data)
    
    # Wait for a minute before sending data again
    time.sleep(60)

