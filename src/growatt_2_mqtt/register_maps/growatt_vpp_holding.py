#!/usr/bin/env python3
"""
growatt_vpp_holding.py

Modbus Holding Register Map for Growatt VPP Protocol.
Based on "GROWATT VPP COMMUNICATION PROTOCOL OF INVERTER V2.01".
"""

# Block 1: 30000 - 30099
REG_HOLDING_VPP_30000_MAP = {
    "EquipmentType": (0, 1, 1, "uint"),
    "SerialNumber": (1, 15, 1, "ascii"),
    "RatedPower": (16, 2, 10, "uint32"),  # 0.1W -> scale 10
    "MaxActivePower": (18, 2, 10, "uint32"),
    "MaxReactivePowerToGrid": (20, 2, 10, "uint32"),
    "MaxReactivePowerFromGrid": (22, 2, 10, "uint32"),
    "MaxApparentPower": (24, 2, 10, "uint32"),
    "RatedChargeDischargePowerBDC": (26, 2, 10, "uint32"),
    "PVInputMaxPower": (28, 2, 10, "uint32"),
    "BatteryType": (30, 1, 1, "uint"),  # 0: lead acid, 1: lithium
    "MachineModel": (60, 1, 1, "ascii"),
    "DSP2SoftwareVersion": (71, 1, 1, "ascii"),
    "VPPProtocolVersion": (99, 1, 1, "uint"),
}

# Block 2: 30100 - 30199
REG_HOLDING_VPP_30100_MAP = {
    "ControlAuthority": (0, 1, 1, "uint"),
    "OnOffCommand": (1, 1, 1, "uint"),  # 0: off, 1: on
    # System Time
    "Year": (4, 1, 1, "uint"),
    "Month": (5, 1, 1, "uint"),
    "Day": (6, 1, 1, "uint"),
    "Hour": (7, 1, 1, "uint"),
    "Minute": (8, 1, 1, "uint"),
    "Second": (9, 1, 1, "uint"),
    "ActivePowerDerating": (51, 1, 1, "uint"),  # %
    "StaticActivePowerLimitation": (54, 1, 1, "uint"),  # %
    "EPSOfflineEnable": (55, 1, 1, "uint"),
    "EPSOfflineFrequency": (56, 1, 100, "uint"),  # 0.01Hz
    "EPSOfflineVoltage": (57, 1, 1, "uint"),
    "FixQ": (60, 1, 1, "uint"),  # %
    "ReactivePowerMode": (61, 1, 1, "uint"),
    "PowerFactor": (62, 1, 1, "uint"),
}

# Block 3: 30200 - 30299
REG_HOLDING_VPP_30200_MAP = {
    "ExportLimitationEnable": (0, 1, 1, "uint"),
    "ExportLimitationPowerRate": (1, 1, 1, "int"),  # %
    "ExportLimitationFailurePowerRate": (2, 1, 1, "uint"),  # %
    "SuperExportLimitationEnable": (5, 1, 1, "uint"),
    "ExportLimitationChangeSlope": (6, 1, 100, "uint"), 
    "ExportLimitationSinglePhaseControl": (7, 1, 1, "uint"),
    "ExportLimitationProtectionMode": (8, 1, 1, "uint"),
}

# Block 4: 30400 - 30499 (Battery Power Control)
REG_HOLDING_VPP_30400_MAP = {
    "ChargingCutOffSOC": (4, 1, 1, "uint"),  # %
    "OnlineDischargeCutOffSOC": (5, 1, 1, "uint"),  # %
    "LoadPriorityDischargeCutOffSOC": (6, 1, 1, "uint"),  # %
    "RemotePowerControlEnable": (7, 1, 1, "uint"),
    "RemotePowerControlChargingTime": (8, 1, 1, "uint"),  # min
    "RemoteChargeDischargePower": (9, 1, 1, "int"),  # % positive: charge, negative: discharge
    "ACChargingEnable": (10, 1, 1, "uint"),
    "ActualControlValueOfChargeDischargePower": (74, 1, 1, "int"),
    "OfflineDischargeCutOffSOC": (75, 1, 1, "uint"),  # %
    "BatteryChargeStopVoltage": (96, 1, 10, "uint"),  # 0.1V
    "BatteryDischargeStopVoltage": (97, 1, 10, "uint"),  # 0.1V
    "BatteryMaxChargeCurrent": (98, 1, 10, "uint"),  # 0.1A
    "BatteryMaxDischargeCurrent": (99, 1, 10, "uint"),  # 0.1A
}

# Write Map
REG_HOLDING_VPP_WRITE_MAP = {
    "OnOffCommand": 30101,
    "RemotePowerControlEnable": 30407,
    "RemoteChargeDischargePower": 30409,
    "ExportLimitationEnable": 30200,
    "ExportLimitationPowerRate": 30201,
}
