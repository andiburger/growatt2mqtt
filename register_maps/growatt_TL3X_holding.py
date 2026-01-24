"""
growatt_TL3X_holding.py

Modbus Holding Register Map for Growatt TL3-X (MAX, MID, MAC Type).
Based on Protocol V1.24 - HOLDING REGISTERS (Function Code 03).

Covered Ranges:
- 0-124: Basic Settings (On/Off, Power Limits, PF)
- 125-249: Advanced Grid & System Parameters

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_HOLDING_TL3X_MAP = {
    # =================================================================
    # GROUP 1: Basic Settings (0-124)
    # =================================================================
    
    # 0: Inverter Switch (0: Off, 1: On)
    "OnOff": (0, 1, 1, "uint"),

    # 1: Grid Standard (Country Code index)
    "GridStandard": (1, 1, 1, "uint"),

    # 3: Active Power Rate (0-100%) - Used for power throttling
    "ActivePowerRate": (3, 1, 1, "uint"),

    # 4: Reactive Power Rate (0-100%)
    "ReactivePowerRate": (4, 1, 1, "uint"),

    # 5: Power Factor (0-10000, where 10000 = 1.0)
    "PowerFactor": (5, 1, 10000, "uint"),

    # 16-17: Grid Voltage High/Low Limits (0.1V)
    "GridVoltHigh": (16, 1, 10, "uint"),
    "GridVoltLow": (17, 1, 10, "uint"),

    # 18-19: Grid Frequency High/Low Limits (0.01Hz)
    "GridFreqHigh": (18, 1, 100, "uint"),
    "GridFreqLow": (19, 1, 100, "uint"),

    # 88: Modbus Address (1-247)
    "ModbusAddress": (88, 1, 1, "uint"),

    # =================================================================
    # GROUP 2: Advanced Parameters (125-249)
    # =================================================================

    # 125: PV Start Voltage (0.1V)
    "VpvStart": (0, 1, 10, "uint"), # Relative to base 125

    # 231: Export Limit Enable (0: Disable, 1: Enable)
    "ExportLimitEnable": (106, 1, 1, "uint"), # Relative to base 125 (125+106=231)

    # 232: Export Limit Power Rate (0.1% or 0.1W depending on firmware)
    "ExportLimitRate": (107, 1, 1, "uint"),

    # =================================================================
    # GROUP 3: Identification (3000-3124)
    # =================================================================
    
    # 3001-3015: Serial Number (ASCII, 15 Registers)
    "SerialNumber": (1, 15, 1, "ascii"), # Relative to base 3000

    # 3021-3024: Firmware Version (ASCII, 4 Registers)
    "FirmwareVersion": (21, 4, 1, "ascii"), # Relative to base 3000
}