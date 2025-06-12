import time
import logging

from gpiozero import DigitalInputDevice, OutputDevice  # Import the gpiozero library to interact with GPIO pins

# Set up basic configuration for logging
logging.basicConfig(
    filename='app.log',        # Log will be saved in 'app.log'
    level=logging.DEBUG,       # Log all messages with severity level DEBUG or higher
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    filemode='a'               # Ensure that logs are appended to the file (not overwritten)
)

# Set up GPIO pin 27 as an OUTPUT pin for controlling the pump relay
relay_pin = 27 # Connect relay on pin 13
relayCarbPump = OutputDevice(relay_pin, active_high=False)

# Set up GPIO pin 17 as an INPUT pin for the flow sensor signal
signal_pin = 17  # The GPIO pin connected to the flow sensor PIN 11
pulses_per_liter = 450  # Set this to the correct value based on your flow sensor's datasheet

# Create an instance of the DigitalInputDevice to monitor the flow sensor's pulses
flow_sensor = DigitalInputDevice(signal_pin, pull_up=True)  # Using pull-up resistor

pulse_count = 0  # Variable to keep track of the pulses detected by the sensor
total_volume = 0.0  # Total volume in liters (accumulates over time)

# Define the function to handle the pulse detection event
def on_pulse():
    """Callback function to increment pulse count whenever a pulse is detected."""
    global pulse_count
    pulse_count += 1  # Increment pulse count each time the flow sensor is activated
    print(f"Pulse count: {pulse_count}")

# Bind the on_pulse function to be called when a pulse is detected
flow_sensor.when_activated = on_pulse

# Function to monitor flow rate continuously
def monitor_flow_rate(duration=60, interval=10):
    """Monitor flow rate continuously and control the pump relay for the given duration."""
    global pulse_count, total_volume

    try:
        while True:
            relayCarbPump.on()  # Turn on the pump relay
            time.sleep(1)  # Wait for 1 second to allow the pump to stabilize

            pulse_count = 0  # Reset pulse count for the next cycle
            start_time = time.time()  # Start measuring the time for this cycle

            # Sleep for the duration of the cycle
            time.sleep(duration)

            end_time = time.time()  # End the cycle after the specified duration
            elapsed_time = end_time - start_time  # Calculate how much time has passed

            # Calculate flow rate: pulses per liter divided by elapsed time, then convert to L/min
            flow_rate = (pulse_count / pulses_per_liter) / elapsed_time * 60  # L/min
            # Calculate volume: number of pulses divided by pulses per liter
            volume = pulse_count / pulses_per_liter
            total_volume += volume  # Accumulate the total volume over time

            msg = f"PULSE COUNT IN: {elapsed_time:.2f}s: {pulse_count}"
            
            print(msg)
            logging.debug(msg)

            relayCarbPump.off()
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Stopped by user.")  # Handle user interrupt (Ctrl+C) to stop the program
    except Exception as e:
        print(f"Error: {e}")  # Print any errors that occur during execution
    finally:
        # Clean up: turn off the relay and close the flow sensor
        relayCarbPump.off()  # Turn off the pump relay
        flow_sensor.close()  # Close the flow sensor properly

# Call the monitor_flow_rate function with a 1-second duration for flow rate calculation
monitor_flow_rate(duration=3, interval=2)
