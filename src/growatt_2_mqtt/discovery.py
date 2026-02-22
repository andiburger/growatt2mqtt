#!/usr/bin/env python3
import json
import logging

log = logging.getLogger(__name__)


class HADiscoveryManager:
    """
    Handles Home Assistant MQTT Auto-Discovery.
    Guesses sensor types based on their register names to make it plug & play.
    """
    def __init__(self, mqtt_client, base_topic):
        """
        Docstring for __init__
        
        :param self: Description
        :param mqtt_client: Description
        :param base_topic: Description
        """
        self.mqtt = mqtt_client
        self.base_topic = base_topic
        self.ha_status = "online"  # Assume HA is online at start (it will correct us if not)
        # Keeps track of published components to avoid spamming the broker
        self.published_components = set()

    def set_ha_status(self, status):
        """Called when Home Assistant sends its online/offline status.
        :param status: 'online' or 'offline'"""
        status = status.lower()
        if status != self.ha_status:
            log.info(f"Home Assistant status changed to: {status}")
            self.ha_status = status
            if status == "online":
                # HA restarted, we need to republish all discovery messages
                self.published_components.clear()

    def _guess_sensor_properties(self, key):
        """
        Infers the unit, device class, and state class from the sensor's name.
        :param key: The name of the sensor (e.g. 'Pac', 'Vpv1', 'FaultCode')
        :return: tuple (unit_of_measurement, device_class, state_class)
        """
        key_upper = key.upper()
        
        # 1. Text/Status Sensors (No unit, no measurement class)
        if any(x in key_upper for x in ["STATUS", "MODE", "FAULT", "CODE", "TEXT", "DERATING", "WARNING"]):
            return None, None, None
            
        # 2. Numeric Sensors
        if key_upper.startswith("P") or "POWER" in key_upper:
            return "W", "power", "measurement"
        if key_upper.startswith("E") or "ENERGY" in key_upper or "TODAY" in key_upper or "TOTAL" in key_upper:
            return "kWh", "energy", "total_increasing"
        if key_upper.startswith("V") and "VERSION" not in key_upper:
            return "V", "voltage", "measurement"
        if key_upper.startswith("I"):
            return "A", "current", "measurement"
        if key_upper.startswith("F") or "FREQ" in key_upper:
            return "Hz", "frequency", "measurement"
        if "TEMP" in key_upper or "TINV" in key_upper:
            return "°C", "temperature", "measurement"
        if "SOC" in key_upper:
            return "%", "battery", "measurement"
        if "TIME" in key_upper:
            return "s", "duration", "total_increasing"
            
        # Generic fallback for unknown numbers
        return None, None, "measurement"

    def publish_discovery(self, inverter_name, model, sensor_keys, is_settings=False):
        """
        Publishes HA Auto-Discovery config. 
        Differentiates between live sensors (read-only) and settings (read/write),
        which are created as interactive switches or number sliders in Home Assistant.
        :param inverter_name: Name of the inverter
        :param model: Model of the inverter
        :param sensor_keys: List of sensor keys to publish
        :param is_settings: If True, creates interactive components (switches/sliders) for settings; otherwise, creates read-only sensors for live data.
        """
        # If set to offline, we just silently return (no logging)
        if self.ha_status != "online":
            return
            
        # Prevent spamming the MQTT broker if already published
        cache_key = f"{inverter_name}_{'settings' if is_settings else 'live'}"
        if cache_key in self.published_components:
            return
            
        log.info(f"Publishing HA Auto-Discovery for '{inverter_name}' ({'Settings' if is_settings else 'Live Data'})...")
        safe_name = inverter_name.replace(" ", "_").lower()
        
        # Device information to group all sensors under one device in HA
        device_info = {
            "identifiers": [f"growatt_{safe_name}"],
            "name": f"Growatt {inverter_name}",
            "manufacturer": "Growatt",
            "model": model
        }
        
        count = 0
        for key in sensor_keys:
            payload = {}
            component = "sensor"  # Default to read-only sensor
            
            # ==========================================
            # CASE 1: HOLDING REGISTERS (WRITABLE)
            # ==========================================
            if is_settings:
                state_topic = f"{self.base_topic}/settings"
                
                # A: Is it a switch? (e.g., "ACChargeEnable" or "OnOff")
                if any(x in key.upper() for x in ["ENABLE", "ONOFF"]):
                    component = "switch"
                    
                    # HA expects ON/OFF states for switches, but Modbus uses 1/0
                    val_template = f"{{% if value_json.{key} == 1 %}}ON{{% else %}}OFF{{% endif %}}"
                    
                    payload = {
                        "name": f"{inverter_name} {key}",
                        "unique_id": f"growatt_{safe_name}_{key.lower()}",
                        "state_topic": state_topic,
                        "value_template": val_template,
                        # The topic where HA sends the command
                        "command_topic": f"{self.base_topic}/set",
                        # Translate HA's "ON/OFF" back into our custom JSON command format
                        "command_template": f'{{"command": "{key}", "value": {{% if value == "ON" %}}1{{% else %}}0{{% endif %}} }}',
                        "device": device_info
                    }
                
                # B: Is it a number / slider? (e.g., Power limits or percentages)
                else:
                    component = "number"
                    val_template = f"{{{{ value_json.{key} }}}}"
                    
                    payload = {
                        "name": f"{inverter_name} {key}",
                        "unique_id": f"growatt_{safe_name}_{key.lower()}",
                        "state_topic": state_topic,
                        "value_template": val_template,
                        "command_topic": f"{self.base_topic}/set",
                        # Send the new slider value as a JSON command
                        "command_template": f'{{"command": "{key}", "value": {{{{ value }}}} }}',
                        "device": device_info
                    }
                    
                    # Set smart limits for specific sliders to prevent invalid Modbus writes
                    if "Rate" in key or "Limit" in key:
                        payload["min"] = 0
                        payload["max"] = 100
                    elif "Time" in key or "Hour" in key:
                        payload["min"] = 0
                        payload["max"] = 23
                    elif "Min" in key:
                        payload["min"] = 0
                        payload["max"] = 59
            
            # ==========================================
            # CASE 2: INPUT REGISTERS (READ-ONLY)
            # ==========================================
            else:
                component = "sensor"
                state_topic = self.base_topic
                val_template = f"{{{{ value_json.fields.{key} }}}}"
                
                # Guess units and HA classes based on the sensor name
                unit, dev_class, state_class = self._guess_sensor_properties(key)
                
                payload = {
                    "name": f"{inverter_name} {key}",
                    "unique_id": f"growatt_{safe_name}_{key.lower()}",
                    "state_topic": state_topic,
                    "value_template": val_template,
                    "device": device_info
                }
                
                # Only append attributes if they were successfully guessed
                if unit: payload["unit_of_measurement"] = unit
                if dev_class: payload["device_class"] = dev_class
                if state_class: payload["state_class"] = state_class

            # ==========================================
            # PUBLISH TO HOME ASSISTANT
            # ==========================================
            config_topic = f"homeassistant/{component}/{safe_name}/{key.lower()}/config"
            self.mqtt.publish(config_topic, json.dumps(payload), retain=True)
            count += 1
            
        self.published_components.add(cache_key)
        log.info(f"Successfully published {count} discovery {component}s for '{inverter_name}'.")