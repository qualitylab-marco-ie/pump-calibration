# Raspberry Pi Flow Sensor Calibration Script

This script is designed to help you **calibrate your flow sensor** by determining the number of pulses per liter (`pulses_per_liter`). The script runs for 60 seconds, counts the pulses from the flow sensor, and calculates how many pulses correspond to 1 liter of liquid.

By running this calibration script, you will determine the `pulses_per_liter` value, which is crucial for accurate flow rate and volume calculations in your projects.

## Project Overview

This script listens for pulses from a **flow sensor** connected to your Raspberry Pi, counts how many pulses occur in 60 seconds, and then calculates the `pulses_per_liter`. This value is essential to accurately convert pulse counts into flow rate and volume.

### Key Features:

* **Pulse Counting**: Counts pulses from the flow sensor for a set period (60 seconds).
* **Relay Control**: Controls a relay to turn a pump on/off (optional, depending on your setup).
* **Easy Calibration**: Simple, straightforward way to calibrate the sensor for your specific system.

## Requirements

* **Hardware**:

  * Raspberry Pi (any model with GPIO support, such as Raspberry Pi 3 or 4).
  * Flow sensor
  * Relay module to control the pump
  * Jumper wires and breadboard for prototyping.

* **Software**:

  * Raspbian OS (or any Linux-based OS on Raspberry Pi).
  * Python 3.x.
  * `gpiozero` library for GPIO pin management.
  * `time` module for controlling flow timing.

## Setup

### 1. Install Required Libraries

You’ll need the `gpiozero` library to interact with GPIO pins.

To install `gpiozero`, run:

```bash
pip install gpiozero
```

### 2. Wiring the Hardware

* **Flow Sensor**:

  * Connect the **signal pin** of the flow sensor to GPIO pin 17 on the Raspberry Pi.
  * Connect **VCC** to 5V and **GND** to ground.

* **Relay** (Optional):

  * If you want to control a pump, connect the **relay control pin** to GPIO pin 27 on the Raspberry Pi.
  * Connect the **COM** terminal of the relay to the pump's power source, and the **NO** (Normally Open) terminal to the pump’s power line.

Make sure the relay can handle the voltage and current of the pump. This is optional for calibration and can be left out if only pulse counting is required.

### 3. Running the Calibration Script

* The script will run for **60 seconds**, counting pulses from the flow sensor. During this time, you should allow liquid to flow through the sensor.

* After the 60 seconds, the script will display:

  * The **total number of pulses** detected.
  * The **calculated value of pulses per liter**, based on the actual volume of liquid passed through the sensor during the calibration period.

### 4. Calculate `pulses_per_liter`

To calculate `pulses_per_liter`, use the following equation:

$$
\text{pulses\_per\_liter} = \frac{\text{Total Pulse Count in 60 Seconds}}{\text{Volume of Liquid in Liters}}
$$

Where:

* **Total Pulse Count in 60 Seconds** is the number of pulses detected during the 60-second measurement.
* **Volume of Liquid in Liters** is the amount of liquid passed through the sensor during this time (you'll need to measure this manually by using a known container with a specified volume).

For example, if the flow sensor detects **450 pulses** in 60 seconds while you are flowing **1 liter** of liquid through the sensor, the `pulses_per_liter` would be calculated as:

$$
\text{pulses\_per\_liter} = \frac{450}{1} = 450
$$

If you used **0.5 liters** for calibration, the calculation would be:

$$
\text{pulses\_per\_liter} = \frac{450}{0.5} = 900
$$

### 5. Example Output

When you run the calibration script, the output might look like this:

```
Starting flow sensor calibration...
Pulse count in 60 seconds: 450
```

After determining `pulses_per_liter`, you can update your main project code with this value to calculate flow rate and total volume accurately.

---

### Usage:

1. **Run the Script**: Execute the script with the following command:

```bash
python app.py
```

2. **Wait for Calibration**: Let the script run for 60 seconds. During this time, allow a known volume of liquid (e.g., 1 liter) to pass through the flow sensor.

3. **Get the Result**: The script will output the pulse count and calculate the `pulses_per_liter` value based on the number of pulses detected in 60 seconds.

---

## Conclusion

Once you have calibrated the sensor and calculated the `pulses_per_liter`, you can use this value in your main application code to accurately calculate flow rates and total volume.

---

Feel free to modify the script for your specific setup, especially if you're using a different flow sensor or need to adjust for a different calibration duration. Let me know if you need more details or help with the code!
