#!/usr/bin/env python3
"""
Growatt2MQTT - Refactored Main Service
Reads Growatt Inverter Data via Modbus RTU and publishes to MQTT.
"""

import time
import os
import json
import logging
import sys
import argparse
from configparser import RawConfigParser
from typing import List, Dict, Any, Optional

import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

# Import our new Inverter class
from growatt import Growatt

# --- Constants ---
SETTINGS_READ_INTERVAL_CYCLES = 60  # Read settings every X cycles (e.g. 60 * 10s = 10 Min)
DEFAULT_CONFIG_PATH = 'growatt2mqtt.cfg'


class GrowattService:
    """
    Main Service class to control Growatt communication.
    """

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.settings = None
        # Internals
        self.client_modbus = None
        self.client_mqtt = None
        self.mqtt_props = None
        self.inverters: List[Dict[str, Any]] = [] 
        # Logger Setup
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.log = logging.getLogger('GrowattService')
        # Load Configuration immediately
        self._load_config()

    def _load_config(self):
        """Reads the configuration file."""
        if not os.path.exists(self.config_path):
            self.log.fatal(f"Config file not found: {self.config_path}")
            sys.exit(1)
        self.settings = RawConfigParser()
        self.settings.read(self.config_path)
        # Set Log Level
        log_level_str = self.settings.get('general', 'log_level', fallback='INFO').upper()
        self.log.setLevel(logging.getLevelName(log_level_str))
        self.log.info(f"Configuration loaded from {self.config_path}")

    def _setup_modbus(self):
        """Initializes the RS485 Modbus connection."""
        port = self.settings.get('serial', 'port', fallback='/dev/ttyUSB0')
        baud = self.settings.getint('serial', 'baudrate', fallback=9600)
        self.log.info(f"Connecting to Modbus RTU on {port} ({baud} baud)...")
        self.client_modbus = ModbusClient(
            method='rtu',
            port=port,
            baudrate=baud,
            stopbits=1,
            parity='N',
            bytesize=8,
            timeout=3
        )
        if not self.client_modbus.connect():
            self.log.error("Failed to connect to Modbus interface!")
            # We don't exit hard here, allowing the loop to retry later
        else:
            self.log.info("Modbus connection established.")

    def _setup_mqtt(self):
        """Initializes the MQTT connection."""
        host = self.settings.get('mqtt', 'host', fallback='localhost')
        port = self.settings.getint('mqtt', 'port', fallback=1883)
        self.mqtt_topic = self.settings.get('mqtt', 'topic', fallback='inverter/growatt')
        self.mqtt_error_topic = self.settings.get('mqtt', 'error_topic', fallback='inverter/growatt/error')
        self.log.info(f"Connecting to MQTT Broker at {host}:{port}...")
        self.client_mqtt = mqtt.Client()
        self.client_mqtt.on_connect = self._on_mqtt_connect
        self.client_mqtt.on_disconnect = self._on_mqtt_disconnect
        try:
            self.client_mqtt.connect(host, port, 60)
            self.client_mqtt.loop_start()  
            # MQTT v5 Properties (optional, if supported by broker)
            self.mqtt_props = Properties(PacketTypes.PUBLISH)
            self.mqtt_props.MessageExpiryInterval = 30
        except Exception as e:
            self.log.fatal(f"Failed to connect to MQTT Broker: {e}")
            sys.exit(1)

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.log.info("MQTT connected successfully.")
        else:
            self.log.error(f"MQTT connection failed with code {rc}")

    def _on_mqtt_disconnect(self, client, userdata, rc):
        self.log.warning(f"MQTT disconnected (rc={rc})")

    def _init_inverters(self):
        """Creates instances of the Growatt class based on config."""
        self.inverters = []
        for section in self.settings.sections():
            if not section.startswith('inverters.'):
                continue

            name = section.split('.', 1)[1] # e.g. "main" from "inverters.main"
            unit = self.settings.getint(section, 'unit')
            model = self.settings.get(section, 'protocol_version') # e.g. "TL-XH"
            measurement = self.settings.get(section, 'measurement')

            self.log.info(f"Initializing Inverter '{name}' (Unit: {unit}, Model: {model})")
            
            # Using the new signature from growatt.py
            inverter_obj = Growatt(self.client_modbus, name, unit, model)
            
            self.inverters.append({
                'obj': inverter_obj,
                'measurement': measurement,
                'error_sleep': 0,
                'cycles_since_settings': 999  # Force immediate read on start
            })

    def run(self):
        """Main loop of the service."""
        self._setup_modbus()
        self._setup_mqtt()
        self._init_inverters()

        interval = self.settings.getint('time', 'interval', fallback=10)
        offline_interval = self.settings.getint('time', 'offline_interval', fallback=60)
        error_interval = self.settings.getint('time', 'error_interval', fallback=60)

        self.log.info("Starting main loop...")

        while True:
            any_inverter_online = False
            start_time = time.time()

            for item in self.inverters:
                inv: Growatt = item['obj']
                
                # Check error backoff
                if item['error_sleep'] > 0:
                    item['error_sleep'] -= interval
                    continue

                try:
                    # 1. Read Live Data
                    data = inv.update()
                    
                    if not data:
                        # No data (Inverter offline or Com error)
                        continue
                    
                    any_inverter_online = True
                    
                    # 2. Read Settings / Holding Registers (Interval based)
                    item['cycles_since_settings'] += 1
                    if item['cycles_since_settings'] >= SETTINGS_READ_INTERVAL_CYCLES*10:  #every 10 minutes
                        settings = inv.read_settings()  # The new method from growatt.py
                        if settings:
                            self._publish(f"{self.mqtt_topic}/settings", settings, retain=True)
                            self.log.debug(f"Published settings for {inv.name}")
                        item['cycles_since_settings'] = 0

                    # 3. Prepare and Send Data
                    payload = {
                        'time': int(time.time()),
                        'measurement': item['measurement'],
                        'fields': data
                    }
                    
                    self.log.info(f"Data received from {inv.name}: {len(data)} registers")
                    self.log.debug(f"Payload: {data}")
                    
                    self._publish(self.mqtt_topic, payload)

                except Exception as e:
                    self.log.error(f"Error processing inverter {inv.name}: {e}")
                    # Send Error Payload
                    error_payload = {
                        "name": inv.name,
                        "error": str(e)
                    }
                    self._publish(self.mqtt_error_topic, error_payload)
                    item['error_sleep'] = error_interval

            # Sleep Logic
            sleep_time = interval if any_inverter_online else offline_interval
            
            # Calculate actual sleep time (subtracting processing time)
            elapsed = time.time() - start_time
            actual_sleep = max(0.1, sleep_time - elapsed)
            
            time.sleep(actual_sleep)

    def _publish(self, topic: str, payload: dict, retain: bool = False):
        """Helper method to safely publish JSON."""
        try:
            json_str = json.dumps(payload, default=str)
            self.client_mqtt.publish(
                topic, 
                json_str, 
                qos=0, 
                retain=retain, 
                properties=self.mqtt_props
            )
        except Exception as e:
            self.log.error(f"Failed to publish MQTT message: {e}")

def main():
    parser = argparse.ArgumentParser(description='Growatt2MQTT Service')
    parser.add_argument('-c', '--config', default=DEFAULT_CONFIG_PATH, help='Path to config file')
    args = parser.parse_args()

    print("""
   ____                        _   _   ____  __  __  ___ _____ _____ 
  / ___|_ __ _____      ____ _| |_| |_|___ \|  \/  |/ _ \_   _|_   _|
 | |  _| '__/ _ \ \ /\ / / _` | __| __| __) | |\/| | | | || |   | |  
 | |_| | | | (_) \ V  V / (_| | |_| |_ / __/| |  | | |_| || |   | |  
  \____|_|  \___/ \_/\_/ \__,_|\__|\__|_____|_|  |_|\__\_\|_|   |_|  
    """)

    service = GrowattService(config_path=args.config)
    
    try:
        service.run()
    except KeyboardInterrupt:
        print("\nStopping service (KeyboardInterrupt)...")
        sys.exit(0)


if __name__ == "__main__":
    main()