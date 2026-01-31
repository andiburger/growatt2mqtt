#!/usr/bin/env python3
"""
growatt.py

Refactored module for Modbus RTU communication with Growatt Inverters.
Supports TL-X, TL-XH, MOD-XH, and other series via flexible register maps.
"""

import logging
import struct
import time
from pymodbus.exceptions import ModbusIOException

# --- Import Register Maps ---
try:
    from register_maps.growatt_TLXH_input_reg import REG_INPUT_MAP as MAP_TLXH_3000
except ImportError:
    MAP_TLXH_3000 = {}

try:
    from register_maps.growatt_TL3X_MAX_MID_MAC_MIC_input_reg import REG_INPUT_0_MAP as MAP_TL3X_0
except ImportError:
    MAP_TL3X_0 = {}

try:
    from register_maps.growatt_MAX_input_reg import REG_INPUT_MAX_MAP as MAP_MAX
except ImportError:
    MAP_MAX = {}

try:
    from register_maps.growatt_TLXH_min_input import REG_INPUT_TLXH_MIN_MAP as MAP_TLXH_MIN
except ImportError:
    MAP_TLXH_MIN = {}

try:
    from register_maps.growatt_storage_mix_input import REG_INPUT_MIX_MAP as MAP_MIX
except ImportError:
    MAP_MIX = {}

try:
    from register_maps.growatt_storage_spa_input import REG_INPUT_SPA_MAP as MAP_SPA
except ImportError:
    MAP_SPA = {}

try:
    from register_maps.growatt_storage_sph_input import REG_INPUT_SPH_MAP as MAP_SPH
except ImportError:
    MAP_SPH = {}

try:
    from register_maps.growatt_meter_input import REG_METER_EASTRON_MAP as MAP_EASTRON
    from register_maps.growatt_meter_input import REG_METER_CHINT_MAP as MAP_CHINT
except ImportError:
    MAP_EASTRON = {}
    MAP_CHINT = {}

# MOD TL3-XH Input Registers
try:
    from register_maps.growatt_MOD_TL3_XH_input import REG_INPUT_MOD_TL3_XH_MAP as MAP_MOD_TL3_XH
except ImportError:
    MAP_MOD_TL3_XH = {}

# --- Holding Registers Imports (Optional) ---
try:
    from register_maps.growatt_MOD_TL3_XH_holding import REG_HOLDING_MOD_TL3_XH_MAP
except ImportError:
    REG_HOLDING_MOD_TL3_XH_MAP = {}
try:
    from register_maps.growatt_MAX_holding import REG_HOLDING_MAX_MAP
except ImportError:
    REG_HOLDING_MAX_MAP = {}
try:
    from register_maps.growatt_TLXH_min_holding import REG_HOLDING_TLXH_MIN_MAP
except ImportError:
    REG_HOLDING_TLXH_MIN_MAP = {}
try:
    from register_maps.growatt_storage_mix_holding import REG_HOLDING_MIX_MAP
except ImportError:
    REG_HOLDING_MIX_MAP = {}
try:
    from register_maps.growatt_storage_spa_holding import REG_HOLDING_SPA_MAP
except ImportError:
    REG_HOLDING_SPA_MAP = {}
try:
    from register_maps.growatt_storage_sph_holding import REG_HOLDING_SPH_MAP
except ImportError:
    REG_HOLDING_SPH_MAP = {}

# --- Constants & Lookups ---

# Generic State Codes (Low Byte of InverterStatus)
STATE_CODES = {
    0: "Waiting", 
    1: "Normal", 
    3: "Fault",
    4: "Flash",
    5: "PVBATOnline",
    6: "BatOnline",
    7: "PVOffline",
    8: "BatOffline"
}

# Run Modes (High Byte of InverterStatus for XH/Hybrid)
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

# Web Page Status Mappings
INVERTER_WEB_PAGE_STATUS = {
    0: "StandbyStatus",
    1: "NormalStatus",
    3: "FaultStatus",
    4: "FlashStatus",
    5: "PVBatOnlineStatus",
    6: "BatOnlineStatus",
    7: "PVOfflineStatus",
    8: "BatOfflineStatus"
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
}
# Fallback for generic error codes
for i in range(1, 24):
    if i not in ERROR_CODES:
        ERROR_CODES[i] = f"Error Code: {99 + i}"


class Growatt:
    """
    Main class to control and read data from Growatt Inverters via Modbus RTU.
    """

    def __init__(self, client, name, unit, model, log=None):
        self.client = client
        self.name = name
        self.unit = unit
        self.model = model
        self.log = logging.getLogger(f"Growatt_{name}")

    def read_settings(self):
        """Reads Holding Registers."""
        data = {}
        # MOD-XH
        if self.model == "MOD-XH" and REG_HOLDING_MOD_TL3_XH_MAP:
            # 3001 Offset logic applies to Holding as well for some FW versions
            # Trying standard 0 and 3000 blocks first
            b1 = self._read_block(0, 100, REG_HOLDING_MOD_TL3_XH_MAP, is_input_reg=False)
            if b1: data.update(b1)
            b2 = self._read_block(3000, 100, REG_HOLDING_MOD_TL3_XH_MAP, is_input_reg=False)
            if b2: data.update(b2)
            
        elif self.model == "TL-XH" or self.model == "TL-XH-MIN":
            if REG_HOLDING_TLXH_MIN_MAP:
                b1 = self._read_block(0, 100, REG_HOLDING_TLXH_MIN_MAP, is_input_reg=False)
                if b1: data.update(b1)
                b2 = self._read_block(3000, 100, REG_HOLDING_TLXH_MIN_MAP, is_input_reg=False)
                if b2: data.update(b2)
                
        # ... Add other models here as needed ...
        return data

    def _read_block(self, start_reg, length, map_ref, is_input_reg=True):
        try:
            if is_input_reg:
                rr = self.client.read_input_registers(start_reg, length, unit=self.unit)
            else:
                rr = self.client.read_holding_registers(start_reg, length, unit=self.unit)

            if isinstance(rr, ModbusIOException) or rr.isError():
                # Suppress log spam for expected night-time timeouts if needed
                self.log.debug(f"Modbus Error reading block {start_reg}: {rr}")
                return None
            # --- NEU: DEBUG SCANNNER ---
            # Zeigt uns die rohen Zahlen im Log an, damit wir sie sortieren können
            if start_reg == 3000:
                self.log.error(f"!!! RAW DATA DUMP 3001: {rr.registers}")
            # ---------------------------
            return self._parse_registers(rr, start_reg, map_ref)
        except Exception as e:
            self.log.exception(f"Exception reading block {start_reg}: {e}")
            return None

    def _parse_registers(self, row, base_index, reg_map):
        results = {}
        if not hasattr(row, 'registers') or not row.registers:
            return results

        for name, (offset, length, scale, dtype) in reg_map.items():
            if offset + length > len(row.registers):
                continue

            regs = row.registers[offset: offset + length]
            val = 0

            # --- Type Conversion ---
            if dtype == "ascii":
                try:
                    byte_data = b"".join(struct.pack(">H", r) for r in regs)
                    val = byte_data.decode("ascii", errors='ignore').strip('\x00').strip()
                except Exception:
                    val = str(regs)

            elif dtype == "uint32":
                # Standard: High-Byte zuerst (wie bei deiner PV Leistung gesehen: 0, 14500)
                val_standard = (regs[0] << 16) + regs[1]
                
                # Smart-Check: Wenn der Wert riesig ist (>100 Mio) ODER es ein Energiewert ist,
                # dann ist er wahrscheinlich verdreht (Little Endian).
                if val_standard > 100000000 or (name.startswith("E_") and val_standard > 1000000):
                    val = (regs[1] << 16) + regs[0]
                else:
                    val = val_standard
                
                val = float(val) / scale

            elif dtype == "int32":
                # Same logic for signed 32-bit
                if self.model in ["MOD-XH", "TL-XH"]:
                    combined = (regs[1] << 16) + regs[0]
                else:
                    combined = (regs[0] << 16) + regs[1]
                
                if combined > 0x7FFFFFFF:
                    combined -= 0x100000000
                val = combined

            elif dtype == "int":
                val = regs[0]
                if val > 0x7FFF:
                    val -= 0x10000
            elif dtype == "float":
                try:
                    raw = struct.pack('>HH', regs[0], regs[1])
                    val = struct.unpack('>f', raw)[0]
                    val = round(val, 4)
                except Exception:
                    val = 0.0
            else:
                val = regs[0]

            # --- Scaling ---
            if scale != 1 and isinstance(val, (int, float)):
                val = float(val) / scale

            results[name] = val

        return results

    def _process_logic(self, data):
        # 1. Split Inverter Status
        # We use .get() everywhere to avoid KeyError: 7 or similar
        if "InverterStatus" in data:
            raw = int(data["InverterStatus"])
            
            # Hybrid / XH models pack Status + Mode
            if self.model in ["TL-XH", "TL-XH-MIN", "MOD-XH", "MIX", "SPH"]:
                status = raw & 0xFF
                mode = (raw >> 8) & 0xFF
                data["StatusVal"] = INVERTER_WEB_PAGE_STATUS.get(status, f"Unknown({status})")
                data["StatusMode"] = INVERTER_RUN_STATES.get(mode, f"UnknownMode({mode})")
            else:
                # Standard PV models just use the raw value as status
                data["StatusText"] = STATE_CODES.get(raw, f"Unknown({raw})")

        # 2. Map Fault Codes
        if "FaultCode" in data:
            code = int(data["FaultCode"])
            data["FaultText"] = ERROR_CODES.get(code, f"Error {code}")

        # 3. Map Derating Mode
        if "DeratingMode" in data:
            code = int(data["DeratingMode"])
            data["DeratingText"] = DERATING_MODE.get(code, "Unknown")
            
        return data

    def update(self):
        data = {}
        
        # --- MOD-XH Logic (Fixed 3001 Offset) ---
        if self.model == "MOD-XH" and MAP_MOD_TL3_XH:
            # We use 3001 as start address because 3000 returns garbage/shift on this firmware
            block1 = self._read_block(3000, 125, MAP_MOD_TL3_XH, is_input_reg=True)
            if block1: data.update(block1)
            
            # Second block also shifted by 1
            block2 = self._read_block(3125, 125, MAP_MOD_TL3_XH, is_input_reg=True)
            if block2: data.update(block2)

        # --- TL-XH Logic ---
        elif (self.model == "TL-XH" or self.model == "TL_X") and MAP_TLXH_3000:
            block1 = self._read_block(3000, 125, MAP_TLXH_3000, is_input_reg=True)
            if block1: data.update(block1)
            block2 = self._read_block(3125, 125, MAP_TLXH_3000, is_input_reg=True)
            if block2: data.update(block2)

        # --- TL3X Logic ---
        elif self.model == "TL3X" and MAP_TL3X_0:
            block1 = self._read_block(0, 125, MAP_TL3X_0, is_input_reg=True)
            if block1: data.update(block1)
            block2 = self._read_block(125, 125, MAP_TL3X_0, is_input_reg=True)
            if block2: data.update(block2)

        # --- MAX Logic ---
        elif self.model == "MAX" and MAP_MAX:
            block1 = self._read_block(0, 125, MAP_MAX, is_input_reg=True)
            if block1: data.update(block1)
            block2 = self._read_block(125, 125, MAP_MAX, is_input_reg=True)
            if block2: data.update(block2)
            block3 = self._read_block(875, 125, MAP_MAX, is_input_reg=True)
            if block3: data.update(block3)

        # --- Other models (Shortened for brevity, add back if needed) ---
        elif self.model == "SPH" and MAP_SPH:
            block1 = self._read_block(0, 125, MAP_SPH, is_input_reg=True)
            if block1: data.update(block1)
            block2 = self._read_block(1000, 125, MAP_SPH, is_input_reg=True)
            if block2: data.update(block2)
            block3 = self._read_block(1125, 125, MAP_SPH, is_input_reg=True)
            if block3: data.update(block3)
            
        elif self.model == "SPA" and MAP_SPA:
            block1 = self._read_block(1000, 125, MAP_SPA, is_input_reg=True)
            if block1: data.update(block1)
            block2 = self._read_block(1125, 125, MAP_SPA, is_input_reg=True)
            if block2: data.update(block2)
            
        elif self.model == "MIX" and MAP_MIX:
            block1 = self._read_block(0, 125, MAP_MIX, is_input_reg=True)
            if block1: data.update(block1)
            block2 = self._read_block(1000, 125, MAP_MIX, is_input_reg=True)
            if block2: data.update(block2)
        
        elif self.model == "EASTRON" and MAP_EASTRON:
             block1 = self._read_block(0, 50, MAP_EASTRON, is_input_reg=True)
             if block1: data.update(block1)

        # Post-Processing
        if data:
            data = self._process_logic(data)
        return data