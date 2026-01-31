# growatt2mqtt

Growatt2MQTT is a Python-based service that connects to the Modbus interface (RS485/USB) of Growatt inverters, reads specific registers based on the inverter model, and publishes the collected data to an MQTT broker.

**New:** The project has been refactored to support a wide range of inverter series (including Hybrid and Storage systems like SPH, SPA, and TL-XH) through modular register maps.

## Features

- Reads Input Registers (and optionally Holding Registers) via Modbus RTU.
- **Modular Architecture:** Supports different inverter types by selecting a `protocol_version`.
- Retrieves PV data, Grid data, Battery status (SOC, power), and BMS information.
- Configurable via `growatt2mqtt.cfg`.
- Can run as a Linux Systemd service or inside a Docker container.

## Configuration (`growatt2mqtt.cfg`)

Configuration is handled via the `growatt2mqtt.cfg` file. You must set the `protocol_version` to match your specific hardware.

### Example Configuration

```ini
[time]
# Data polling interval in seconds
interval = 10
# Time to sleep if inverter is offline (e.g., at night for PV-only systems)
offline_interval = 60
# Time to sleep after a communication error
error_interval = 60

[serial]
# Path to your USB-RS485 adapter
port = /dev/ttyUSB0
baudrate = 9600

[inverters.main]
unit = 1
measurement = inverter
# IMPORTANT: Select the correct protocol for your device (see table below)
# Options: TL3X, TL-X, TL-XH, TL-XH-MIN, MAX, MIX, SPH, SPA
protocol_version = TL-XH

[general]
# Options: DEBUG, INFO, WARNING, ERROR
log_level = INFO

[mqtt]
host = 192.168.1.100
port = 1883
topic = inverter/growatt/solar
error_topic = inverter/growatt/solar/error
```

## Supported Inverters (protocol_version)

Use one of the following shortcodes in your config file to load the correct register map:

| Shortcode | Description / Compatible Series | Covered Registers |
| :---------| :--------------------------- | :---------------- |
| TL3X      | Standard PV Inverters (MIC, MIN, MAC, TL-X, TL3-X) | Basic Data (0-124), Strings/PID (125-249) |
| TL-XH     | "Battery Ready" Hybrid Systems (High Voltage) | Inverter (3000-3124), Battery/BDC (3125-3249) |
|TL-XH-MIN	| MIN TL-XH Series (US/Global Single Phase Hybrid)	| Inverter (3000+), Battery 1 (3125+), Battery 2 (3250+)|
|SPH	| SPH 3000-6000 Hybrid Inverters	|Basic (0-124), Hybrid Data (1000-1124), Extended (1125+)|
|SPA	|AC-Coupled Storage Retrofit (e.g., SPA 3000TL BL)	|Hybrid (1000-1124), Extended (1125+), AC-Grid (2000+)|
|MIX	|MIX / SPH Series (Alternative Layout)	|Basic (0-124), Storage/Energy Flow (1000-1124)|
|MAX	|Commercial Inverters (MAX 1500V / MAX-X LV)	|Basic (0-124), Strings 1-16 (125-249), Strings 17-32 (875-999)|
| MOD-XH | MOD TL3-XH Series (3-Phase Battery Ready Hybrid) | Inverter (3000-3124), Battery/BDC (3125-3249) |
| EASTRON | Eastron SDM630 Smart Meter (Direct RS485 Connection) | Voltage/Amps (0-50), Power/Energy (52-80, 342) |
| CHINT | Chint DTSU666 Smart Meter (Direct RS485 Connection) | Voltage/Amps (8192+), Power/Energy (8212+, 16384+) |

Note: If you are unsure, start with TL3X for pure PV inverters or TL-XH for modern battery-ready systems.

## Installation
### Prerequisites

Python 3.x

A USB to RS485 adapter connected to the inverter's Modbus interface.

### Install Dependencies
```bash
pip3 install -r requirements.txt
# Or manually:
pip3 install pymodbus paho-mqtt configparser
```

### Run Manually
```bash
python3 growatt2mqtt.py
```

### Run as Linux Service (Systemd)

1. Copy the service file:
```bash
sudo cp growatt2mqtt.service /etc/systemd/system/
```

2. Edit the service file to match your installation path if necessary.

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable growatt2mqtt.service
sudo systemctl start growatt2mqtt.service
```

4. Check status:
```bash
systemctl status growatt2mqtt.service
```

## Run with Docker

1. Build the image:
```bash
docker build -t growatt2mqtt .
```
2. Run the container (ensure you pass the correct device path):
```bash
docker run --device=/dev/ttyUSB0:/dev/ttyUSB0 -v $(pwd)/growatt2mqtt.cfg:/app/growatt2mqtt.cfg growatt2mqtt
```

## Project Structure
+ growatt2mqtt.py: Main entry point. Handles config parsing, Modbus connection loop, and MQTT publishing.

+ growatt.py: Inverter logic class. Dynamically imports the correct register map based on the configured model.

+ register_maps/: Directory containing the specific register definitions (e.g., growatt_TLXH_input_reg.py, growatt_SPH_input_reg.py).

+ growatt2mqtt.cfg: User configuration file.

## Troubleshooting
If you receive no data or errors:

+ Check your wiring (A to A, B to B on RS485).

+ Verify the unit ID (default is often 1).

+ Set log_level = DEBUG in growatt2mqtt.cfg to see raw Modbus frames and parser outputs.

## Compatibility
Currently the code is tested for the following models: 
| Model | Compatibility | Covered Registers |
| :---------| :--------------------------- | :---------------- |
| Growatt MOD 5000TL3-XH |  &#x2611; | Input Reg / Holding Reg |
| Growatt MIC 600TL-X | &#x2612;| to be confirmed |
