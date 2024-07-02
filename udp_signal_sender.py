import serial
import time
import threading

# Function to send AT command and get the response
def send_at_command(ser, command, timeout=2):
    ser.write((command + '\r').encode())
    time.sleep(timeout)
    response = ser.read(ser.in_waiting).decode()
    print(f"Command: {command}\nResponse: {response}")
    return response

# Function to get the signal strength
def get_signal_strength(ser):
    response = send_at_command(ser, 'AT+CSQ')
    if 'CSQ' in response:
        try:
            # Extract signal strength value
            signal_strength = int(response.split()[1].split(',')[0])
            return signal_strength
        except:
            return None
    return None

# Function to send UDP message using AT commands
def send_udp_message(ser, server_ip, server_port, message):
    # Start UDP connection
    response = send_at_command(ser, f'AT+CIPSTART="UDP","{server_ip}","{server_port}"')
    if 'ERROR' in response:
        print("Error: Failed to start UDP connection.")
        return
    
    # Send the message
    response = send_at_command(ser, f'AT+CIPSEND={len(message)}')
    if '>' in response:
        ser.write(message.encode() + b'\x1A')  # Append Ctrl+Z to indicate end of message
        response = ser.read(ser.in_waiting).decode()
        print(f"Message: {message}\nResponse: {response}")
    
    # Close the UDP connection
    send_at_command(ser, 'AT+CIPCLOSE')

# Function to be run in the thread
def udp_sender_thread(ser, server_ip, server_port):
    while True:
        signal_strength = get_signal_strength(ser)
        if signal_strength is not None:
            message = '{"s":' + str(signal_strength) + '}'
            send_udp_message(ser, server_ip, server_port, message)
            print(f"Sent message: {message}")
        else:
            print("Failed to get signal strength.")
        time.sleep(60)  # Wait for 1 minute

def main():
    # Serial setup
    ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=2)
    ser.flushOutput()

    # Test serial connection
    if 'OK' not in send_at_command(ser, 'AT'):
        print("Failed to connect to serial device.")
        return

    # Start UDP sender thread
    server_ip = "18.217.31.126"
    server_port = 12345  # Change this to your server's port
    thread = threading.Thread(target=udp_sender_thread, args=(ser, server_ip, server_port))
    thread.daemon = True
    thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()

