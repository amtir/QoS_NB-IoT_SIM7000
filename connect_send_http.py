import serial
import time

def send_at_command(ser, command, timeout=2):
    ser.write((command + '\r').encode())
    time.sleep(timeout)
    response = ser.read(ser.in_waiting).decode()
    print(f"Command: {command}\nResponse: {response}")
    return response

def wait_for_response(ser, expected_response, timeout=10):
    end_time = time.time() + timeout
    response = ""
    while time.time() < end_time:
        if ser.in_waiting:
            response += ser.read(ser.in_waiting).decode()
            if expected_response in response:
                return response
        time.sleep(0.1)
    return None

def connect_to_network(ser):
    # Check signal quality
    send_at_command(ser, 'AT+CSQ')
    
    # Check registration status
    response = send_at_command(ser, 'AT+CREG?')
    if '+CREG: 0,1' not in response and '+CREG: 0,5' not in response:
        print("Not registered to network. Attempting to register...")
        return False

    # Attach to GPRS
    response = send_at_command(ser, 'AT+CGATT?')
    if '+CGATT: 1' not in response:
        print("Not attached to GPRS. Attempting to attach...")
        return False

    # Set APN
    send_at_command(ser, 'AT+CGDCONT=1,"IP","shared.m2m.ch"')
    
    # Start task and set APN
    send_at_command(ser, 'AT+CSTT="shared.m2m.ch"')
    
    # Bring up wireless connection
    response = send_at_command(ser, 'AT+CIICR')
    if 'OK' not in response:
        print("Failed to bring up wireless connection.")
        return False
    
    # Get local IP address
    response = send_at_command(ser, 'AT+CIFSR')
    if 'ERROR' in response:
        print("Failed to get IP address.")
        return False

    print(f"IP Address: {response.strip()}")
    return True

def send_http_message(ser):
    # Open a TCP connection to the server
    server_ip = "44.209.119.53"  # IP address resolved from your hostname
    port = "80"  # HTTP port
    response = send_at_command(ser, f'AT+CIPSTART="TCP","{server_ip}","{port}"')
    
    # Wait for the connection to be established
    connection_response = wait_for_response(ser, "CONNECT OK")
    if not connection_response or "CONNECT OK" not in connection_response:
        print("Error: TCP connection was not established.")
        return

    # Prepare HTTP GET request
    http_request = (
        "GET / HTTP/1.1\r\n"
        "Host: eoqa51bb0wezap8.m.pipedream.net\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    
    # Send HTTP GET request
    response = send_at_command(ser, f'AT+CIPSEND={len(http_request)}')
    
    # Wait for prompt '>'
    send_response = wait_for_response(ser, ">")
    if not send_response or ">" not in send_response:
        print("Error: '>' prompt not received for AT+CIPSEND.")
        return
    
    # Send the actual request
    ser.write(http_request.encode())
    
    # Wait for server response
    time.sleep(5)  # Adjust time based on server response time
    response = ser.read(ser.in_waiting).decode()
    print("Server Response:")
    print(response)

    # Close the TCP connection
    print(send_at_command(ser, 'AT+CIPCLOSE'))

def main():
    try:
        ser = serial.Serial("/dev/ttyAMA0")
        ser.baudrate = 9600
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 2
        ser.flushOutput()
        
        print("Connected to Serial.")

        # Check if already connected and has an IP address
        response = send_at_command(ser, 'AT+CIFSR')
        if 'ERROR' in response:
            print("No existing IP address. Connecting to network...")
            if not connect_to_network(ser):
                print("Failed to connect to network.")
                return
        else:
            print(f"Already connected. IP Address: {response.strip()}")
        
        # Send HTTP message
        send_http_message(ser)

        ser.close()

    except Exception as e:
        print(f"Error: {e}")
        print("Not Connected: Error.")

if __name__ == "__main__":
    main()

