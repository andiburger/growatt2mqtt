#!/usr/bin/env python3
"""
growatt_storage_spa_input.py

Modbus Input Register Map for Growatt Storage (SPA Type) Inverters.
Based on Protocol V1.24 - INPUT REGISTERS (Function Code 04).

Covered Ranges:
- 1000-1124: Storage / Hybrid Data (Battery, Energy Flow)
- 1125-1249: Extended Battery Info (Cell Voltages, BMS)
- 2000-2124: SPA Specific AC/Grid Data

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_INPUT_SPA_MAP = {
    # =================================================================
    # GROUP 1: Storage / Hybrid Data (1000-1124)
    # =================================================================
    
    # 1000: System Work Mode
    # 0:Waiting, 1:SelfTest, 3:Fault, 4:Flash, 5:PV+Bat, 6:BatOnly, 7:PVOnly, 8:BatOffline
    "SystemWorkMode": (1000, 1, 1, "uint"),

    # 1001-1008: System Fault Words (Bitmasks)
    "SysFaultWord0": (1001, 1, 1, "uint"),
    
    # 1009-1010: Discharge Power - 0.1W
    "Pdischarge": (1009, 2, 10, "uint32"),

    # 1011-1012: Charge Power - 0.1W
    "Pcharge": (1011, 2, 10, "uint32"),

    # 1013: Battery Voltage - 0.1V
    "Vbat": (1013, 1, 10, "uint"),

    # 1014: SOC (State of Charge) - 1%
    "SOC": (1014, 1, 1, "uint"),

    # 1021-1022: Power to User Total (Load) - 0.1W
    "P_ToUser_Total": (1021, 2, 10, "uint32"),

    # 1029-1030: Power to Grid Total (Export) - 0.1W
    "P_ToGrid_Total": (1029, 2, 10, "uint32"),

    # 1037-1038: Local Load Total - 0.1W
    "P_LocalLoad_Total": (1037, 2, 10, "uint32"),

    # 1040: Battery Temperature - 0.1C
    "TempBattery": (1040, 1, 10, "uint"),
    
    # 1041: DSP Status (0:Wait, 1:Normal, 2:Fault)
    "DSP_Status": (1041, 1, 1, "uint"),
    
    # 1042: Bus Voltage - 0.1V
    "Vbus": (1042, 1, 10, "uint"),

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

    # 1064-1065: Export Limit Apparent Power - 0.1VA
    "ExportLimitApparent": (1064, 2, 10, "uint32"),

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
    # GROUP 2: Extended Battery & System Info (1125-1249)
    # =================================================================
    
    # 1125-1126: AC Charge Energy Today - 0.1kWh
    "E_ACCharge_Today": (1125, 2, 10, "uint32"),
    # 1127-1128: AC Charge Energy Total - 0.1kWh
    "E_ACCharge_Total": (1127, 2, 10, "uint32"),

    # 1129-1130: AC Charge Power - 0.1W
    "P_ACCharge": (1129, 2, 10, "uint32"),
    
    # 1133-1134: Extra Inverter Energy To User Today - 0.1kWh
    "E_Extra_ToUser_Today": (1133, 2, 10, "uint32"),
    # 1135-1136: Extra Inverter Energy To User Total - 0.1kWh
    "E_Extra_ToUser_Total": (1135, 2, 10, "uint32"),

    # 1137-1138: System Energy Today - 0.1kWh
    "Esys_Today": (1137, 2, 10, "uint32"),
    # 1139-1140: System Energy Total - 0.1kWh
    "Esys_Total": (1139, 2, 10, "uint32"),

    # 1145-1146: System Power - 0.1W
    "Psystem": (1145, 2, 10, "uint32"),

    # 1200: Max Cell Voltage (Redundant?) - 0.001V
    "MaxCellVolt_Ext": (1200, 1, 1000, "uint"),
    # 1201: Min Cell Voltage - 0.001V
    "MinCellVolt_Ext": (1201, 1, 1000, "uint"),
    
    # 1206-1207: Max/Min Cell Temperature - 0.1C
    "MaxCellTemp": (1206, 1, 10, "uint"),
    "MinCellTemp": (1207, 1, 10, "uint"),
    
    # 1211-1212: Parallel Max/Min SOC - 1%
    "MaxSOC_Parallel": (1211, 1, 1, "uint"),
    "MinSOC_Parallel": (1212, 1, 1, "uint"),


    # =================================================================
    # GROUP 3: SPA Specific AC/Grid Data (2000-2124)
    # =================================================================
    
    # 2000: Inverter Status (SPA)
    "InverterStatus_SPA": (2000, 1, 1, "uint"),

    # 2035-2036: Output Power (Pac) - 0.1W
    "Pac_SPA": (2035, 2, 10, "uint32"),

    # 2037: Grid Frequency - 0.01Hz
    "Fac_SPA": (2037, 1, 100, "uint"),

    # 2038: Grid Voltage - 0.1V
    "Vac1_SPA": (2038, 1, 10, "uint"),
    
    # 2039: Grid Current - 0.1A
    "Iac1_SPA": (2039, 1, 10, "uint"),
    
    # 2040-2041: Output Apparent Power - 0.1VA
    "Pac1_SPA": (2040, 2, 10, "uint32"),

    # 2053-2054: Energy AC Today - 0.1kWh
    "Eac_Today_SPA": (2053, 2, 10, "uint32"),
    # 2055-2056: Energy AC Total - 0.1kWh
    "Eac_Total_SPA": (2055, 2, 10, "uint32"),

    # 2057-2058: Work Time Total - 0.5s
    "WorkTimeTotal_SPA": (2057, 2, 2, "uint32"),

    # 2093-2095: Temperatures - 0.1C
    "TempInverter_SPA": (2093, 1, 10, "uint"),
    "TempIPM_SPA": (2094, 1, 10, "uint"),
    "TempBoost_SPA": (2095, 1, 10, "uint"),

    # 2097: Battery Voltage (DSP) - 0.1V
    "Vbat_DSP": (2097, 1, 10, "uint"),

    # 2098: Bus Voltage P - 0.1V
    "VbusP_SPA": (2098, 1, 10, "uint"),
    # 2099: Bus Voltage N - 0.1V
    "VbusN_SPA": (2099, 1, 10, "uint"),

    # 2102-2103: Extra AC Power To Grid - 0.1W
    # Used when an external PV inverter is connected to the SPA
    "P_Extra_ToGrid": (2102, 2, 10, "uint32"),

    # 2104-2105: Extra Energy To User Today - 0.1kWh
    "E_Extra_ToUser_Today_SPA": (2104, 2, 10, "uint32"),

    # 2112-2113: AC Charge Energy Today - 0.1kWh
    "E_ACCharge_Today_SPA": (2112, 2, 10, "uint32"),
    
    # 2116-2117: Grid Power to Local Load - 0.1kWh ?? or W?
    # Doku says 0.1kWh but label says Power. Likely Power 0.1W.
    # Be careful here.
    "P_GridToLoad": (2116, 2, 10, "uint32"),

    # 2118: Priority (0:Load, 1:Bat, 2:Grid)
    "Priority_SPA": (2118, 1, 1, "uint"),
    
    # 2119: Battery Type (0:Lead, 1:Lithium)
    "BatteryType": (2119, 1, 1, "uint"),
}