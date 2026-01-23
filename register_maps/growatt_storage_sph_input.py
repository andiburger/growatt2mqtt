#!/usr/bin/env python3
"""
growatt_storage_sph_input.py

Modbus Input Register Map for Growatt Storage (SPH Type) Inverters.
Based on Protocol V1.24 - INPUT REGISTERS (Function Code 04).

Covered Ranges:
- 0-124: Basic Inverter Data
- 1000-1124: Storage / Hybrid Data
- 1125-1249: Extended Battery / System Info

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_INPUT_SPH_MAP = {
    # =================================================================
    # GROUP 1: Basic Inverter Data (0-124)
    # =================================================================
    
    # 0: Inverter Status
    "InverterStatus": (0, 1, 1, "uint"),

    # 1-2: PV Input Power (Total) - 0.1W
    "PpvInput": (1, 2, 10, "uint32"),

    # --- PV1 ---
    "Vpv1": (3, 1, 10, "uint"),
    "Ipv1": (4, 1, 10, "uint"),
    "Ppv1": (5, 2, 10, "uint32"),

    # --- PV2 ---
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

    # 93: Inverter Temp - 0.1C
    "TempInverter": (93, 1, 10, "uint"),
    
    # 94: IPM Temp - 0.1C
    "TempIPM": (94, 1, 10, "uint"),
    
    # 101: Real Output Percent - 1%
    "RealOPPercent": (101, 1, 1, "uint"),

    # 105: Fault Main Code
    "FaultCode": (105, 1, 1, "uint"),


    # =================================================================
    # GROUP 2: Storage / Hybrid Data (1000-1124)
    # =================================================================
    
    # 1000: System Work Mode
    "SystemWorkMode": (1000, 1, 1, "uint"),

    # 1009-1010: Discharge Power - 0.1W
    "Pdischarge": (1009, 2, 10, "uint32"),

    # 1011-1012: Charge Power - 0.1W
    "Pcharge": (1011, 2, 10, "uint32"),

    # 1013: Battery Voltage - 0.1V
    "Vbat": (1013, 1, 10, "uint"),

    # 1014: SOC (State of Charge) - 1%
    "SOC": (1014, 1, 1, "uint"),

    # 1021-1022: Power to User Total (Home Consumption) - 0.1W
    "P_ToUser_Total": (1021, 2, 10, "uint32"),

    # 1029-1030: Power to Grid Total (Export/Import) - 0.1W
    "P_ToGrid_Total": (1029, 2, 10, "uint32"),

    # 1037-1038: Local Load Total (Backup Load) - 0.1W
    "P_LocalLoad_Total": (1037, 2, 10, "uint32"),

    # 1040: Battery Temperature - 0.1C
    "TempBattery": (1040, 1, 10, "uint"),

    # --- Energy Statistics ---
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
    "EPS_Fac": (1067, 1, 100, "uint"), # 0.01Hz
    "EPS_Vac1": (1068, 1, 10, "uint"), # 0.1V
    "EPS_Iac1": (1069, 1, 10, "uint"), # 0.1A
    "EPS_Pac1": (1070, 2, 10, "uint32"), # 0.1VA
    
    "EPS_LoadPercent": (1080, 1, 1, "uint"), # 1%

    # --- BMS Information (1082-1123) ---
    "BMS_Status": (1083, 1, 1, "uint"),
    "BMS_Error": (1085, 1, 1, "uint"),
    "BMS_SOC": (1086, 1, 1, "uint"),
    "BMS_Vbat": (1087, 1, 100, "uint"), # 0.01V
    "BMS_Ibat": (1088, 1, 100, "int"),  # 0.01A
    "BMS_Temp": (1089, 1, 10, "uint"),  # 0.1C
    "BMS_SOH": (1096, 1, 1, "uint"),
    
    # 1108: Max Cell Voltage - 0.001V
    "BMS_MaxCellVolt": (1108, 1, 1000, "uint"),
    # 1109: Min Cell Voltage - 0.001V
    "BMS_MinCellVolt": (1109, 1, 1000, "uint"),
    

    # =================================================================
    # GROUP 3: Extended System Info (1125-1249)
    # =================================================================
    
    # 1125-1126: AC Charge Energy Today - 0.1kWh
    "E_ACCharge_Today": (1125, 2, 10, "uint32"),
    # 1127-1128: AC Charge Energy Total - 0.1kWh
    "E_ACCharge_Total": (1127, 2, 10, "uint32"),

    # 1129-1130: AC Charge Power - 0.1W
    "P_ACCharge": (1129, 2, 10, "uint32"),
    
    # 1137-1138: System Energy Today (Overall) - 0.1kWh
    "Esys_Today": (1137, 2, 10, "uint32"),
    # 1139-1140: System Energy Total (Overall) - 0.1kWh
    "Esys_Total": (1139, 2, 10, "uint32"),
    
    # 1141-1142: Self-Consumption Energy Today - 0.1kWh
    "E_Self_Today": (1141, 2, 10, "uint32"),
    # 1143-1144: Self-Consumption Energy Total - 0.1kWh
    "E_Self_Total": (1143, 2, 10, "uint32"),

    # 1145-1146: System Power - 0.1W
    "Psystem": (1145, 2, 10, "uint32"),
    
    # 1147-1148: Self-Consumption Power - 0.1W
    "Pself": (1147, 2, 10, "uint32"),

    # 1200: Max Cell Voltage (Extended) - 0.001V
    "MaxCellVolt_Ext": (1200, 1, 1000, "uint"),
    # 1201: Min Cell Voltage (Extended) - 0.001V
    "MinCellVolt_Ext": (1201, 1, 1000, "uint"),

    # 1206: Max Cell Temp - 0.1C
    "MaxCellTemp": (1206, 1, 10, "uint"),
    # 1207: Min Cell Temp - 0.1C
    "MinCellTemp": (1207, 1, 10, "uint"),
}