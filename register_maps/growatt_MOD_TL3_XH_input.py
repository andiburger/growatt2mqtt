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
    "InverterStatus": (0, 1, 1, "uint"),
    "PpvInput": (1, 2, 10, "uint32"),
    "Vpv1": (3, 1, 10, "uint"),
    "Ipv1": (4, 1, 10, "uint"),
    "Ppv1": (5, 2, 10, "uint32"),
    "Vpv2": (7, 1, 10, "uint"),
    "Ipv2": (8, 1, 10, "uint"),
    "Ppv2": (9, 2, 10, "uint32"),
    "Vpv3": (11, 1, 10, "uint"),
    "Ipv3": (12, 1, 10, "uint"),
    "Ppv3": (13, 2, 10, "uint32"),
    "Vpv4": (15, 1, 10, "uint"),
    "Ipv4": (16, 1, 10, "uint"),
    "Ppv4": (17, 2, 10, "uint32"),
    "Psys": (19, 2, 10, "uint32"),
    "Qac": (21, 2, 10, "uint32"),
    "Pac": (23, 2, 10, "uint32"),
    "Fac": (25, 1, 100, "uint"),
    "Vac1": (26, 1, 10, "uint"),
    "Iac1": (27, 1, 10, "uint"),
    "Pac1": (28, 2, 10, "uint32"),
    "Vac2": (30, 1, 10, "uint"),
    "Iac2": (31, 1, 10, "uint"),
    "Pac2": (32, 2, 10, "uint32"),
    "Vac3": (34, 1, 10, "uint"),
    "Iac3": (35, 1, 10, "uint"),
    "Pac3": (36, 2, 10, "uint32"),
    "Vac_RS": (38, 1, 10, "uint"),
    "Vac_ST": (39, 1, 10, "uint"),
    "Vac_TR": (40, 1, 10, "uint"),
    "E_ToUser_Total": (41, 2, 10, "uint32"),
    "E_ToGrid_Total": (43, 2, 10, "uint32"),
    "E_Load_Total": (45, 2, 10, "uint32"),
    "WorkTimeTotal": (47, 2, 10, "uint32"),
    "Eac_Today": (49, 2, 10, "uint32"),
    "Eac_Total": (51, 2, 10, "uint32"),
    "Epv_Total": (53, 2, 10, "uint32"),
    "Epv1_Today": (55, 2, 10, "uint32"),
    "Epv1_Total": (57, 2, 10, "uint32"),
    "Epv2_Today": (59, 2, 10, "uint32"),
    "Epv2_Total": (61, 2, 10, "uint32"),
    "Epv3_Today": (63, 2, 10, "uint32"),
    "Epv3_Total": (65, 2, 10, "uint32"),
    "Epv4_Today": (67, 2, 10, "uint32"),
    "Epv4_Total": (69, 2, 10, "uint32"),
    "DeratingMode": (88, 1, 1, "uint"),
    "TempInverter": (89, 1, 10, "uint"),
    "TempIPM": (90, 1, 10, "uint"),
    "TempBoost": (91, 1, 10, "uint"),
    "FaultCode": (101, 1, 1, "uint"),
    "WarnCode": (102, 1, 1, "uint"),
}