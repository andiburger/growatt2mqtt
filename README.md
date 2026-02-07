# growatt2mqtt --- A Python-based Growatt Modbus MQTT Bridge (Read & Write)

A Python-based bridge to communicate with Growatt Inverters (specifically **MOD TL3-XH**) via Modbus RS485 and publish data to MQTT. 

Unlike simple monitoring scripts, this project supports **writing to holding registers**, allowing you to control battery limits and AC charging via Home Assistant.

## Features

* 📡 **Live Monitoring:** Reads PV power, Grid voltage, Battery status (SOC, Power), and Load consumption.
* 🎛️ **Control:** Allows writing to registers to control Battery Charge/Discharge limits and AC Charging.
* 📦 **Modern Packaging:** Easy installation via `pip` or `Docker`.
* 🏠 **Home Assistant Ready:** Optimized for easy integration with HA automation.
* 🔧 **MOD TL3-XH Optimized:** Uses the correct register map (3000+ range) for newer firmware versions.

---

## 🚀 Installation

### Option A: Python Package (Recommended for Raspberry Pi)

You can install the package directly from the source.

```bash
# 1. Clone repository
git clone [https://github.com/YOUR_USER/growatt-mqtt-bridge.git](https://github.com/YOUR_USER/growatt-mqtt-bridge.git)
cd growatt-mqtt-bridge

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# 2. Install package
pip install .

# 3. Setup configuration
cp config.cfg.example growatt.cfg
nano growatt.cfg  # <-- Edit MQTT IP and Serial Port here

# 4. Run
growatt-run -c growatt.cfg
```

### Option B: Docker

A Dockerfile is included to run the bridge in an isolated environment.

```bash
# 1. Build Image
docker build -t growatt-bridge .

# 2. Run Container
# Note: You must map the USB device and the config file!
docker run -d \
  --name growatt \
  --restart unless-stopped \
  --device /dev/ttyUSB0:/dev/ttyUSB0 \
  -v $(pwd)/growatt.cfg:/config/growatt.cfg \
  growatt-bridge
```


## ⚙️ Configuration
Configuration is handled via the growatt2mqtt.cfg file.

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
port = /dev/ttyUSB0
baudrate = 9600

[mqtt]
host = 192.168.1.10
port = 1883
topic = inverter/growatt
user = mqtt_user
password = mqtt_pass

[inverters.main]
unit = 1
# Important for MOD TL3-XH: Use the XH specific protocol
protocol_version = TL-XH
```

## 🏠 Home Assistant Integration
To control the inverter (e.g., stop battery discharge when your EV is charging), add the following configuration to your configuration.yaml in Home Assistant.

```yaml
mqtt:
  number:
    # Control Battery Discharge Limit (0-100%)
    - name: "Growatt Discharge Limit"
      unique_id: growatt_bat_discharge_limit
      command_topic: "inverter/control/BatDischargePowerLimit"
      state_topic: "inverter/growatt/solar/MOD5000TL3-XH"
      value_template: "{{ value_json.fields.BatDischargePowerLimit }}"
      min: 0
      max: 100
      mode: slider
      unit_of_measurement: "%"

    # Control Battery Charge Limit (0-100%)
    - name: "Growatt Charge Limit"
      unique_id: growatt_bat_charge_limit
      command_topic: "inverter/control/BatChargePowerLimit"
      state_topic: "inverter/growatt/solar/MOD5000TL3-XH"
      value_template: "{{ value_json.fields.BatChargePowerLimit }}"
      min: 0
      max: 100
      mode: slider
      unit_of_measurement: "%"

  switch:
    # Enable/Disable AC Charging (Grid Charging)
    - name: "Growatt AC Charge"
      unique_id: growatt_ac_charge_enable
      command_topic: "inverter/control/ACChargeEnable"
      state_topic: "inverter/growatt/solar/MOD5000TL3-XH"
      value_template: "{{ value_json.fields.ACChargeEnable }}"
      payload_on: "1"
      payload_off: "0"
      state_on: 1
      state_off: 0
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
