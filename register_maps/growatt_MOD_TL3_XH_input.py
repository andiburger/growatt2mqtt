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
"""
growatt_MOD_TL3_XH_input.py
Corrected Map with Dummy Register shift for new Firmware.
"""

REG_INPUT_MOD_TL3_XH_MAP = {
    # Offset 0: Status (Liest Register 3001)
    "InverterStatus": (0, 1, 1, "uint"),

    # Offset 1: DUMMY / Fehlercode (Liest Register 3002)
    # Dient nur dazu, den Shift zu korrigieren!
    "FaultCode_Internal": (1, 1, 1, "uint"),

    # Ab hier sind alle Indizes um 1 verschoben (im Vergleich zum Original)
    # PpvInput liest nun 3003+3004
    "PpvInput": (2, 2, 10, "uint32"),
    
    "Vpv1": (4, 1, 10, "uint"),
    "Ipv1": (5, 1, 10, "uint"),
    "Ppv1": (6, 2, 10, "uint32"),
    
    "Vpv2": (8, 1, 10, "uint"),
    "Ipv2": (9, 1, 10, "uint"),
    "Ppv2": (10, 2, 10, "uint32"),
    
    "Vpv3": (12, 1, 10, "uint"),
    "Ipv3": (13, 1, 10, "uint"),
    "Ppv3": (14, 2, 10, "uint32"),
    
    "Vpv4": (16, 1, 10, "uint"),
    "Ipv4": (17, 1, 10, "uint"),
    "Ppv4": (18, 2, 10, "uint32"),

    # System Power
    "Psys": (20, 2, 10, "uint32"),
    "Qac": (22, 2, 10, "uint32"), # Blindleistung?
    
    # AC Output
    "Pac": (24, 2, 10, "uint32"),
    "Fac": (26, 1, 100, "uint"),
    
    "Vac1": (27, 1, 10, "uint"),
    "Iac1": (28, 1, 10, "uint"),
    "Pac1": (29, 2, 10, "uint32"),
    
    "Vac2": (31, 1, 10, "uint"),
    "Iac2": (32, 1, 10, "uint"),
    "Pac2": (33, 2, 10, "uint32"),
    
    "Vac3": (35, 1, 10, "uint"),
    "Iac3": (36, 1, 10, "uint"),
    "Pac3": (37, 2, 10, "uint32"),
    
    # Grid Info (Hier war vorher Vac_RS oft verschoben)
    "Vac_RS": (39, 1, 10, "uint"),
    "Vac_ST": (40, 1, 10, "uint"),
    "Vac_TR": (41, 1, 10, "uint"), # Frequenz? Oder Spannung T-R?
    
    # Energy Data
    "E_ToUser_Total": (42, 2, 10, "uint32"),
    "E_ToGrid_Total": (44, 2, 10, "uint32"),
    "E_Load_Total": (46, 2, 10, "uint32"),
    
    "WorkTimeTotal": (48, 2, 10, "uint32"), # High count
    "Eac_Today": (50, 2, 10, "uint32"),
    "Eac_Total": (52, 2, 10, "uint32"),
    
    "Epv_Total": (54, 2, 10, "uint32"),
    "Epv1_Today": (56, 2, 10, "uint32"),
    "Epv1_Total": (58, 2, 10, "uint32"),
    
    "Epv2_Today": (60, 2, 10, "uint32"),
    "Epv2_Total": (62, 2, 10, "uint32"),
    
    "Epv3_Today": (64, 2, 10, "uint32"),
    "Epv3_Total": (66, 2, 10, "uint32"),
    
    "Epv4_Today": (68, 2, 10, "uint32"),
    "Epv4_Total": (70, 2, 10, "uint32"),
    
    # Status Codes (Verschoben von ~88 auf ~89/90)
    "DeratingMode": (89, 1, 1, "uint"),
    "TempInverter": (90, 1, 10, "uint"),
    "TempIPM": (91, 1, 10, "uint"),
    "TempBoost": (92, 1, 10, "uint"),
    
    "FaultCode": (102, 1, 1, "uint"), # Prüfen ob das passt, sonst Dummy
    "WarnCode": (103, 1, 1, "uint"),
}