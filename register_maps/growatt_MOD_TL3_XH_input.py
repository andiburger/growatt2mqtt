#!/usr/bin/env python3
"""
growatt_MOD_TL3_XH_input.py

Modbus Input Register Map for Growatt MOD TL3-XH Inverters.
(3-Phase Battery Ready Hybrid Inverters).
Based on Protocol V1.24 - INPUT REGISTERS (Function Code 04).

Covered Ranges:
- 3000-3124: Basic Inverter Data (PV, Grid 3-Phase, Energy)
- 3125-3249: Battery / BDC Data (XH Series)

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_INPUT_MOD_TL3_XH_MAP = {
    # =================================================================
    # GROUP 1: Inverter Data (3000-3124)
    # =================================================================
    
    # 3000: Inverter Status
    # Low Byte: Status (0:Wait, 1:Normal, 3:Fault), High Byte: Mode
    "InverterStatus": (0, 1, 1, "uint"),

    # 3001-3002: PV Input Power (Total) - 0.1W
    "PpvInput": (1, 2, 10, "uint32"),

    # --- PV1 Data ---
    "Vpv1": (3, 1, 10, "uint"),
    "Ipv1": (4, 1, 10, "uint"),
    "Ppv1": (5, 2, 10, "uint32"),

    # --- PV2 Data ---
    "Vpv2": (7, 1, 10, "uint"),
    "Ipv2": (8, 1, 10, "uint"),
    "Ppv2": (9, 2, 10, "uint32"),

    # --- PV3 Data (Usually only 2 MPPTs on MOD, but mapping exists) ---
    "Vpv3": (11, 1, 10, "uint"),
    "Ipv3": (12, 1, 10, "uint"),
    "Ppv3": (13, 2, 10, "uint32"),

    # --- PV4 Data ---
    "Vpv4": (15, 1, 10, "uint"),
    "Ipv4": (16, 1, 10, "uint"),
    "Ppv4": (17, 2, 10, "uint32"),

    # 3019-3020: System Output Power - 0.1W
    "Psys": (19, 2, 10, "uint32"),

    # 3021-3022: Reactive Power - 0.1Var
    "Qac": (21, 2, 10, "int32"),

    # 3023-3024: Output Active Power (Pac) - 0.1W
    "Pac": (23, 2, 10, "uint32"),

    # 3025: Grid Frequency - 0.01Hz
    "Fac": (25, 1, 100, "uint"),

    # --- Phase 1 (R) Data ---
    "Vac1": (26, 1, 10, "uint"),
    "Iac1": (27, 1, 10, "uint"),
    "Pac1": (28, 2, 10, "uint32"),

    # --- Phase 2 (S) Data ---
    "Vac2": (30, 1, 10, "uint"),
    "Iac2": (31, 1, 10, "uint"),
    "Pac2": (32, 2, 10, "uint32"),

    # --- Phase 3 (T) Data ---
    "Vac3": (34, 1, 10, "uint"),
    "Iac3": (35, 1, 10, "uint"),
    "Pac3": (36, 2, 10, "uint32"),

    # 3038-3040: Line Voltages (L-L)
    "Vac_RS": (38, 1, 10, "uint"),
    "Vac_ST": (39, 1, 10, "uint"),
    "Vac_TR": (40, 1, 10, "uint"),

    # 3041-3042: Energy To User Total - 0.1kWh
    "E_ToUser_Total": (41, 2, 10, "uint32"),
    
    # 3043-3044: Energy To Grid Total - 0.1kWh
    "E_ToGrid_Total": (43, 2, 10, "uint32"),

    # 3045-3046: Energy Load Total - 0.1kWh
    "E_Load_Total": (45, 2, 10, "uint32"),

    # 3047-3048: Total Work Time - 0.5s
    "WorkTimeTotal": (47, 2, 2, "uint32"),

    # 3049-3050: Energy AC Today - 0.1kWh
    "Eac_Today": (49, 2, 10, "uint32"),
    # 3051-3052: Energy AC Total - 0.1kWh
    "Eac_Total": (51, 2, 10, "uint32"),

    # 3053-3054: PV Energy Total - 0.1kWh
    "Epv_Total": (53, 2, 10, "uint32"),

    # 3055-3056: PV1 Energy Today - 0.1kWh
    "Epv1_Today": (55, 2, 10, "uint32"),
    # 3057-3058: PV1 Energy Total - 0.1kWh
    "Epv1_Total": (57, 2, 10, "uint32"),

    # 3059-3062: PV2 Energy Today/Total
    "Epv2_Today": (59, 2, 10, "uint32"),
    "Epv2_Total": (61, 2, 10, "uint32"),
    
    # 3086: Derating Mode
    "DeratingMode": (86, 1, 1, "uint"),
    
    # 3093: Inverter Temperature - 0.1C
    "TempInverter": (93, 1, 10, "uint"),
    # 3094: IPM Temperature - 0.1C
    "TempIPM": (94, 1, 10, "uint"),
    # 3095: Boost Temperature - 0.1C
    "TempBoost": (95, 1, 10, "uint"),

    # 3105: Fault Main Code
    "FaultCode": (105, 1, 1, "uint"),
    # 3106: Warning Main Code
    "WarnCode": (106, 1, 1, "uint"),

    # 3123-3124: System Energy Today - 0.1kWh
    "Esys_Today": (123, 2, 10, "uint32")
}

REG_INPUT_MOD_TL3_XH_BAT_MAP = {
    # =================================================================
    # GROUP 2: Battery / BDC Data (3125-3249)
    # =================================================================

    # 3125: BDC Status
    # 0:Wait, 1:SelfCheck, 2:Normal, 3:Fault, 4:Flash
    "BDC_Status": (0, 1, 1, "uint"),

    # 3126: BDC Mode
    # 0:Idle, 1:Discharge, 2:Charge
    "BDC_Mode": (1, 1, 1, "uint"),

    # 3127: Battery Voltage - 0.1V
    "Vbat": (2, 1, 10, "uint"),

    # 3128: Battery Current - 0.1A (Signed)
    "Ibat": (3, 1, 10, "int"),

    # 3129: SOC - 1%
    "SOC": (4, 1, 1, "uint"),

    # 3130: SOH - 1%
    "SOH": (5, 1, 1, "uint"),

    # 3131-3132: Battery Power - 0.1W (Signed)
    # Discharge > 0, Charge < 0
    "Pbat": (6, 2, 10, "int32"),

    # 3133-3134: Charge Energy Today - 0.1kWh
    "Ebat_Charge_Today": (8, 2, 10, "uint32"),
    
    # 3135-3136: Discharge Energy Today - 0.1kWh
    "Ebat_Discharge_Today": (10, 2, 10, "uint32"),

    # 3137-3138: Charge Energy Total - 0.1kWh
    "Ebat_Charge_Total": (12, 2, 10, "uint32"),
    
    # 3139-3140: Discharge Energy Total - 0.1kWh
    "Ebat_Discharge_Total": (14, 2, 10, "uint32"),

    # 3143: BMS Status
    "BMS_Status": (18, 1, 1, "uint"),

    # 3144: Priority Mode
    # 0:Load First, 1:Bat First, 2:Grid First
    "PriorityMode": (19, 1, 1, "uint"),
}