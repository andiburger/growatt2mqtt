"""
growatt_TLXH_min_holding.py

Modbus Holding Register Map for Growatt TL-X / TL-XH / TL-XH US (MIN Type).
Based on Protocol V1.24 - HOLDING REGISTERS (Function Code 03).

Covered Ranges:
- 0-124: Basic System Settings (On/Off, Power Limits, Grid)
- 3000-3124: Advanced Settings & Time (RTC, Export Limit, Battery Config)
- 3125-3249: Specific US/Extended Battery Config (TL-XH US)

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_HOLDING_TLXH_MIN_MAP = {
    # =================================================================
    # GROUP 1: Basic Settings (0-124)
    # =================================================================
    
    # 0: Inverter On/Off switch (0: Off, 1: On)
    "OnOff": (0, 1, 1, "uint"),

    # 3: Active Power Rate (0-100%)
    "ActivePowerRate": (3, 1, 1, "uint"),

    # 5: Power Factor (0-10000, 10000 = 1.0)
    "PowerFactor": (5, 1, 10000, "uint"),

    # 88: Modbus Address (1-247)
    "ModbusAddress": (88, 1, 1, "uint"),

    # =================================================================
    # GROUP 2: Advanced & Battery Control (3000-3124)
    # =================================================================

    # 3001-3015: Serial Number (ASCII, 15 Registers)
    "SerialNumber": (1, 15, 1, "ascii"), # Relative to 3000

    # 3021-3024: Firmware Version (ASCII, 4 Registers)
    "FirmwareVersion": (21, 4, 1, "ascii"),

    # --- Real Time Clock (RTC) ---
    "Year": (25, 1, 1, "uint"),
    "Month": (26, 1, 1, "uint"),
    "Day": (27, 1, 1, "uint"),
    "Hour": (28, 1, 1, "uint"),
    "Minute": (29, 1, 1, "uint"),
    "Second": (30, 1, 1, "uint"),

    # --- Export Limit Settings ---
    "ExportLimitEnable": (38, 1, 1, "uint"), # 0: Disable, 1: Enable
    "ExportLimitRate": (39, 1, 1, "uint"),   # 0-100%

    # --- Battery Management (TL-XH) ---
    # 3047: Max Charge Power Rate (0-100%)
    "MaxChargeRate": (47, 1, 1, "uint"),
    # 3048: Max Discharge Power Rate (0-100%)
    "MaxDischargeRate": (48, 1, 1, "uint"),

    # 3049: AC Charge Enable (Charging from Grid)
    "ACChargeEnable": (49, 1, 1, "uint"), # 0: Disable, 1: Enable

    # 3080: Operation Priority Mode
    # 0: Load First, 1: Battery First, 2: Grid First
    "PriorityMode": (80, 1, 1, "uint"),

    # =================================================================
    # GROUP 3: US Specific / Extended Battery (3125-3249)
    # =================================================================

    # 3125: Battery Type (0: Lead-acid, 1: Lithium)
    "BatteryType": (125, 1, 1, "uint"), # Relative to 3000 -> 3125

    # 3129: Forced Discharge Enable
    "ForcedDischargeEnable": (129, 1, 1, "uint"),
}