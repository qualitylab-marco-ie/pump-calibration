import time
from gpiozero import DigitalInputDevice, OutputDevice

relay_pin = 27
relayCarbPump = OutputDevice(relay_pin)

signal_pin = 17
pulses_per_liter = 2775 # CHARLES

flow_sensor = DigitalInputDevice(signal_pin, pull_up=True)

pulse_count = 0
total_volume = 0.0  # Total volume in liters

def on_pulse():
    global pulse_count
    pulse_count += 1

flow_sensor.when_activated = on_pulse

def monitor_flow_rate(duration):
    """Monitor flow rate continuously and control the pump relay."""
    global pulse_count, total_volume

    try:
        relayCarbPump.on()
        time.sleep(1)  # Optional: allow pump to stabilize
        while True:
            pulse_count = 0
            start_time = time.time()

            time.sleep(duration)

            end_time = time.time()
            elapsed_time = end_time - start_time

            flow_rate = (pulse_count / pulses_per_liter) / elapsed_time * 60  # L/min
            volume = pulse_count / pulses_per_liter
            total_volume += volume

            print(f"Flow Rate: {flow_rate:.2f} L/min | Volume: {volume:.3f} L | Total Volume: {total_volume:.3f} L")
    except KeyboardInterrupt:
        print("Stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        relayCarbPump.off()
        flow_sensor.close()

monitor_flow_rate(1)
