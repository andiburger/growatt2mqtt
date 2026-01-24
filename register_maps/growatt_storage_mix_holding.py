"""
growatt_storage_mix_holding.py

Modbus Holding Register Map for Growatt Storage (MIX Type) Inverters.
Based on Protocol V1.24 - HOLDING REGISTERS (Function Code 03).

Covered Ranges:
- 0-124: Basic System Settings
- 1000-1124: Storage / Hybrid Strategy & Time-of-Use Settings

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_HOLDING_MIX_MAP = {
    # =================================================================
    # GROUP 1: Basic Settings (0-124)
    # =================================================================
    
    # 0: Inverter On/Off logic (0: Off, 1: On)
    "OnOff": (0, 1, 1, "uint"),

    # 3: Active Power Percentage (0-100%)
    "ActivePowerRate": (3, 1, 1, "uint"),

    # 88: Modbus Address (1-247)
    "ModbusAddress": (88, 1, 1, "uint"),

    # =================================================================
    # GROUP 2: Storage & Time-of-Use (1000-1124)
    # =================================================================

    # 1000: Storage Operation Mode
    # 0: Load First, 1: Battery First, 2: Grid First
    "StorageMode": (1000, 1, 1, "uint"),

    # 1001: Battery Type (0: Lead-acid, 1: Lithium)
    "BatteryType": (1001, 1, 1, "uint"),

    # 1010: Charge Power Rate (0-100%)
    "ChargePowerRate": (1010, 1, 1, "uint"),

    # 1011: Discharge Power Rate (0-100%)
    "DischargePowerRate": (1011, 1, 1, "uint"),

    # 1012: Stop Charging SOC (e.g., 90 for 90%)
    "StopChargeSOC": (1012, 1, 1, "uint"),

    # 1013: Stop Discharging SOC (e.g. 10 for 10%)
    "StopDischargeSOC": (1013, 1, 1, "uint"),

    # --- Time-of-Use (AC Charge) Settings ---
    # 1014: AC Charge (Grid Charge) Enable (0: Disable, 1: Enable)
    "ACChargeEnable": (1014, 1, 1, "uint"),

    # 1015-1020: AC Charge Time Period 1
    "ACCharge_StartHour": (1015, 1, 1, "uint"),
    "ACCharge_StartMin": (1016, 1, 1, "uint"),
    "ACCharge_EndHour": (1017, 1, 1, "uint"),
    "ACCharge_EndMin": (1018, 1, 1, "uint"),
    "ACCharge_EnablePeriod": (1019, 1, 1, "uint"),

    # 1047: Grid Export Limit Enable (0: Disable, 1: Enable)
    "ExportLimitEnable": (1047, 1, 1, "uint"),

    # 1048: Export Limit Power Rate (0-100%)
    "ExportLimitRate": (1048, 1, 1, "uint"),
    
    # 1056: EPS (Off-grid) Mode Enable (0: Disable, 1: Enable)
    "EPS_ModeEnable": (1056, 1, 1, "uint"),
}