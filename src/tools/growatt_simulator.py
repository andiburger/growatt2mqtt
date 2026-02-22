#!/usr/bin/env python3
import logging
import threading
import time
import math
import argparse

from pymodbus.server import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSparseDataBlock

# --- Logging Setup ---
logging.basicConfig(format='%(asctime)s - %(levelname)s - Simulator: %(message)s', level=logging.INFO)
log = logging.getLogger()

# ==========================================
# 1. PROFILE
# ==========================================


# BaseProfile defines the structure for different inverter profiles, allowing us to simulate various models with specific register values and behaviors. Each profile can override the get_initial_registers method to set up its own initial state and the simulate_tick method to define how the registers should change over time, simulating real-world conditions.
class BaseProfile:
    """
    BaseProfile
    Base class for defining different inverter profiles. 
    Each profile can specify its own initial register values and simulation behavior.
    """
    name = "Base"
    
    def get_initial_registers(self):
        """
        Docstring for get_initial_registers
        
        :param self: Description
        """
        return {"ir": {}, "hr": {}}

    def simulate_tick(self, context, slave_id, step):
        """
        Docstring for simulate_tick
        
        :param self: Description
        :param context: Description
        :param slave_id: Description
        :param step: Description
        """
        pass


class Mic600Profile(BaseProfile):
    """Profile for Growatt MIC 600 TL-X, based on typical register values and behavior observed in real devices"""
    name = "mic600"

    def get_initial_registers(self):
        """
        Docstring for get_initial_registers
        
        :param self: Description
        """
        # dict for initial register values based on typical readings for a TL-X/MIC inverter
        ir = {
            0: 1,       # Status: 1 = Normal
            35: 6000,   # Pac (Aktuelle Leistung): 600.0 W
            37: 2300,   # Vac (Netzspannung): 230.0 V
            53: 50,     # E_Today: 5.0 kWh
            55: 12000,  # E_Total: 1200.0 kWh
            93: 350     # Temperatur: 35.0 °C
        }
        hr = {
            0: 1,       # On/Off
            3: 100      # Power Limit 100%
        }
        return {"ir": ir, "hr": hr}

    def simulate_tick(self, context, slave_id, step):
        """
        Docstring for simulate_tick
        
        :param self: Description
        :param context: Description
        :param slave_id: Description
        :param step: Description
        """
        new_power = int(5500 + 500 * math.sin(step))
        new_volt = int(2300 + 10 * math.sin(step * 0.5))
        
        context[slave_id].setValues(4, 35, [new_power])
        context[slave_id].setValues(4, 37, [new_volt])
        log.debug(f"[{self.name}] Updated: Power={new_power/10}W, Volt={new_volt/10}V")


class ModHybridProfile(BaseProfile):
    """Profile for hybrid inverters (e.g., TL-XH, TL-H) with battery and export limit features"""
    name = "mod_tlxh"

    def get_initial_registers(self):
        """
        Docstring for get_initial_registers
        
        :param self: Description
        """
        ir = {
            3000: 1,       # status 1 = Normal
            3004: 45000,   # Pac: 4500.0 W
            3125: 550,     # SOC Battery: 55.0%
            3144: 1        # battery status: 1 = Charging
        }
        hr = {
            3000: 1        # register for on/off control
        }
        return {"ir": ir, "hr": hr}

    def simulate_tick(self, context, slave_id, step):
        """
        Docstring for simulate_tick
        
        :param self: Description
        :param context: Description
        :param slave_id: Description
        :param step: Description
        """
        # simulates soc and power changes for a hybrid inverter
        new_soc = int(500 + 200 * math.sin(step * 0.1)) # SOC varies between 50% and 70%
        new_power = int(45000 + 2000 * math.cos(step))
        
        context[slave_id].setValues(4, 3004, [new_power])
        context[slave_id].setValues(4, 3125, [new_soc])
        log.debug(f"[{self.name}] Updated: Power={new_power/10}W, SOC={new_soc/10}%")


# registry for available profiles
PROFILES = {
    "mic600": Mic600Profile(),
    "tlxh": ModHybridProfile()
}

# ==========================================
# 2. SIMULATOR ENGINE
# ==========================================


class GrowattSimulator:
    """
    Docstring for GrowattSimulator
    """
    def __init__(self, profile: BaseProfile):
        """
        Docstring for __init__
        :param self: Description
        :param profile: Description
        :type profile: BaseProfile
        """
        self.profile = profile
        log.info(f"Initialisiere Simulator mit Profil: {self.profile.name}")
        
        regs = self.profile.get_initial_registers()
        
        # ModbusSparseDataBlock perfect for sparse register maps 
        store = ModbusSlaveContext(
            di=ModbusSparseDataBlock({0: 0}),
            co=ModbusSparseDataBlock({0: 0}),
            hr=ModbusSparseDataBlock(regs["hr"]),
            ir=ModbusSparseDataBlock(regs["ir"])
        )
        
        self.context = ModbusServerContext(slaves={1: store}, single=True)

    def update_loop(self):
        """
        Docstring for update_loop
        :param self: Description
        """
        step = 0
        while True:
            # the profile's simulate_tick method will update the register values based on the current step
            self.profile.simulate_tick(self.context, slave_id=1, step=step)
            step += 0.1
            time.sleep(2)

    def run(self, port, baudrate=9600):
        # start background thread for updating register values
        sim_thread = threading.Thread(target=self.update_loop, daemon=True)
        sim_thread.start()

        log.info(f"Starte seriellen Modbus Server auf {port}...")
        StartSerialServer(
            context=self.context,
            port=port,
            baudrate=baudrate,
            framer='rtu',
            stopbits=1,
            bytesize=8,
            parity='N'
        )

# ==========================================
# 3. START SCRIPT
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Growatt Modbus Simulator")
    parser.add_argument("port", help="Serieller Port (z.B. /dev/pts/4)")
    parser.add_argument("--profile", choices=PROFILES.keys(), default="mic600", help="Inverter Profil")
    parser.add_argument("--debug", action="store_true", help="Aktiviere Modbus Debug Logs")
    
    args = parser.parse_args()

    if args.debug:
        logging.getLogger("pymodbus").setLevel(logging.DEBUG)
        log.setLevel(logging.DEBUG)

    # load selected profile and start simulator
    selected_profile = PROFILES[args.profile]
    sim = GrowattSimulator(selected_profile)
    sim.run(args.port)