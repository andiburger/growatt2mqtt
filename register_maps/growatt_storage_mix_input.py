#!/usr/bin/env python3
"""
growatt_storage_mix_input.py

Modbus Input Register Map for Growatt Storage (MIX Type) Inverters (e.g., SPH Series).
Based on Protocol V1.24 - INPUT REGISTERS (Function Code 04).

Covered Ranges:
- 0-124: Basic Inverter Data (PV, Grid, Status)
- 1000-1124: Storage / Hybrid Data (Battery, Energy Flow, BMS, EPS)

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_INPUT_MIX_MAP = {
    # =================================================================
    # GROUP 1: Basic Inverter Data (0-124)
    # =================================================================
    
    # 0: Inverter Status
    "InverterStatus": (0, 1, 1, "uint"),

    # 1-2: PV Input Power (Total) - 0.1W
    "PpvInput": (1, 2, 10, "uint32"),

    # --- PV1 Data ---
    "Vpv1": (3, 1, 10, "uint"),
    "Ipv1": (4, 1, 10, "uint"),
    "Ppv1": (5, 2, 10, "uint32"),

    # --- PV2 Data ---
    "Vpv2": (7, 1, 10, "uint"),
    "Ipv2": (8, 1, 10, "uint"),
    "Ppv2": (9, 2, 10, "uint32"),

    # 35-36: Output Active Power (Pac) - 0.1W
    "Pac": (35, 2, 10, "uint32"),

    # 37: Grid Frequency - 0.01Hz
    "Fac": (37, 1, 100, "uint"),

    # 38: Grid Voltage (Phase 1 / R) - 0.1V
    "Vac1": (38, 1, 10, "uint"),
    # 39: Grid Current (Phase 1 / R) - 0.1A
    "Iac1": (39, 1, 10, "uint"),
    # 40-41: Grid Power (Phase 1) - 0.1VA
    "Pac1": (40, 2, 10, "uint32"),

    # 42: Grid Voltage (Phase 2 / S) - 0.1V
    "Vac2": (42, 1, 10, "uint"),
    # 43: Grid Current (Phase 2 / S) - 0.1A
    "Iac2": (43, 1, 10, "uint"),
    # 44-45: Grid Power (Phase 2) - 0.1VA
    "Pac2": (44, 2, 10, "uint32"),

    # 46: Grid Voltage (Phase 3 / T) - 0.1V
    "Vac3": (46, 1, 10, "uint"),
    # 47: Grid Current (Phase 3 / T) - 0.1A
    "Iac3": (47, 1, 10, "uint"),
    # 48-49: Grid Power (Phase 3) - 0.1VA
    "Pac3": (48, 2, 10, "uint32"),

    # 53-54: Energy AC Today - 0.1kWh
    "Eac_Today": (53, 2, 10, "uint32"),
    # 55-56: Energy AC Total - 0.1kWh
    "Eac_Total": (55, 2, 10, "uint32"),

    # 57-58: Total Work Time - 0.5s
    "WorkTimeTotal": (57, 2, 2, "uint32"),

    # 59-62: PV1 Energy Today/Total - 0.1kWh
    "Epv1_Today": (59, 2, 10, "uint32"),
    "Epv1_Total": (61, 2, 10, "uint32"),

    # 63-66: PV2 Energy Today/Total - 0.1kWh
    "Epv2_Today": (63, 2, 10, "uint32"),
    "Epv2_Total": (65, 2, 10, "uint32"),

    # 91-92: PV Energy Total - 0.1kWh
    "Epv_Total": (91, 2, 10, "uint32"),

    # 93-95: Temperatures - 0.1C
    "TempInverter": (93, 1, 10, "uint"),
    "TempIPM": (94, 1, 10, "uint"),
    "TempBoost": (95, 1, 10, "uint"),

    # 101: Real Output Percent - 1%
    "RealOPPercent": (101, 1, 1, "uint"),

    # 105: Fault Main Code
    "FaultCode": (105, 1, 1, "uint"),   
}

REG_INPUT_MIX_H_MAP = {
    
    # =================================================================
    # GROUP 2: Storage / Hybrid Data (1000-1124)
    # =================================================================
    
    # 1000: System Work Mode
    # 0:Waiting, 1:SelfTest, 3:Fault, 4:Flash, 5:PV+Bat, 6:BatOnly, 7:PVOnly, 8:BatOffline
    "SystemWorkMode": (1000, 1, 1, "uint"),

    # 1001-1008: System Fault Words (Bitmasks)
    "SysFaultWord0": (1001, 1, 1, "uint"),
    "SysFaultWord1": (1002, 1, 1, "uint"),
    # ... (1003-1008 skipped for brevity, add if needed)

    # 1009-1010: Discharge Power - 0.1W
    "Pdischarge": (1009, 2, 10, "uint32"),

    # 1011-1012: Charge Power - 0.1W
    "Pcharge": (1011, 2, 10, "uint32"),

    # 1013: Battery Voltage - 0.1V
    "Vbat": (1013, 1, 10, "uint"),

    # 1014: SOC (State of Charge) - 1%
    "SOC": (1014, 1, 1, "uint"),

    # --- Power to User (Load) ---
    # 1015-1016: Power to User R - 0.1W
    "P_ToUser_R": (1015, 2, 10, "uint32"),
    # ... S and T phases skipped ...
    # 1021-1022: Power to User Total - 0.1W
    "P_ToUser_Total": (1021, 2, 10, "uint32"),

    # --- Power to Grid (Export) ---
    # 1023-1024: Power to Grid R - 0.1W
    "P_ToGrid_R": (1023, 2, 10, "uint32"),
    # ... S and T phases skipped ...
    # 1029-1030: Power to Grid Total - 0.1W
    "P_ToGrid_Total": (1029, 2, 10, "uint32"),

    # --- Local Load Power (Consumption) ---
    # 1031-1032: Local Load R - 0.1W
    "P_LocalLoad_R": (1031, 2, 10, "uint32"),
    # ... S and T phases skipped ...
    # 1037-1038: Local Load Total - 0.1W
    "P_LocalLoad_Total": (1037, 2, 10, "uint32"),

    # 1040: Battery Temperature - 0.1C
    "TempBattery": (1040, 1, 10, "uint"),

    # --- Energy Statistics (Storage) ---
    # 1044-1045: Energy To User Today - 0.1kWh
    "E_ToUser_Today": (1044, 2, 10, "uint32"),
    # 1046-1047: Energy To User Total - 0.1kWh
    "E_ToUser_Total": (1046, 2, 10, "uint32"),

    # 1048-1049: Energy To Grid Today - 0.1kWh
    "E_ToGrid_Today": (1048, 2, 10, "uint32"),
    # 1050-1051: Energy To Grid Total - 0.1kWh
    "E_ToGrid_Total": (1050, 2, 10, "uint32"),

    # 1052-1053: Discharge Energy Today - 0.1kWh
    "E_Discharge_Today": (1052, 2, 10, "uint32"),
    # 1054-1055: Discharge Energy Total - 0.1kWh
    "E_Discharge_Total": (1054, 2, 10, "uint32"),

    # 1056-1057: Charge Energy Today - 0.1kWh
    "E_Charge_Today": (1056, 2, 10, "uint32"),
    # 1058-1059: Charge Energy Total - 0.1kWh
    "E_Charge_Total": (1058, 2, 10, "uint32"),

    # 1060-1061: Local Load Energy Today - 0.1kWh
    "E_LocalLoad_Today": (1060, 2, 10, "uint32"),
    # 1062-1063: Local Load Energy Total - 0.1kWh
    "E_LocalLoad_Total": (1062, 2, 10, "uint32"),

    # --- UPS / EPS Information (1067-1081) ---
    # 1067: EPS Frequency - 0.01Hz
    "EPS_Fac": (1067, 1, 100, "uint"),
    
    # 1068: EPS Voltage R - 0.1V
    "EPS_Vac1": (1068, 1, 10, "uint"),
    # 1069: EPS Current R - 0.1A
    "EPS_Iac1": (1069, 1, 10, "uint"),
    # 1070-1071: EPS Power R - 0.1VA
    "EPS_Pac1": (1070, 2, 10, "uint32"),

    # 1080: Load Percent - 1%
    "EPS_LoadPercent": (1080, 1, 1, "uint"),

    # --- BMS Information (1082-1123) ---
    # 1083: BMS Status
    "BMS_Status": (1083, 1, 1, "uint"),
    
    # 1085: BMS Error Code
    "BMS_Error": (1085, 1, 1, "uint"),
    
    # 1086: BMS SOC - 1% (Redundant but from BMS directly)
    "BMS_SOC": (1086, 1, 1, "uint"),
    
    # 1087: BMS Voltage - 0.01V (Note scale!)
    "BMS_Vbat": (1087, 1, 100, "uint"),
    
    # 1088: BMS Current - 0.01A (Note scale!)
    "BMS_Ibat": (1088, 1, 100, "int"),

    # 1089: BMS Temperature - 0.1C
    "BMS_Temp": (1089, 1, 10, "uint"),

    # 1096: BMS SOH - 1%
    "BMS_SOH": (1096, 1, 1, "uint"),

    # 1108: Max Cell Voltage - 0.001V
    "BMS_MaxCellVolt": (1108, 1, 1000, "uint"),
    # 1109: Min Cell Voltage - 0.001V
    "BMS_MinCellVolt": (1109, 1, 1000, "uint"),

    # 1124: AC Charge Energy Today H (starts here) - 0.1kWh
    # Note: This often spans to 1125, careful with block reading boundaries.
    "E_ACCharge_Today": (1124, 2, 10, "uint32"),
}