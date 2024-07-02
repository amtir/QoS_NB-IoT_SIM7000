import serial
import time

def send_at_command(ser, command, timeout=2):
    ser.write((command + '\r').encode())
    time.sleep(timeout)
    response = ser.read(ser.in_waiting).decode()
    return response

def main():
    status_machine = [0]

    try:
        ser = serial.Serial("/dev/ttyAMA0")
        ser.baudrate = 9600
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 2
        ser.flushOutput()
        
        print("Connected to Serial.")
        status_machine[0] = 1

        # Initialize connection
        print(send_at_command(ser, 'AT'))
        print(send_at_command(ser, 'AT+CSQ'))
        print(send_at_command(ser, 'AT+CREG?'))
        print(send_at_command(ser, 'AT+CGATT?'))
        print(send_at_command(ser, 'AT+CGDCONT=1,"IP","shared.m2m.ch"'))
        print(send_at_command(ser, 'AT+CSTT="shared.m2m.ch"'))
        print(send_at_command(ser, 'AT+CIICR'))
        print(send_at_command(ser, 'AT+CIFSR'))

        # Optionally, you can start a TCP connection and send data
        # server_ip = "your_server_ip"
        # port = "your_port"
        # print(send_at_command(ser, f'AT+CIPSTART="TCP","{server_ip}","{port}"'))
        # print(send_at_command(ser, 'AT+CIPSEND'))
        # print(send_at_command(ser, 'your data here' + chr(26)))

        ser.close()

    except Exception as e:
        print(f"Error: {e}")
        print("Not Connected: Error.")
        status_machine[0] = 0

if __name__ == "__main__":
    main()

