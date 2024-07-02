import serial
import time

def send_at_command(ser, command, timeout=2):
    ser.write((command + '\r').encode())
    time.sleep(timeout)
    response = ser.read(ser.in_waiting).decode()
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
        
        # Open a TCP connection to the server
        server_ip = "44.209.119.53"  # IP address resolved from your hostname
        port = "80"  # HTTP port
        response = send_at_command(ser, f'AT+CIPSTART="TCP","{server_ip}","{port}"')
        print(response)
        
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
        print(response)
        
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

        ser.close()

    except Exception as e:
        print(f"Error: {e}")
        print("Not Connected: Error.")

if __name__ == "__main__":
    main()

