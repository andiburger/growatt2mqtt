"""
growatt_TLXH_min_input.py

Modbus Input Register Map for Growatt TL-X / TL-XH / TL-XH US (MIN Type).
Based on Protocol V1.24 - INPUT REGISTERS (Function Code 04).

Covered Ranges:
- 3000-3124: Basic Inverter Data
- 3125-3249: Battery / BDC 1 Data (TL-XH)
- 3250-3374: Battery / BDC 2 Data (TL-XH Extended)

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

REG_INPUT_TLXH_MIN_MAP = {
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

    # --- PV3 Data (if available) ---
    "Vpv3": (11, 1, 10, "uint"),
    "Ipv3": (12, 1, 10, "uint"),
    "Ppv3": (13, 2, 10, "uint32"),

    # --- PV4 Data (if available) ---
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

    # 3026: Grid Voltage (Phase 1 / R) - 0.1V
    "Vac1": (26, 1, 10, "uint"),
    # 3027: Grid Current (Phase 1 / R) - 0.1A
    "Iac1": (27, 1, 10, "uint"),
    # 3028-3029: Grid Power (Phase 1) - 0.1VA
    "Pac1": (28, 2, 10, "uint32"),

    # 3030: Grid Voltage (Phase 2 / S) - 0.1V
    "Vac2": (30, 1, 10, "uint"),
    # 3031: Grid Current (Phase 2 / S) - 0.1A
    "Iac2": (31, 1, 10, "uint"),
    # 3032-3033: Grid Power (Phase 2) - 0.1VA
    "Pac2": (32, 2, 10, "uint32"),

    # 3034: Grid Voltage (Phase 3 / T) - 0.1V
    "Vac3": (34, 1, 10, "uint"),
    # 3035: Grid Current (Phase 3 / T) - 0.1A
    "Iac3": (35, 1, 10, "uint"),
    # 3036-3037: Grid Power (Phase 3) - 0.1VA
    "Pac3": (36, 2, 10, "uint32"),

    # 3038-3040: Line Voltages
    "Vac_RS": (38, 1, 10, "uint"),
    "Vac_ST": (39, 1, 10, "uint"),
    "Vac_TR": (40, 1, 10, "uint"),

    # 3041-3042: Energy To User Total - 0.1kWh
    # Note: Sometimes labeled differently, check specific manual if unsure
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

    # 3063-3066: PV3 Energy Today/Total
    "Epv3_Today": (63, 2, 10, "uint32"),
    "Epv3_Total": (65, 2, 10, "uint32"),

    # 3067-3070: PV4 Energy Today/Total
    "Epv4_Today": (67, 2, 10, "uint32"),
    "Epv4_Total": (69, 2, 10, "uint32"),
    
    # 3086: Derating Mode
    "DeratingMode": (86, 1, 1, "uint"),

    # 3087: ISO Resistance - 1kOhm
    "ISO": (87, 1, 1, "uint"),
    
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
    "Esys_Today": (123, 2, 10, "uint32"),


    # =================================================================
    # GROUP 2: Battery / BDC 1 Data (3125-3249)
    # =================================================================

    # 3125: BDC Status
    # 0:Wait, 1:SelfCheck, 2:Normal, 3:Fault, 4:Flash
    "BDC1_Status": (125, 1, 1, "uint"),

    # 3126: BDC Mode
    # 0:Idle, 1:Discharge, 2:Charge
    "BDC1_Mode": (126, 1, 1, "uint"),

    # 3127: Battery Voltage - 0.1V
    "Vbat": (127, 1, 10, "uint"),

    # 3128: Battery Current - 0.1A (Signed)
    "Ibat": (128, 1, 10, "int"),

    # 3129: SOC - 1%
    "SOC": (129, 1, 1, "uint"),

    # 3130: SOH - 1%
    "SOH": (130, 1, 1, "uint"),

    # 3131-3132: Battery Power - 0.1W (Signed)
    # Discharge > 0, Charge < 0
    "Pbat": (131, 2, 10, "int32"),

    # 3133-3134: Charge Energy Today - 0.1kWh
    "Ebat_Charge_Today": (133, 2, 10, "uint32"),
    
    # 3135-3136: Discharge Energy Today - 0.1kWh
    "Ebat_Discharge_Today": (135, 2, 10, "uint32"),

    # 3137-3138: Charge Energy Total - 0.1kWh
    "Ebat_Charge_Total": (137, 2, 10, "uint32"),
    
    # 3139-3140: Discharge Energy Total - 0.1kWh
    "Ebat_Discharge_Total": (139, 2, 10, "uint32"),

    # 3143: BMS Status
    "BMS_Status": (143, 1, 1, "uint"),

    # 3144: Priority Mode
    # 0:Load First, 1:Bat First, 2:Grid First
    "PriorityMode": (144, 1, 1, "uint"),

    # --- EPS (Emergency Power Supply) Data (3169+) ---
    # 3169: EPS Voltage - 0.1V
    "Veps": (169, 1, 10, "uint"),
    # 3170: EPS Frequency - 0.01Hz
    "Feps": (170, 1, 100, "uint"),
    # 3171-3172: EPS Power - 0.1W
    "Peps": (171, 2, 10, "uint32"),
    
    # 3200: BMS FCC (Ah)
    "BMS_FCC": (200, 1, 1, "uint"),
    # 3201: BMS RM (Ah)
    "BMS_RM": (201, 1, 1, "uint"),

    # 3216: BMS Battery Voltage - 0.01V
    "BMS_Vbat": (216, 1, 100, "uint"),
    # 3217: BMS Battery Current - 0.01A
    "BMS_Ibat": (217, 1, 100, "int"),
    # 3218: BMS Temperature - 0.1C
    "BMS_Temp": (218, 1, 10, "uint"),


    # =================================================================
    # GROUP 3: Battery / BDC 2 Data (3250-3374) (Extended)
    # =================================================================

    # 3250: PV Inverter 1 Output Power (High) - 0.1W
    # Note: Sometimes used for external PV inverters in AC coupling
    "Pex1": (250, 2, 10, "uint32"),

    # 3254: PV Inverter 1 Energy Today - 0.1kWh
    "Eex1_Today": (254, 2, 10, "uint32"),
    # 3258: PV Inverter 1 Energy Total - 0.1kWh
    "Eex1_Total": (258, 2, 10, "uint32"),

    # 3262: Battery Pack Number
    "BatPackNum": (262, 1, 1, "uint"),

    # --- Second Battery Pack / BDC Data (starts around 3280+) ---
    # Be aware: Map structure for 2nd battery often mirrors the 1st
    # but offsets vary by firmware version. Common mapping:
    
    # 3280: BDC2 Charge Power - 0.1W
    "BDC2_Pcharge": (280, 2, 10, "uint32"),
    
    # 3282: BDC2 Discharge Energy Total - 0.1kWh
    "BDC2_Edischr_Total": (282, 2, 10, "uint32"),
    
    # 3284: BDC2 Charge Energy Total - 0.1kWh
    "BDC2_Echr_Total": (284, 2, 10, "uint32"),

    # 3288: Vbus2 - 0.1V
    "Vbus2": (288, 1, 10, "uint"),

    # 3313: BMS2 Status
    "BMS2_Status": (313, 1, 1, "uint"),

    # 3315: BMS2 SOC - 1%
    "BMS2_SOC": (315, 1, 1, "uint"),

    # 3316: BMS2 Voltage - 0.01V
    "BMS2_Vbat": (316, 1, 100, "uint"),
    
    # 3317: BMS2 Current - 0.01A
    "BMS2_Ibat": (317, 1, 100, "int"),

    # 3322: BMS2 SOH - 1%
    "BMS2_SOH": (322, 1, 1, "uint"),
}