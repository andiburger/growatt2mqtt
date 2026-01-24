"""
growatt_MAX_holding.py

Modbus Holding Register Map for Growatt MAX 1500V / MAX-X LV.
Based on Protocol V1.24 - HOLDING REGISTERS (Function Code 03).

Covered Ranges:
- 0-124: Basic Settings (Power Rates, PF, State)
- 125-249: Advanced Grid & Protection Settings

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_HOLDING_MAX_MAP = {
    # =================================================================
    # GROUP 1: Basic Settings (0-124)
    # =================================================================
    
    # 0: Inverter On/Off logic (0: Off, 1: On)
    "OnOff": (0, 1, 1, "uint"),

    # 3: Active Power Percentage (0-100%)
    "ActivePowerRate": (3, 1, 1, "uint"),

    # 4: Fixed Reactive Power Percentage (0-100%)
    "ReactivePowerRate": (4, 1, 1, "uint"),

    # 5: Power Factor (Scale 10000, e.g., 10000 = 1.0)
    "PowerFactor": (5, 1, 10000, "uint"),

    # 16-17: Grid Voltage High/Low Limits (0.1V)
    "GridVoltHigh": (16, 1, 10, "uint"),
    "GridVoltLow": (17, 1, 10, "uint"),

    # 18-19: Grid Frequency High/Low Limits (0.01Hz)
    "GridFreqHigh": (18, 1, 100, "uint"),
    "GridFreqLow": (19, 1, 100, "uint"),

    # 30: Start-up Delay Time (Seconds)
    "StartDelay": (30, 1, 1, "uint"),

    # 88: Modbus Address (1-247)
    "ModbusAddress": (88, 1, 1, "uint"),

    # =================================================================
    # GROUP 2: Extended Grid & Advanced Settings (125-249)
    # =================================================================

    # 125: PV Start Voltage (0.1V)
    "VpvStart": (0, 1, 10, "uint"), # Offset relative to 125

    # 131: Active Power Islanding Protection (0: Disable, 1: Enable)
    "IslandingProt": (6, 1, 1, "uint"),

    # 231: Export Limit Enable (0: Disable, 1: Enable)
    "ExportLimitEnable": (106, 1, 1, "uint"),

    # 232: Export Limit Power Rate (0.1% or 0.1W depending on specific firmware)
    "ExportLimitRate": (107, 1, 1, "uint"),
}