#!/usr/bin/env python3
"""
Main module for Growatt ModBus RTU data to MQTT
"""
import time
import os
import json
import logging
import sys
from configparser import RawConfigParser
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

from growatt import Growatt
__logo = """
   ____                        _   _   ____  __  __  ___ _____ _____ 
  / ___|_ __ _____      ____ _| |_| |_|___ \|  \/  |/ _ \_   _|_   _|
 | |  _| '__/ _ \ \ /\ / / _` | __| __| __) | |\/| | | | || |   | |  
 | |_| | | | (_) \ V  V / (_| | |_| |_ / __/| |  | | |_| || |   | |  
  \____|_|  \___/ \_/\_/ \__,_|\__|\__|_____|_|  |_|\__\_\|_|   |_|  
                                                                      
    """


class Growatt2MQTT:
    """
    Main class, implementing the Growatt to MQTT functionality
    """
    # Global variables, defined private, all variables will be configured via cfg file
    # settings --> from config file
    __settings = None
    # interval in seconds for pulling modbus data [s]
    __interval = None
    # in case inverter is offline the script will sleep that defined time [s]
    __offline_interval = None
    # error interval in [s]
    __error_interval = None
    # device name of serial usb connection [/dev/tty...]
    __port = None
    # baudrate to access modbus connection
    __baudrate = -1
    # modbus client handle
    __client = None
    # mqtt server host address
    __mqtt_host = None
    # mqtt client handle
    __mqtt_client = None
    # mqtt port of mqtt broker
    __mqtt_port = -1
    # mqtt topic the inverter data will be published
    __mqtt_topic = ""
    # mqtt error topic in case the growatt2mqtt runs in error moder or inverter is powered off
    __mqtt_error_topic = ""
    # mqtt properties handle for publishing data
    __properties = None
    # logging module
    __log = None
    # log level, available log levels are CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG
    __log_level = 'DEBUG'

    def __init__(self):
        self.__log = logging.getLogger('growatt2mqqt_log')
        handler = logging.StreamHandler(sys.stdout)
        self.__log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s]  {%(filename)s:%(lineno)d}  %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.__log.addHandler(handler)
        return None

    def init_growatt2mqtt(self):
        """
        initialize growatt 2 mqtt
        """
        self.__log.info("Initialize growatt2mqtt")
        self.__settings = RawConfigParser()
        self.__settings.read(os.path.dirname(
            os.path.realpath(__file__)) + '/growatt2mqtt.cfg')
        self.__interval = self.__settings.getint(
            'time', 'interval', fallback=1)
        self.__offline_interval = self.__settings.getint(
            'time', 'offline_interval', fallback=60)
        self.__error_interval = self.__settings.getint(
            'time', 'error_interval', fallback=60)
        self.__log_level = self.__settings.get('general','log_level', fallback='DEBUG')
        if (self.__log_level != 'DEBUG'):
            self.__log.setLevel(logging.getLevelName(self.__log_level))
        self.__log.info('Setup Serial Connection... ')
        self.__port = self.__settings.get(
            'serial', 'port', fallback='/dev/ttyUSB0')
        self.__baudrate = self.__settings.get(
            'serial', 'baudrate', fallback=9600)
        self.__client = ModbusClient(method='rtu', port=self.__port, baudrate=int(
            self.__baudrate), stopbits=1, parity='N', bytesize=8, timeout=1)
        self.__client.connect()
        self.__log.info('Serial connection established...')

        self.__log.info("start connection mqtt ...")
        self.__mqtt_host = self.__settings.get(
            'mqtt', 'host', fallback='mqtt.eclipseprojects.io')
        self.__mqtt_port = self.__settings.get('mqtt', 'port', fallback=1883)
        self.__mqtt_topic = self.__settings.get(
            'mqtt', 'topic', fallback='home/inverter')
        self.__mqtt_error_topic = self.__settings.get(
            'mqtt', 'error_topic', fallback='home/inverter/error')
        self.__log.info("mqtt settings: \n")
        self.__log.info("mqtt host %s\n", self.__mqtt_host)
        self.__log.info("mqtt port %s\n", self.__mqtt_port)
        self.__log.info("mqtt_topic %s\n", self.__mqtt_topic)
        self.__mqtt_client = mqtt.Client()
        self.__mqtt_client.on_connect = self.on_connect
        self.__mqtt_client.on_message = self.on_message

        self.__mqtt_client.connect(
            str(self.__mqtt_host), int(self.__mqtt_port), 60)
        self.__mqtt_client.loop_start()

        self.__properties = Properties(PacketTypes.PUBLISH)
        self.__properties.MessageExpiryInterval = 30  # in seconds

    def on_connect(self, client, userdata, flags, rc):
        """ The callback for when the client receives a CONNACK response from the server. """
        self.__log.info("Connected with result code %s\n",str(rc))

    def on_message(self, client, userdata, msg):
        """ The callback for when a PUBLISH message is received from the server. """
        self.__log.info(msg.topic+" "+str(msg.payload))

    def run(self):
        """
        run method, starts ModBus connection and mqtt connection
        """
        self.__log.info('Loading inverters... ')
        inverters = []
        for section in self.__settings.sections():
            if not section.startswith('inverters.'):
                continue

            name = section[10:]
            unit = int(self.__settings.get(section, 'unit'))
            protocol_version = str(
                self.__settings.get(section, 'protocol_version'))
            measurement = self.__settings.get(section, 'measurement')
            #growatt = Growatt(self.__client, name, unit, protocol_version, self.__log)
            growatt = Growatt(self.__client, name, unit, protocol_version, self.__log)
            growatt.print_info()
            inverters.append({
                'error_sleep': 0,
                'growatt': growatt,
                'measurement': measurement
            })
        self.__log.info('Done!')

        while True:
            online = False
            for inverter in inverters:
                # If this inverter errored then we wait a bit before trying again
                if inverter['error_sleep'] > 0:
                    inverter['error_sleep'] -= self.__interval
                    continue

                growatt = inverter['growatt']
                try:
                    now = time.time()
                    info = growatt.update()

                    if info is None:
                        continue

                    # Mark that at least one inverter is online so we should continue collecting data
                    online = True

                    points = [{
                        'time': int(now),
                        'measurement': inverter['measurement'],
                        "fields": info
                    }]
                    self.__log.info(points)
                    # Serializing json
                    json_object = json.dumps(points[0], indent=4)

                    self.__mqtt_client.publish(
                        self.__mqtt_topic, json_object, 0, properties=self.__properties)

                except Exception as err:
                    self.__log.error(growatt.name)
                    self.__log.error(err)
                    json_object = '{"name":' + \
                        str(growatt.name)+',error_code:'+str(err)+'}'
                    self.__mqtt_client.publish(
                        self.__mqtt_error_topic, json_object, 0, properties=self.__properties)
                    inverter['error_sleep'] = self.__error_interval

            if online:
                time.sleep(self.__interval)
            else:
                # If all the inverters are not online because no power is being generated then we sleep for 1 min
                time.sleep(self.__offline_interval)


def main():
    """
    main method
    """
    print(__logo)
    my_growatt2mqtt = Growatt2MQTT()
    my_growatt2mqtt.init_growatt2mqtt()
    my_growatt2mqtt.run()


if __name__ == "__main__":
    main()
