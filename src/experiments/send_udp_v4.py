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

# Function to print AT command details and responses with status messages
def print_at_command(command, success_message, failure_message):
    response = send_at_command(command, 1)
    nugget = extract_nugget(response)
    print(f"{command}\n{nugget}")
    if 'OK' in response or '1' in response:
        print(f"[+] {success_message}")
    else:
        print(f"[-] {failure_message}")
    return response

# Function to extract nugget part from the response
def extract_nugget(response):
    match = re.search(r'\+.*', response)
    if match:
        return match.group(0)
    return response.strip()

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

# Main loop
while True:
    # Check modem connection
    print("Checking modem connection...")
    print_at_command('AT', "Modem connection OK", "Modem connection failed")
    
    # Check signal quality
    signal_quality = get_signal_quality()
    if signal_quality is not None:
        print(f"Signal Quality: {signal_quality}")
    else:
        print("Failed to get signal quality")
    
    # Print GPRS attachment status
    print_at_command('AT+CGATT?', "GPRS attached", "GPRS not attached")
    
    # Print the current mode
    print_at_command('AT+CPSI?', "Current mode retrieved", "Failed to retrieve current mode")
    
    # Print PDP context
    print_at_command('AT+CSTT?', "PDP context active", "PDP context not active")
    
    # Print network registration status
    print_at_command('AT+CREG?', "Network registered", "Network not registered")
    
    # Print IP address
    ip_address = get_ip_address()
    if ip_address:
        print(f"[+] IP Address: {ip_address}")
    else:
        print("[-] Failed to get IP address")
    
    # Check GPRS attachment
    if not check_gprs_attachment():
        print("Not attached to GPRS. Retrying...")
        time.sleep(10)
        continue
    
    # Setup PDP context
    ip_address = setup_pdp_context()
    if ip_address:
        print(f"[+] PDP context established with IP: {ip_address}")
    else:
        print("[-] Failed to establish PDP context. Retrying...")
        time.sleep(10)
        continue
    
    # Prepare JSON data
    json_data = f'{{"s": {signal_quality}}}'
    
    # Send data
    send_data(json_data)
    print(f"**Data sent: {json_data}")
    
    # Wait for a minute before sending data again
    time.sleep(60)

