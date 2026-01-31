#!/usr/bin/env python3
"""
growatt_input_0.py

Modbus Input Register Map for Growatt Inverters.
Based on Protocol V1.24 - INPUT REGISTERS (Function Code 04).
Reference: Pages 48-56 (Ranges 0-124 and 125-249).

Tuple structure:
(Offset from index 0, Length in registers, Scaling factor, Type)
"""

REG_INPUT_0_MAP = {
    # =================================================================
    # GROUP 1: Inverter Basic Data (Registers 0-124)
    # =================================================================
    
    # 0: Inverter Status
    # 0:Waiting, 1:Normal, 3:Fault
    "InverterStatus": (0, 1, 1, "uint"),

    # 1-2: PV Input Power (Total) - 0.1W
    "PpvInput": (1, 2, 10, "uint32"),

    # --- PV1 (MPPT 1) ---
    "Vpv1": (3, 1, 10, "uint"),
    "Ipv1": (4, 1, 10, "uint"),
    "Ppv1": (5, 2, 10, "uint32"),

    # --- PV2 (MPPT 2) ---
    "Vpv2": (7, 1, 10, "uint"),
    "Ipv2": (8, 1, 10, "uint"),
    "Ppv2": (9, 2, 10, "uint32"),

    # --- PV3 to PV8 (if available) ---
    "Vpv3": (11, 1, 10, "uint"),
    "Ipv3": (12, 1, 10, "uint"),
    "Ppv3": (13, 2, 10, "uint32"),

    "Vpv4": (15, 1, 10, "uint"),
    "Ipv4": (16, 1, 10, "uint"),
    "Ppv4": (17, 2, 10, "uint32"),

    # Registers 19-34 continue for PV5-PV8...
    
    # --- Output (Grid) ---
    # 35-36: Output Active Power (Pac) - 0.1W
    "Pac": (35, 2, 10, "uint32"),

    # 37: Grid Frequency - 0.01Hz
    "Fac": (37, 1, 100, "uint"),

    # 38: Grid Voltage (Phase 1 / Single Phase) - 0.1V
    "Vac1": (38, 1, 10, "uint"),
    # 39: Grid Current (Phase 1) - 0.1A
    "Iac1": (39, 1, 10, "uint"),
    # 40-41: Apparent Power Phase 1 - 0.1VA
    "Pac1": (40, 2, 10, "uint32"),

    # 42: Grid Voltage Phase 2 - 0.1V
    "Vac2": (42, 1, 10, "uint"),
    # 43: Grid Current Phase 2 - 0.1A
    "Iac2": (43, 1, 10, "uint"),
    # 44-45: Apparent Power Phase 2 - 0.1VA
    "Pac2": (44, 2, 10, "uint32"),

    # 46: Grid Voltage Phase 3 - 0.1V
    "Vac3": (46, 1, 10, "uint"),
    # 47: Grid Current Phase 3 - 0.1A
    "Iac3": (47, 1, 10, "uint"),
    # 48-49: Apparent Power Phase 3 - 0.1VA
    "Pac3": (48, 2, 10, "uint32"),

    # 50-52: Line Voltages (RS, ST, TR) - 0.1V
    "Vac_RS": (50, 1, 10, "uint"),
    "Vac_ST": (51, 1, 10, "uint"),
    "Vac_TR": (52, 1, 10, "uint"),

    # --- Energy Statistics ---
    # 53-54: Energy AC Today - 0.1kWh
    "Eac_Today": (53, 2, 10, "uint32"),
    # 55-56: Energy AC Total - 0.1kWh
    "Eac_Total": (55, 2, 10, "uint32"),

    # 57-58: Total Work Time - 0.5s
    "WorkTimeTotal": (57, 2, 2, "uint32"),

    # 59-62: PV1 Energy Today/Total - 0.1kWh
    "Epv1_Today": (59, 2, 10, "uint32"),
    "Epv1_Total": (61, 2, 10, "uint32"),
    
    # 63-66: PV2 Energy Today/Total
    "Epv2_Today": (63, 2, 10, "uint32"),
    "Epv2_Total": (65, 2, 10, "uint32"),

    # Registers 67-90 continue for PV3-PV8 Energy...

    # 91-92: Total PV Energy (All strings) - 0.1kWh
    "Epv_Total": (91, 2, 10, "uint32"),

    # --- Temperatures & Bus Voltages ---
    # 93: Inverter Temperature - 0.1C
    "TempInverter": (93, 1, 10, "uint"),
    # 94: IPM Temperature (Internal Power Module) - 0.1C
    "TempIPM": (94, 1, 10, "uint"),
    # 95: Boost Temperature - 0.1C
    "TempBoost": (95, 1, 10, "uint"),

    # 98: Bus Voltage P (+) - 0.1V
    "VbusP": (98, 1, 10, "uint"),
    # 99: Bus Voltage N (-) - 0.1V
    "VbusN": (99, 1, 10, "uint"),

    # 100: Power Factor (0-20000)
    "IPF": (100, 1, 1, "uint"),

    # 101: Real Output Power Percent - 1%
    "RealOPPercent": (101, 1, 1, "uint"),

    # 104: Derating Mode
    # 0:No derate, 1:PV, 3:Vac, 4:Fac, 5:Tboost, 6:Tinv, 7:Control...
    "DeratingMode": (104, 1, 1, "uint"),

    # 105: Fault Main Code
    "FaultMain": (105, 1, 1, "uint"),
    # 107: Fault Sub Code
    "FaultSub": (107, 1, 1, "uint"),

    # 110: Warning Bit Map
    "WarningBitH": (110, 1, 1, "uint"),
    # 111: Warn Sub Code
    "WarnSub": (111, 1, 1, "uint"),
    # 112: Warn Main Code
    "WarnMain": (112, 1, 1, "uint"),
}

REG_INPUT_125_MAP = {

    # =================================================================
    # GROUP 2: PID, String Monitor & Extended Data (Registers 125-249)
    # =================================================================
    
    # --- PID Information (125-141) ---
    # 125: PID PV1+ Voltage - 0.1V
    "PID_Vpv1": (125, 1, 10, "uint"),
    # 126: PID PV1+ Current - 0.1mA (Signed: -10 to 10mA)
    "PID_Ipv1": (126, 1, 10, "int"), 
    
    # ... (PID PV2-PV8 follows pattern +2 offset)

    # 141: PID Status (0-3)
    # Bit0-7: Status (1:Wait, 2:Normal, 3:Fault)
    "PID_Status": (141, 1, 1, "uint"),

    # --- String Monitoring (142-173) ---
    # Note: These are individual strings, not MPPTs.
    
    # 142: String 1 Voltage - 0.1V
    "V_String1": (142, 1, 10, "uint"),
    # 143: String 1 Current - 0.1A (Signed: -15 to 15A)
    "I_String1": (143, 1, 10, "int"),
    
    "V_String2": (144, 1, 10, "uint"),
    "I_String2": (145, 1, 10, "int"),
    
    "V_String3": (146, 1, 10, "uint"),
    "I_String3": (147, 1, 10, "int"),
    
    "V_String4": (148, 1, 10, "uint"),
    "I_String4": (149, 1, 10, "int"),
    
    # ... continues up to String 16 (Register 173) ...
    
    # 174: String Unmatch Status (Bitmask for Strings 1-16)
    "StringUnmatch": (174, 1, 1, "uint"),
    
    # 177: PID Fault Code (Bitmask)
    # Bit0: OverVolt, Bit1: ISO Fault, Bit2: Bus Volt Abnormal
    "PID_FaultCode": (177, 1, 1, "uint"),

    # --- Extended Power & Debug (182+) ---
    
    # 230-231: Output Apparent Power (Sac) - 0.1VA
    "Sac": (230, 2, 10, "uint32"),

    # 232-233: Real Output Reactive Power - 0.1Var
    # (Often signed int32, as reactive power can be negative)
    "Qac_Real": (232, 2, 10, "int32"),

    # 236-237: Reactive Power Generation Total - 0.1kVarh
    "E_Reactive_Total": (236, 2, 10, "uint32"),

    # 238: AFCI Status (Arc Fault Circuit Interrupter)
    # 0:Waiting, 1:SelfCheck, 2:Detecting, 3:Fault
    "AFCI_Status": (238, 1, 1, "uint"),
}