#!/usr/bin/env python3
"""
growatt_MOD_TL3_XH_holding.py

Modbus Holding Register Map for Growatt MOD TL3-XH Inverters.
Based on Protocol V1.24 - HOLDING REGISTERS (Function Code 03).

Covered Ranges:
- 0-124: Basic Settings (On/Off, Power Rate, PF)
- 3000-3124: Advanced Settings (Time, Export Limit, Battery Control)

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_HOLDING_MOD_TL3_XH_MAP = {
    # =================================================================
    # GROUP 1: Basic Settings (0-124)
    # =================================================================
    
    # 0: On/Off Switch
    # 0: Off, 1: On
    "OnOff": (0, 1, 1, "uint"),

    # 1: Command (Grid Standard / Country Code)
    # Value depends on country (e.g., VDE 4105)
    "GridStandard": (1, 1, 1, "uint"),

    # 3: Active Power Percentage (0-100%)
    "ActivePowerRate": (3, 1, 1, "uint"),

    # 4: Reactive Power Percentage (0-100%)
    "ReactivePowerRate": (4, 1, 1, "uint"),

    # 5: Power Factor (0-10000, 10000 = 1.0)
    "PowerFactor": (5, 1, 10000, "uint"),

    # 8: PV Voltage High Limit (0.1V)
    "VpvStart": (8, 1, 10, "uint"),

    # 16: Grid Voltage High Limit (0.1V)
    "GridVoltHigh": (16, 1, 10, "uint"),
    # 17: Grid Voltage Low Limit (0.1V)
    "GridVoltLow": (17, 1, 10, "uint"),
    # 18: Grid Freq High Limit (0.01Hz)
    "GridFreqHigh": (18, 1, 100, "uint"),
    # 19: Grid Freq Low Limit (0.01Hz)
    "GridFreqLow": (19, 1, 100, "uint"),

    # 88: Modbus Address
    "ComAddress": (88, 1, 1, "uint"),
}


REG_HOLDING_MOD_TL3_XH_ADVANCED_SETTINGS_MAP = {
    # =================================================================
    # GROUP 2: Advanced Settings & Identification (3000-3124)
    # =================================================================

    # 3000: Export Limit Failed Power Rate (0-100%)
    "ExportLimitFailSafe": (0, 1, 1, "uint"),

    # 3001-3015: Serial Number (ASCII, 30 chars/15 regs)
    # Note: Offset is relative to 3000 -> 1
    "SerialNumber": (1, 15, 1, "ascii"),

    # 3016-3020: Model Number (ASCII, 10 chars/5 regs)
    "ModelNumber": (16, 5, 1, "ascii"),

    # 3021-3024: Firmware Version (ASCII, 8 chars/4 regs)
    "FirmwareVersion": (21, 4, 1, "ascii"),

    # --- System Time (RTC) ---
    # 3025: Year (e.g. 2023)
    "Year": (25, 1, 1, "uint"),
    # 3026: Month
    "Month": (26, 1, 1, "uint"),
    # 3027: Day
    "Day": (27, 1, 1, "uint"),
    # 3028: Hour
    "Hour": (28, 1, 1, "uint"),
    # 3029: Minute
    "Minute": (29, 1, 1, "uint"),
    # 3030: Second
    "Second": (30, 1, 1, "uint"),

    # --- Export Limit Settings ---
    # 3038: Export Limit Enable
    # 0: Disable, 1: Enable
    "ExportLimitEnable": (38, 1, 1, "uint"),

    # 3039: Export Limit Power Rate (0-100%)
    "ExportLimitRate": (39, 1, 1, "uint"),

    # --- Battery / EMS Settings (XH Series) ---
    # 3047: Charge Power Limit (%)
    "BatChargePowerLimit": (47, 1, 1, "uint"),
    
    # 3048: Discharge Power Limit (%)
    "BatDischargePowerLimit": (48, 1, 1, "uint"),

    # 3049: AC Charge Enable (Grid Charging)
    # 0: Disable, 1: Enable
    "ACChargeEnable": (49, 1, 1, "uint"),

    # 3050-3052: AC Charge Time Slot 1
    # Format usually: Start Hour, Start Min, End Hour... need specific parsing logic often
    "ACChargeTime1_StartH": (50, 1, 1, "uint"),
    "ACChargeTime1_StartM": (51, 1, 1, "uint"),
    "ACChargeTime1_EndH": (52, 1, 1, "uint"),
    
    # 3080: Battery Priority
    # 0: Load First, 1: Battery First, 2: Grid First
    "BatPriority": (80, 1, 1, "uint"),
}