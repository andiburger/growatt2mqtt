#!/usr/bin/env python3
"""
growatt_MAX_input.py

Modbus Input Register Map for Growatt MAX 1500V / MAX-X LV Inverters.
Based on Protocol V1.24 - INPUT REGISTERS (Function Code 04).
Reference: Pages 48-60.

Covered Ranges:
- 0-124: Basic Inverter Data (PV1-PV8, Grid, Energy)
- 125-249: String Monitor 1-16 & PID 1-8
- 875-999: Extended Data (PV9-PV16, String 17-32, PID 9-16)

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_INPUT_MAX_MAP = {
    # =================================================================
    # GROUP 1: Basic Inverter Data (0-124)
    # =================================================================
    
    # 0: Inverter Status
    "InverterStatus": (0, 1, 1, "uint"),

    # 1-2: PV Input Power (Total) - 0.1W
    "PpvInput": (1, 2, 10, "uint32"),

    # --- PV1 to PV8 Data (Voltage, Current, Power) ---
    # PV1
    "Vpv1": (3, 1, 10, "uint"),
    "Ipv1": (4, 1, 10, "uint"),
    "Ppv1": (5, 2, 10, "uint32"),
    # PV2
    "Vpv2": (7, 1, 10, "uint"),
    "Ipv2": (8, 1, 10, "uint"),
    "Ppv2": (9, 2, 10, "uint32"),
    # PV3
    "Vpv3": (11, 1, 10, "uint"),
    "Ipv3": (12, 1, 10, "uint"),
    "Ppv3": (13, 2, 10, "uint32"),
    # PV4
    "Vpv4": (15, 1, 10, "uint"),
    "Ipv4": (16, 1, 10, "uint"),
    "Ppv4": (17, 2, 10, "uint32"),
    # PV5
    "Vpv5": (19, 1, 10, "uint"),
    "Ipv5": (20, 1, 10, "uint"),
    "Ppv5": (21, 2, 10, "uint32"),
    # PV6
    "Vpv6": (23, 1, 10, "uint"),
    "Ipv6": (24, 1, 10, "uint"),
    "Ppv6": (25, 2, 10, "uint32"),
    # PV7
    "Vpv7": (27, 1, 10, "uint"),
    "Ipv7": (28, 1, 10, "uint"),
    "Ppv7": (29, 2, 10, "uint32"),
    # PV8
    "Vpv8": (31, 1, 10, "uint"),
    "Ipv8": (32, 1, 10, "uint"),
    "Ppv8": (33, 2, 10, "uint32"),

    # --- Output (Grid) Data ---
    # 35-36: Output Active Power (Pac) - 0.1W
    "Pac": (35, 2, 10, "uint32"),

    # 37: Grid Frequency - 0.01Hz
    "Fac": (37, 1, 100, "uint"),

    # 38-41: Phase 1 (R) Data
    "Vac1": (38, 1, 10, "uint"),
    "Iac1": (39, 1, 10, "uint"),
    "Pac1": (40, 2, 10, "uint32"),

    # 42-45: Phase 2 (S) Data
    "Vac2": (42, 1, 10, "uint"),
    "Iac2": (43, 1, 10, "uint"),
    "Pac2": (44, 2, 10, "uint32"),

    # 46-49: Phase 3 (T) Data
    "Vac3": (46, 1, 10, "uint"),
    "Iac3": (47, 1, 10, "uint"),
    "Pac3": (48, 2, 10, "uint32"),

    # 50-52: Line Voltages
    "Vac_RS": (50, 1, 10, "uint"),
    "Vac_ST": (51, 1, 10, "uint"),
    "Vac_TR": (52, 1, 10, "uint"),

    # --- Energy Statistics ---
    "Eac_Today": (53, 2, 10, "uint32"),
    "Eac_Total": (55, 2, 10, "uint32"),
    "WorkTimeTotal": (57, 2, 2, "uint32"),

    # --- PV Energy (PV1-PV8) ---
    # PV1
    "Epv1_Today": (59, 2, 10, "uint32"),
    "Epv1_Total": (61, 2, 10, "uint32"),
    # PV2
    "Epv2_Today": (63, 2, 10, "uint32"),
    "Epv2_Total": (65, 2, 10, "uint32"),
    # PV3
    "Epv3_Today": (67, 2, 10, "uint32"),
    "Epv3_Total": (69, 2, 10, "uint32"),
    # PV4
    "Epv4_Today": (71, 2, 10, "uint32"),
    "Epv4_Total": (73, 2, 10, "uint32"),
    # PV5
    "Epv5_Today": (75, 2, 10, "uint32"),
    "Epv5_Total": (77, 2, 10, "uint32"),
    # PV6
    "Epv6_Today": (79, 2, 10, "uint32"),
    "Epv6_Total": (81, 2, 10, "uint32"),
    # PV7
    "Epv7_Today": (83, 2, 10, "uint32"),
    "Epv7_Total": (85, 2, 10, "uint32"),
    # PV8
    "Epv8_Today": (87, 2, 10, "uint32"),
    "Epv8_Total": (89, 2, 10, "uint32"),

    # 91-92: PV Energy Total (Sum)
    "Epv_Total": (91, 2, 10, "uint32"),

    # --- Temperatures & Internal ---
    "TempInverter": (93, 1, 10, "uint"),
    "TempIPM": (94, 1, 10, "uint"),
    "TempBoost": (95, 1, 10, "uint"),
    
    "VbusP": (98, 1, 10, "uint"),
    "VbusN": (99, 1, 10, "uint"),

    "RealOPPercent": (101, 1, 1, "uint"),
    "DeratingMode": (104, 1, 1, "uint"),
    "FaultCode": (105, 1, 1, "uint"),
    "WarnCode": (110, 1, 1, "uint"),
}

REG_INPUT_MAX_STRING_MAP = {
    # =================================================================
    # GROUP 2: String Monitor 1-16 & PID 1-8 (125-249)
    # =================================================================
    
    # --- PID Data PV1-PV8 ---
    # PV1
    "PID_Vpv1": (125, 1, 10, "uint"),
    "PID_Ipv1": (126, 1, 10, "int"),
    # PV2
    "PID_Vpv2": (127, 1, 10, "uint"),
    "PID_Ipv2": (128, 1, 10, "int"),
    # ... (Pattern repeats for PV3-PV8)
    # PV8
    "PID_Vpv8": (139, 1, 10, "uint"),
    "PID_Ipv8": (140, 1, 10, "int"),
    
    "PID_Status": (141, 1, 1, "uint"),

    # --- String Monitor (String 1 - 16) ---
    # Note: Strings are distinct from MPPTs (PVx)
    "V_String1": (142, 1, 10, "uint"),
    "I_String1": (143, 1, 10, "int"),
    "V_String2": (144, 1, 10, "uint"),
    "I_String2": (145, 1, 10, "int"),
    # ...
    "V_String16": (172, 1, 10, "uint"),
    "I_String16": (173, 1, 10, "int"),

    "StringUnmatch_1_16": (174, 1, 1, "uint"),
    "StringCurrentUnbal_1_16": (175, 1, 1, "uint"),
    "StringDisconnect_1_16": (176, 1, 1, "uint"),
    "PID_FaultCode": (177, 1, 1, "uint"),
    
    # 230: Output Apparent Power
    "Sac": (230, 2, 10, "uint32"),
    "Qac_Real": (232, 2, 10, "int32"),
    "AFCI_Status": (238, 1, 1, "uint"),
}

REG_INPUT_MAX_DATA_MAP = {

    # =================================================================
    # GROUP 3: Extended MAX Data (PV9-PV16, String 17-32) (875-999)
    # =================================================================
    
    # --- PV9 to PV16 Data (Voltage, Current, Power) ---
    # PV9
    "Vpv9": (875, 1, 10, "uint"),
    "Ipv9": (876, 1, 10, "uint"),
    "Ppv9": (877, 2, 10, "uint32"),
    # PV10
    "Vpv10": (879, 1, 10, "uint"),
    "Ipv10": (880, 1, 10, "uint"),
    "Ppv10": (881, 2, 10, "uint32"),
    # PV11
    "Vpv11": (883, 1, 10, "uint"),
    "Ipv11": (884, 1, 10, "uint"),
    "Ppv11": (885, 2, 10, "uint32"),
    # PV12
    "Vpv12": (887, 1, 10, "uint"),
    "Ipv12": (888, 1, 10, "uint"),
    "Ppv12": (889, 2, 10, "uint32"),
    # PV13
    "Vpv13": (891, 1, 10, "uint"),
    "Ipv13": (892, 1, 10, "uint"),
    "Ppv13": (893, 2, 10, "uint32"),
    # PV14
    "Vpv14": (895, 1, 10, "uint"),
    "Ipv14": (896, 1, 10, "uint"),
    "Ppv14": (897, 2, 10, "uint32"),
    # PV15
    "Vpv15": (899, 1, 10, "uint"),
    "Ipv15": (900, 1, 10, "uint"),
    "Ppv15": (901, 2, 10, "uint32"),
    # PV16
    "Vpv16": (903, 1, 10, "uint"),
    "Ipv16": (904, 1, 10, "uint"),
    "Ppv16": (905, 2, 10, "uint32"),

    # --- PV9 to PV16 Energy Statistics (starts at 907) ---
    # PV9
    "Epv9_Today": (907, 2, 10, "uint32"),
    "Epv9_Total": (909, 2, 10, "uint32"),
    # PV10
    "Epv10_Today": (911, 2, 10, "uint32"),
    "Epv10_Total": (913, 2, 10, "uint32"),
    # PV11
    "Epv11_Today": (915, 2, 10, "uint32"),
    "Epv11_Total": (917, 2, 10, "uint32"),
    # PV12
    "Epv12_Today": (919, 2, 10, "uint32"),
    "Epv12_Total": (921, 2, 10, "uint32"),
    # PV13
    "Epv13_Today": (923, 2, 10, "uint32"),
    "Epv13_Total": (925, 2, 10, "uint32"),
    # PV14
    "Epv14_Today": (927, 2, 10, "uint32"),
    "Epv14_Total": (929, 2, 10, "uint32"),
    # PV15
    "Epv15_Today": (931, 2, 10, "uint32"),
    "Epv15_Total": (933, 2, 10, "uint32"),
    # PV16
    "Epv16_Today": (935, 2, 10, "uint32"),
    "Epv16_Total": (937, 2, 10, "uint32"),

    # --- PID Data PV9-PV16 (939-954) ---
    "PID_Vpv9": (939, 1, 10, "uint"),
    "PID_Ipv9": (940, 1, 10, "int"),
    # ...
    "PID_Vpv16": (953, 1, 10, "uint"),
    "PID_Ipv16": (954, 1, 10, "int"),

    # --- String Monitor (String 17 - 32) (955-986) ---
    "V_String17": (955, 1, 10, "uint"),
    "I_String17": (956, 1, 10, "int"),
    # ...
    "V_String32": (985, 1, 10, "uint"),
    "I_String32": (986, 1, 10, "int"),

    # --- Extended Status ---
    "StringUnmatch_17_32": (987, 1, 1, "uint"),
    "StringCurrentUnbal_17_32": (988, 1, 1, "uint"),
    "StringDisconnect_17_32": (989, 1, 1, "uint"),

    "PV_Warning_Val": (990, 1, 1, "uint"), # PV9-16 abnormal
    "StringWarning_1_16": (991, 1, 1, "uint"),
    "StringWarning_17_32": (992, 1, 1, "uint"),
    
    # 999: System Command
    "SystemCmd": (999, 1, 1, "uint"),
}