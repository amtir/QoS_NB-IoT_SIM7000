import RPi.GPIO as GPIO
import time
import argparse

# Pin configuration
GPIO_PIN = 4  # BCM pin 4 corresponds to physical pin 7

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT, initial=GPIO.LOW)

# Routine to set the state to low for 1300ms and then high
def power_on_off():
    #GPIO.output(GPIO_PIN, GPIO.LOW)
    #time.sleep(2.0)  # Wait for 1300ms
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(1.2)  # Wait for 1300ms
    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(2.0)

# Routine to ensure the state is low for at least 200ms and then high
def power_off():
    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(0.2)  # Wait for at least 200ms
    GPIO.output(GPIO_PIN, GPIO.HIGH)


# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description='Control GPIO pin state for SIM7000E power management.')
    parser.add_argument('method', choices=['power_on', 'power_off'], 
                        help='Method to run: power_on or power_off')
    
    args = parser.parse_args()

    if args.method == 'power_on':
        print("Power on SIM7000E.")
        power_on_off()
    elif args.method == 'power_off':
        print("Power off SIM7000E.")
        power_on_off()

if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()  # Reset GPIO settings

