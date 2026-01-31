#!/usr/bin/env python3
"""
growatt_input_3000.py

Modbus Input Register Map for Growatt Inverters (TL-X / TL-XH Series).
Based on Protocol V1.24 - INPUT REGISTERS (Function Code 04).
Reference: Pages 70-76 (Live Data).

Ranges:
- 3000-3124: Inverter Data (PV, Grid, Energy, Temp)
- 3125-3249: BDC / Battery Data (TL-XH Series only)

Tuple structure:
(Offset from 3000, Length in registers, Scaling factor, Type)
"""

REG_INPUT_MAP = {
    # =================================================================
    # BLOCK 1: Inverter Status & PV Input (3000-3020)
    # =================================================================
    
    # 3000: Inverter Status
    # 0:Waiting, 1:Normal, 3:Fault
    #Inverter run state
    # High 8 bits mode (specific mode)
    #0: Waiting module
    #1: Self-test mode, optional
    #2: Reserved
    #3：SysFault module
    #4: Flash module
    #5：PVBATOnline module:
    #6：BatOnline module
    #7：PVOfflineMode
    #8：BatOfflineMode
    #The lower 8 bits indicate the machine
    # status (web page display)
    #0: StandbyStatus;
    #1: NormalStatus;
    #3: FaultStatus
    #4：FlashStatus;
    "InverterStatus": (0, 1, 1, "uint"),

    # 3001-3002: PV Input Power (Total) - 0.1W
    "PpvInput": (1, 2, 10, "uint32"),

    # 3003: PV1 Voltage - 0.1V
    "Vpv1": (3, 1, 10, "uint"),
    # 3004: PV1 Current - 0.1A
    "Ipv1": (4, 1, 10, "uint"),
    # 3005-3006: PV1 Power - 0.1W
    "Ppv1": (5, 2, 10, "uint32"),

    # 3007: PV2 Voltage - 0.1V
    "Vpv2": (7, 1, 10, "uint"),
    # 3008: PV2 Current - 0.1A
    "Ipv2": (8, 1, 10, "uint"),
    # 3009-3010: PV2 Power - 0.1W
    "Ppv2": (9, 2, 10, "uint32"),

    # 3011: PV3 Voltage - 0.1V
    "Vpv3": (11, 1, 10, "uint"),
    # 3012: PV3 Current - 0.1A
    "Ipv3": (12, 1, 10, "uint"),
    # 3013-3014: PV3 Power - 0.1W
    "Ppv3": (13, 2, 10, "uint32"),

    # 3015: PV4 Voltage - 0.1V
    "Vpv4": (15, 1, 10, "uint"),
    # 3016: PV4 Current - 0.1A
    "Ipv4": (16, 1, 10, "uint"),
    # 3017-3018: PV4 Power - 0.1W
    "Ppv4": (17, 2, 10, "uint32"),

    # 3019-3020: System Output Power (Psys) - 0.1W
    "Psys": (19, 2, 10, "uint32"),

    # 3021-3022: Reactive Power (Qac) - 0.1Var
    "Qac": (21, 2, 10, "uint32"),  # Note: Can be signed int32?

    # 3023-3024: Output Power (Pac) - 0.1W
    "Pac": (23, 2, 10, "uint32"),

    # 3025: Grid Frequency - 0.01Hz
    "Fac": (25, 1, 100, "uint"),

    # 3026: Grid Voltage (Phase 1 / R) - 0.1V
    "Vac1": (26, 1, 10, "uint"),
    # 3027: Grid Current (Phase 1 / R) - 0.1A
    "Iac1": (27, 1, 10, "uint"),
    # 3028-3029: Grid Output Power (Phase 1 / R) - 0.1VA
    "Pac1": (28, 2, 10, "uint32"),

    # 3030: Grid Voltage (Phase 2 / S) - 0.1V
    "Vac2": (30, 1, 10, "uint"),
    # 3031: Grid Current (Phase 2 / S) - 0.1A
    "Iac2": (31, 1, 10, "uint"),
    # 3032-3033: Grid Output Power (Phase 2 / S) - 0.1VA
    "Pac2": (32, 2, 10, "uint32"),

    # 3034: Grid Voltage (Phase 3 / T) - 0.1V
    "Vac3": (34, 1, 10, "uint"),
    # 3035: Grid Current (Phase 3 / T) - 0.1A
    "Iac3": (35, 1, 10, "uint"),
    # 3036-3037: Grid Output Power (Phase 3 / T) - 0.1VA
    "Pac3": (36, 2, 10, "uint32"),

    # 3038-3040: Line Voltages (RS, ST, TR) - 0.1V
    "Vac_RS": (38, 1, 10, "uint"),
    "Vac_ST": (39, 1, 10, "uint"),
    "Vac_TR": (40, 1, 10, "uint"),

    # 3041-3042: Total Forward Power (ToUser) - 0.1W
    "P_ToUser_Total": (41, 2, 10, "uint32"),

    # 3043-3044: Total Reverse Power (ToGrid) - 0.1W
    "P_ToGrid_Total": (43, 2, 10, "uint32"),

    # 3045-3046: Total Load Power - 0.1W
    "P_Load_Total": (45, 2, 10, "uint32"),

    # 3047-3048: Total Work Time - 0.5s
    "WorkTimeTotal": (47, 2, 2, "uint32"), # Scale 2 means value/2 = seconds? Check parser.

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

    # 3059-3066: PV2/PV3 Energy Today/Total (Skipping for brevity, similar pattern)
    
    # 3067-3068: Energy To User Today - 0.1kWh
    "E_ToUser_Today": (67, 2, 10, "uint32"),
    # 3069-3070: Energy To User Total - 0.1kWh
    "E_ToUser_Total": (69, 2, 10, "uint32"),
    
    # 3071-3072: Energy To Grid Today - 0.1kWh
    "E_ToGrid_Today": (71, 2, 10, "uint32"),
    # 3073-3074: Energy To Grid Total - 0.1kWh
    "E_ToGrid_Total": (73, 2, 10, "uint32"),

    # 3075-3076: Energy Load Today - 0.1kWh
    "E_Load_Today": (75, 2, 10, "uint32"),
    # 3077-3078: Energy Load Total - 0.1kWh
    "E_Load_Total": (77, 2, 10, "uint32"),
    
    # 3086: Derating Mode (Enum)
    "DeratingMode": (86, 1, 1, "uint"),

    # 3087: ISO Value (1 kOhm)
    "ISO": (87, 1, 1, "uint"),

    # 3092: Bus Voltage (0.1V)
    "Vbus": (92, 1, 10, "uint"),

    # 3093-3095: Temperatures (0.1C)
    "Temp_Inverter": (93, 1, 10, "uint"),
    "Temp_IPM": (94, 1, 10, "uint"),
    "Temp_Boost": (95, 1, 10, "uint"),

    # 3101: Real Output Percent (1%)
    "RealOPPercent": (101, 1, 1, "uint"),

    # 3105: Fault Main Code
    "FaultMain": (105, 1, 1, "uint"),
    # 3106: Warning Main Code
    "WarnMain": (106, 1, 1, "uint"),
    
    # 3123-3124: System Energy Today (0.1kWh)
    "Esys_Today": (123, 2, 10, "uint32"),
}

REG_INPUT_BAT_MAP = {
    # =================================================================
    # BLOCK 2: Battery / BDC Data (3125 - 3249) - TL-XH
    # =================================================================

    # 3125-3126: Battery Discharge Energy Today - 0.1kWh
    "Ebat_Discharge_Today": (125, 2, 10, "uint32"),
    # 3127-3128: Battery Discharge Energy Total - 0.1kWh
    "Ebat_Discharge_Total": (127, 2, 10, "uint32"),

    # 3129-3130: Battery Charge Energy Today - 0.1kWh
    "Ebat_Charge_Today": (129, 2, 10, "uint32"),
    # 3131-3132: Battery Charge Energy Total - 0.1kWh
    "Ebat_Charge_Total": (131, 2, 10, "uint32"),

    # 3133-3134: AC Charge Energy Today - 0.1kWh
    "E_ACCharge_Today": (133, 2, 10, "uint32"),
    # 3135-3136: AC Charge Energy Total - 0.1kWh
    "E_ACCharge_Total": (135, 2, 10, "uint32"),

    # 3137-3138: System Energy Total - 0.1kWh
    "Esys_Total": (137, 2, 10, "uint32"),

    # 3139-3140: Self-Use Energy Today - 0.1kWh
    "E_SelfUse_Today": (139, 2, 10, "uint32"),
    # 3141-3142: Self-Use Energy Total - 0.1kWh
    "E_SelfUse_Total": (141, 2, 10, "uint32"),

    # 3144: Priority Mode
    # 0:LoadFirst, 1:BatFirst, 2:GridFirst
    "PriorityMode": (144, 1, 1, "uint"),

    # --- EPS (Emergency Power Supply) Data ---
    # 3145: EPS Frequency - 0.01Hz
    "EPS_Fac": (145, 1, 100, "uint"),
    # 3146: EPS Voltage Phase 1 - 0.1V
    "EPS_Vac1": (146, 1, 10, "uint"),
    # 3147: EPS Current Phase 1 - 0.1A
    "EPS_Iac1": (147, 1, 10, "uint"),
    # 3148-3149: EPS Power Phase 1 - 0.1VA
    "EPS_Pac1": (148, 2, 10, "uint32"),
    
    # 3158-3159: EPS Total Power - 0.1VA
    "EPS_Pac_Total": (158, 2, 10, "uint32"),

    # 3160: Load Percent (UPS) - 1% (or 0.1%?)
    "EPS_LoadPercent": (160, 1, 1, "uint"),

    # 3165: BDC Derating Mode
    "BDC_DeratingMode": (165, 1, 1, "uint"),

    # 3180-3181: Battery Charge Power - 0.1W
    "Pbat_Charge": (180, 2, 10, "uint32"),

    # 3200: BMS Gauge FCC (Ah)
    "BMS_FCC": (200, 1, 1, "uint"),
    # 3201: BMS Gauge RM (Ah)
    "BMS_RM": (201, 1, 1, "uint"),

    # 3210: Battery ISO Status
    "Bat_ISO_Status": (210, 1, 1, "uint"),

    # 3212: BMS Status
    # 0:Dormancy, 1:Charge, 2:Discharge, ...
    "BMS_Status": (212, 1, 1, "uint"),

    # 3215: BMS SOC - 1%
    "SOC": (215, 1, 1, "uint"),

    # 3216: BMS Battery Voltage - 0.01V
    "BMS_Vbat": (216, 1, 100, "uint"),

    # 3217: BMS Battery Current - 0.01A
    "BMS_Ibat": (217, 1, 100, "uint"), # Often signed int!

    # 3218: BMS Temperature - 0.1C
    "BMS_Temp": (218, 1, 10, "uint"),

    # 3222: BMS SOH - 1%
    "SOH": (222, 1, 1, "uint"),

    # 3232: Battery Load Voltage - 0.01V
    "Bat_Load_Voltage": (232, 1, 100, "uint"),
}