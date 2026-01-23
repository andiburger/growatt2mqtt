#!/usr/bin/env python3
"""
growatt.py

Refactored module for Modbus RTU communication with Growatt Inverters.
Supports TL-X, TL-XH, and other series via flexible register maps.
"""

import logging
import struct
import time
from pymodbus.exceptions import ModbusIOException

# --- Import Register Maps ---
# Ensure these files are located in the same directory.
# We use try-except to prevent crashes if a map file is missing.

# 1. TL-XH Series (Input Registers 3000-3249)
try:
    from register_maps.growatt_TLXH_input_reg import REG_INPUT_MAP as MAP_TLXH_3000
except ImportError:
    MAP_TLXH_3000 = {}
    logging.warning("Could not import growatt_input_3000. TL-XH functionality might be limited.")

# 2. Standard/Legacy Series (Input Registers 0-124, 125-249)
try:
    from register_maps.growatt_TL3X_MAX_MID_MAC_MIC_input_reg import REG_INPUT_0_MAP as MAP_TL3X_0
except ImportError:
    MAP_TL3X_0 = {}
    logging.warning("Could not import growatt_input_0. Standard/Legacy functionality might be limited.")

# 3. MAX 1500V / MAX-X LV Series (Input Registers 0-124, 125-249, 875-999)
try:
    from register_maps.growatt_MAX_input_reg import REG_INPUT_MAX_MAP as MAP_MAX
except ImportError:
    MAP_MAX = {}
    logging.warning("Could not import growatt_MAX_input. MAX series functionality might be limited.")

try:
    from register_maps.growatt_TLXH_min_input import REG_INPUT_TLXH_MIN_MAP as MAP_TLXH_MIN
except ImportError:
    MAP_TLXH_MIN = {}
    logging.warning("Could not import growatt_TLXH_min_input. TL-XH MIN functionality might be limited.")

# 4. Storage / Hybrid Series MIX Type (Input Registers 0-124, 1000-1124)
try:
    from register_maps.growatt_storage_mix_input import REG_INPUT_MIX_MAP as MAP_MIX
except ImportError:
    MAP_MIX = {}
    logging.warning("Could not import growatt_storage_mix_input. Storage MIX functionality might be limited.")

# 5. Storage / Hybrid Series SPA Type (Input Registers 1000-1124, 1125-1249, 2000-2124)
try:
    from register_maps.growatt_storage_spa_input import REG_INPUT_SPA_MAP as MAP_SPA
except ImportError:
    MAP_SPA = {}
    logging.warning("Could not import growatt_storage_spa_input. Storage SPA functionality might be limited.")

# 6. Storage / Hybrid Series SPH Type (Input Registers 0-124, 1000-1124, 1125-1249)
try:
    from register_maps.growatt_storage_sph_input import REG_INPUT_SPH_MAP as MAP_SPH
except ImportError:
    MAP_SPH = {}
    logging.warning("Could not import growatt_storage_sph_input. Storage SPH functionality might be limited.")

# 3. Holding Registers (Settings/Info 3000+) - Optional


# --- Constants & Lookups ---

STATE_CODES = {
    0: "Waiting", 
    1: "Normal", 
    3: "Fault",
    4: "Flash"
}

INVERTER_RUN_STATES = {
    0: "Waiting module",
    1: "Self-test mode",
    2: "Reserved",
    3: "SysFault module",
    4: "Flash module",
    5: "PVBATOnline module",
    6: "BatOnline module",
    7: "PVOfflineMode",
    8: "BatOfflineMode",
}

INVERTER_WEB_PAGE_STATUS = {
    0: "StandbyStatus",
    1: "NormalStatus",
    3: "FaultStatus",
    4: "FlashStatus",
}

DERATING_MODE = {
    0: "No Derating",
    1: "PV",
    2: "Temperature",
    3: "Vac",
    4: "Fac",
    5: "Tboost",
    6: "Tinv",
    7: "Control",
    8: "*LoadSpeed",
    9: "*OverBackByTime",
}

ERROR_CODES = {
    0: "None",
    24: "Auto Test Failed",
    25: "No AC Connection",
    26: "PV Isolation Low",
    27: "Residual Current High",
    28: "DC Current High",
    29: "PV Voltage High",
    30: "AC Voltage Outrange",
    31: "AC Freq Outrange",
    32: "Module Hot",
    # Add more specific error codes here if needed
}

# Fallback for generic error codes (e.g., Error 100)
for i in range(1, 24):
    if i not in ERROR_CODES:
        ERROR_CODES[i] = f"Error Code: {99 + i}"


def parse_inverter_status(value):
    """
    Parses the 16-bit value from InverterStatus register (3000)
    into Status (Lower 8 Bits) and Mode (Higher 8 Bits).
    :param value: The raw integer value read from register 3000
    :return: A tuple (status, mode)
    """
    # Lower 8 Bits: Machine Status (e.g., 0=Standby, 1=Normal, 3=Fault)
    # 0xFF is 11111111 in binary. The AND operation masks out the upper bits.
    status = value & 0xFF
    # Higher 8 Bits: Run Mode (e.g., 5=PVBATOnline, 6=BatOnline)
    # Shift right by 8 bits to move the high byte to the low position, then mask.
    mode = (value >> 8) & 0xFF
    return status, mode


class Growatt:
    """
    Main class to control and read data from Growatt Inverters via Modbus RTU.
    """

    def __init__(self, client, name, unit, model, log=None):
        """
        Initialize the inverter object.
        
        :param client: Pymodbus Serial Client object (must be connected)
        :param name: Name of the inverter (for logging)
        :param unit: Modbus Unit ID (Slave Address)
        :param model: Model variant, e.g., "TL-XH" or "TL3X"
        """
        self.client = client
        self.name = name
        self.unit = unit
        self.model = model
        self.log = logging.getLogger(f"Growatt_{name}")

    def _read_block(self, start_reg, length, map_ref, is_input_reg=True):
        """
        Reads a contiguous block of registers and parses them using the provided map.
        
        :param start_reg: Start address of the block
        :param length: Number of registers to read
        :param map_ref: The dictionary containing the register definitions
        :param is_input_reg: True for Input Registers (04), False for Holding Registers (03)
        :return: Dictionary of parsed data or None on error
        """
        try:
            if is_input_reg:
                rr = self.client.read_input_registers(start_reg, length, unit=self.unit)
            else:
                rr = self.client.read_holding_registers(start_reg, length, unit=self.unit)

            if isinstance(rr, ModbusIOException) or rr.isError():
                self.log.error(f"Modbus Error reading block {start_reg}: {rr}")
                return None
            
            # Parse raw data using the register map
            return self._parse_registers(rr, start_reg, map_ref)

        except Exception as e:
            self.log.exception(f"Exception reading block {start_reg}: {e}")
            return None

    def _parse_registers(self, row, base_index, reg_map):
        """
        Generic Parser: Converts raw register data into readable values based on the map.
        Handles data types (uint, int, uint32, ascii) and scaling.
        """
        results = {}
        
        # Ensure we have valid register data
        if not hasattr(row, 'registers') or not row.registers:
            return results

        for name, (offset, length, scale, dtype) in reg_map.items():
            # Safety check: Is the defined register inside the read block?
            # Note: offset in map is relative to base_index
            if offset + length > len(row.registers):
                continue

            # Extract specific registers for this value
            regs = row.registers[offset: offset + length]
            val = 0

            # --- Type Conversion ---
            if dtype == "ascii":
                try:
                    # Pack as Big-Endian uint16 and decode to ASCII
                    byte_data = b"".join(struct.pack(">H", r) for r in regs)
                    # Remove null bytes and whitespace
                    val = byte_data.decode("ascii", errors='ignore').strip('\x00').strip()
                except Exception:
                    val = str(regs)  # Fallback

            elif dtype == "uint32":
                # 32-Bit Unsigned (High Word First / Big Endian)
                val = (regs[0] << 16) + regs[1]

            elif dtype == "int32":
                # 32-Bit Signed (High Word First)
                val = (regs[0] << 16) + regs[1]
                # Handle Two's Complement for negative values
                if val > 0x7FFFFFFF:
                    val -= 0x100000000

            elif dtype == "int":
                # 16-Bit Signed
                val = regs[0]
                # Handle Two's Complement
                if val > 0x7FFF:
                    val -= 0x10000        
            else:
                # Default "uint" (16-Bit Unsigned)
                val = regs[0]

            # --- Scaling ---
            # Apply scaling only if it's a number and scale is not 1
            if scale != 1 and isinstance(val, (int, float)):
                val = float(val) / scale

            results[name] = val

        return results

    def _process_logic(self, data):
        """
        Post-processing logic:
        - Split status bits
        - Map error codes to text
        - Calculate derived values if needed
        """
        # 1. Split Inverter Status (Register 3000 or 0)
        # Low Byte = Status, High Byte = Run Mode
        if "InverterStatus" in data and self.model == "TL-XH" or self.model == "TL_X":
            raw = int(data["InverterStatus"])
            status = raw & 0xFF
            mode = (raw >> 8) & 0xFF
            
            data["StatusVal"] = INVERTER_WEB_PAGE_STATUS[status]
            data["StatusMode"] = INVERTER_RUN_STATES[mode]
        else:
            status = int(data["InverterStatus"])
            data["StatusText"] = STATE_CODES.get(status, f"Unknown({status})")

        # 2. Map Fault Codes to Text
        if "FaultCode" in data:
            code = int(data["FaultCode"])
            data["FaultText"] = ERROR_CODES.get(code, f"Error {code}")

        # 3. Map Derating Mode to Text
        if "DeratingMode" in data:
            code = int(data["DeratingMode"])
            data["DeratingText"] = DERATING_MODE.get(code, "Unknown")
            
        return data

    def update(self):
        """
        Main method to read data.
        Selects the appropriate register blocks based on the initialized 'model'.
        """
        data = {}
        # --- Logic for TL-XH Series (Battery Ready) ---
        if (self.model == "TL-XH" or self.model == "TL_X") and MAP_TLXH_3000:
            # Block 1: Inverter Data (3000-3124) -> 125 Registers
            block1 = self._read_block(3000, 125, MAP_TLXH_3000, is_input_reg=True)
            if block1:
                data.update(block1)
            if self.model == "TL-XH":
                # Block 2: Battery Data (3125-3249) -> 125 Registers
                # Reads Battery/BMS data specifically for XH series
                block2 = self._read_block(3125, 125, MAP_TLXH_3000, is_input_reg=True)
                if block2:
                    data.update(block2)
        # --- Logic for TL3X / Legacy Series ---
        elif self.model == "TL3X" and MAP_TL3X_0:
            # Block 1: Basic Data (0-124)
            block1 = self._read_block(0, 125, MAP_TL3X_0, is_input_reg=True)
            if block1:
                data.update(block1)
            # Block 2: String & PID Data (125-249)
            block2 = self._read_block(125, 125, MAP_TL3X_0, is_input_reg=True)
            if block2:
                data.update(block2)
        # --- Logic for MAX 1500V、MAX-X LV Series ---
        elif self.model == "MAX" and MAP_MAX:
            # Block 1: Basic Data (0-124)
            block1 = self._read_block(0, 125, MAP_MAX, is_input_reg=True)
            if block1:
                data.update(block1)
            # Block 2: String & PID Data (125-249)
            block2 = self._read_block(125, 125, MAP_MAX, is_input_reg=True)
            if block2:
                data.update(block2)
            # Block 3: Extended Data (875-999)
            block3 = self._read_block(875, 125, MAP_MAX, is_input_reg=True)
            if block3:
                data.update(block3)
        # --- Logic for TL-XH MIN Series ---
        elif (self.model == "TL-XH_MIN" or self.model == "TL_X_MIN") and MAP_TLXH_MIN:
            # Block 1: Inverter Data (3000-3124) -> 125 Registers
            block1 = self._read_block(3000, 125, MAP_TLXH_MIN, is_input_reg=True)
            if block1:
                data.update(block1)
            if self.model == "TL-XH_MIN":
                # Block 2: Battery Data (3125-3249) -> 125 Registers
                block2 = self._read_block(3125, 125, MAP_TLXH_MIN, is_input_reg=True)
                if block2:
                    data.update(block2)
                # Block 3: Extended Battery Data (3250-3374) -> 125 Registers
                block3 = self._read_block(3250, 125, MAP_TLXH_MIN, is_input_reg=True)
                if block3:
                    data.update(block3)
        # --- Logic for Storage / Hybrid MIX Series ---
        elif self.model == "MIX" and MAP_MIX:
            # Block 1: Basic Inverter Data (0-124)
            block1 = self._read_block(0, 125, MAP_MIX, is_input_reg=True)
            if block1:
                data.update(block1)
            # Block 2: Storage / Hybrid Data (1000-1124)
            block2 = self._read_block(1000, 125, MAP_MIX, is_input_reg=True)
            if block2:
                data.update(block2)
        # --- Logic for Storage / Hybrid SPA Series ---
        elif self.model == "SPA" and MAP_SPA:
            # Block 1: Storage / Hybrid Data (1000-1124)
            block1 = self._read_block(1000, 125, MAP_SPA, is_input_reg=True)
            if block1:
                data.update(block1)
            # Block 2: Extended Battery Info (1125-1249)
            block2 = self._read_block(1125, 125, MAP_SPA, is_input_reg=True)
            if block2:
                data.update(block2)
            # Block 3: SPA Specific AC/Grid Data (2000-2124)
            block3 = self._read_block(2000, 125, MAP_SPA, is_input_reg=True)
            if block3:
                data.update(block3)
        # --- Logic for Storage / Hybrid SPH Series ---
        elif self.model == "SPH" and MAP_SPH:
            # Block 1: Basic Inverter Data (0-124)
            block1 = self._read_block(0, 125, MAP_SPH, is_input_reg=True)
            if block1:
                data.update(block1)
            # Block 2: Storage / Hybrid Data (1000-1124)
            block2 = self._read_block(1000, 125, MAP_SPH, is_input_reg=True)
            if block2:
                data.update(block2)
            # Block 3: Extended Battery Info (1125-1249)
            block3 = self._read_block(1125, 125, MAP_SPH, is_input_reg=True)
            if block3:
                data.update(block3)
        else:
            self.log.warning(f"No valid register map found for model: {self.model}")

        # Apply post-processing (Text mapping, bit splitting)
        if data:
            data = self._process_logic(data)
        return data

    def read_holding(self):
        """
        Reads Holding Registers (Settings, Serial Number, etc.).
        Usually starts at 3000 for TL-X series.
        """
        return {}