#!/usr/bin/env python3
"""
growatt_vpp_input.py

Modbus Input Register Map for Growatt VPP Protocol.
Based on "GROWATT VPP COMMUNICATION PROTOCOL OF INVERTER V2.01".
"""

# Block 1: 31000 - 31099 (Working Status & PV Params)
REG_INPUT_VPP_31000_MAP = {
    "InverterStatus": (0, 1, 1, "uint"), # 31000 Working state of energy storage machine
    "BatteryWorkingStatus": (1, 1, 1, "uint"),
    "PriorityOfWork": (2, 1, 1, "uint"),
    "FaultCode": (5, 1, 1, "uint"),
    "FaultSubCode": (6, 1, 1, "uint"),
    "AlarmCode": (7, 1, 1, "uint"),
    "AlarmSubCode": (8, 1, 1, "uint"),
    "PV1Voltage": (10, 1, 10, "int"), # 0.1V
    "PV1Current": (11, 1, 10, "int"), # 0.1A
    "PV2Voltage": (12, 1, 10, "int"),
    "PV2Current": (13, 1, 10, "int"),
    "PVInputPower": (58, 2, 10, "int32"), # 0.1W
}

# Block 2: 31100 - 31199 (AC Info)
REG_INPUT_VPP_31100_MAP = {
    "ActivePower": (0, 2, 10, "int32"), # 0.1W (Positive: export, Negative: import)
    "ReactivePower": (2, 2, 10, "int32"), # 0.1VA
    "GridFrequency": (5, 1, 100, "uint"), # 0.01Hz
    "GridVoltageAB": (6, 1, 10, "uint"), # 0.1V
    "GridVoltageBC": (7, 1, 10, "uint"),
    "GridVoltageCA": (8, 1, 10, "uint"),
    "GridCurrentA": (9, 1, 10, "int"), # 0.1A
    "GridCurrentB": (10, 1, 10, "int"),
    "GridCurrentC": (11, 1, 10, "int"),
    "MeterPower": (12, 2, 10, "int32"), # 0.1W
    "InverterTemperature": (14, 1, 10, "int"), # 0.1C
    "PowerToUserDaily": (18, 2, 10, "uint32"), # 0.1KWH
    "TotalPowerToUser": (20, 2, 10, "uint32"),
    "PowerToGridDaily": (22, 2, 10, "uint32"),
    "TotalPowerToGrid": (24, 2, 10, "uint32"),
}

# Block 3: 31200 - 31299 (Battery Information)
REG_INPUT_VPP_31200_MAP = {
    "ChargeDischargePower": (0, 2, 10, "int32"), # 0.1W Positive: charge, Negative: discharge
    "DailyChargeOfBattery": (2, 2, 10, "uint32"), # 0.1KWH
    "CumulativeChargeOfBattery": (4, 2, 10, "uint32"),
    "DailyDischargeOfBattery": (6, 2, 10, "uint32"),
    "CumulativeDischargeOfBattery": (8, 2, 10, "uint32"),
    "BatteryVoltage": (14, 1, 10, "int"), # 0.1V
    "BatteryCurrent": (15, 2, 10, "int32"), # 0.1A
    "SOC": (17, 1, 1, "uint"),
    "SOH": (18, 1, 1, "uint"),
    "BatteryCapacityRatingFCC": (19, 2, 1, "uint32"),
    "BatteryEnvironmentalTemperature": (23, 1, 10, "int"), # 0.1C
}
