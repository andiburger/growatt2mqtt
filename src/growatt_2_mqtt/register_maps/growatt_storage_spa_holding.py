"""
growatt_storage_spa_holding.py

Modbus Holding Register Map for Growatt Storage (SPA Type) Inverters.
Based on Protocol V1.24 - HOLDING REGISTERS (Function Code 03).

Covered Ranges:
- 0-124: Basic System Settings
- 1000-1124: SPA Storage Strategy & Time-of-Use Settings

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_HOLDING_SPA_MAP = {
    # =================================================================
    # GROUP 1: Basic Settings (0-124)
    # =================================================================
    
    # 0: Inverter Switch (0: Off, 1: On)
    "OnOff": (0, 1, 1, "uint"),

    # 3: Active Power Percentage (0-100%)
    "ActivePowerRate": (3, 1, 1, "uint"),

    # 88: Modbus Address (1-247)
    "ModbusAddress": (88, 1, 1, "uint"),
}

REG_HOLDING_SPA_STRAT_CHRG_MAP = {
    # =================================================================
    # GROUP 2: SPA Strategy & Charge Settings (1000-1124)
    # =================================================================

    # 1000: Storage Operation Mode
    # 0: Load First, 1: Battery First, 2: Grid First
    "StorageMode": (0, 1, 1, "uint"), # Relative to 1000

    # 1001: Battery Type (0: Lead-acid, 1: Lithium)
    "BatteryType": (1, 1, 1, "uint"),

    # 1010: Max Charge Power Rate (0-100%)
    "MaxChargeRate": (10, 1, 1, "uint"),

    # 1011: Max Discharge Power Rate (0-100%)
    "MaxDischargeRate": (11, 1, 1, "uint"),

    # 1012: Stop Charging SOC (1-100%)
    "StopChargeSOC": (12, 1, 1, "uint"),

    # 1013: Stop Discharging SOC (1-100%)
    "StopDischargeSOC": (13, 1, 1, "uint"),

    # --- Time-of-Use / AC Charge Settings ---
    # 1014: AC Charge (Charging from Grid) Enable (0: Disable, 1: Enable)
    "ACChargeEnable": (14, 1, 1, "uint"),

    # 1015-1019: AC Charge Time Slot 1
    "ACCharge_StartHour": (15, 1, 1, "uint"),
    "ACCharge_StartMin": (16, 1, 1, "uint"),
    "ACCharge_EndHour": (17, 1, 1, "uint"),
    "ACCharge_EndMin": (18, 1, 1, "uint"),
    "ACCharge_PeriodEnable": (19, 1, 1, "uint"),

    # 1047: Export Limit Enable (0: Disable, 1: Enable)
    "ExportLimitEnable": (47, 1, 1, "uint"),

    # 1048: Export Limit Power Rate (0-100%)
    "ExportLimitRate": (48, 1, 1, "uint"),

    # 1056: EPS Mode Enable (0: Disable, 1: Enable)
    "EPS_Enable": (56, 1, 1, "uint"),
}