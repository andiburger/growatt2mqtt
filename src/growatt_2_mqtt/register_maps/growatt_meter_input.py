#!/usr/bin/env python3
"""
growatt_meter_input.py

Modbus Input Register Map for Growatt Smart Meters (Three Phase).
Supports Eastron SDM630 (Standard Growatt TPM) and Chint DTSU666.

Note regarding Parsing:
- Eastron SDM630 uses FLOAT32 (2 registers per value).
- Chint DTSU666 uses FLOAT32 (2 registers per value).
- You must ensure your parser handles 'float' type (IEEE 754).

Tuple structure:
(Offset from base index, Length in registers, Scaling factor, Type)
"""

# =================================================================
# MAP 1: Eastron SDM630 (Most common Growatt TPM)
# Base Address usually 0 (some docs say 30001 -> 0)
# =================================================================
REG_METER_EASTRON_MAP = {
    # --- Voltage ---
    "Voltage_L1": (0, 2, 1, "float"),
    "Voltage_L2": (2, 2, 1, "float"),
    "Voltage_L3": (4, 2, 1, "float"),

    # --- Current ---
    "Current_L1": (6, 2, 1, "float"),
    "Current_L2": (8, 2, 1, "float"),
    "Current_L3": (10, 2, 1, "float"),

    # --- Active Power (Watt) ---
    "Power_L1": (12, 2, 1, "float"),
    "Power_L2": (14, 2, 1, "float"),
    "Power_L3": (16, 2, 1, "float"),

    # --- Apparent Power (VA) ---
    "ApparentPower_L1": (18, 2, 1, "float"),
    "ApparentPower_L2": (20, 2, 1, "float"),
    "ApparentPower_L3": (22, 2, 1, "float"),

    # --- Reactive Power (Var) ---
    "ReactivePower_L1": (24, 2, 1, "float"),
    "ReactivePower_L2": (26, 2, 1, "float"),
    "ReactivePower_L3": (28, 2, 1, "float"),

    # --- Power Factor ---
    "PowerFactor_L1": (30, 2, 1, "float"),
    "PowerFactor_L2": (32, 2, 1, "float"),
    "PowerFactor_L3": (34, 2, 1, "float"),

    # --- Frequency ---
    "Frequency": (70, 2, 1, "float"),

    # --- Totals ---
    "TotalActivePower": (52, 2, 1, "float"),   # Positive = Import, Negative = Export? Check wiring.
    "TotalApparentPower": (56, 2, 1, "float"),
    "TotalReactivePower": (60, 2, 1, "float"),
    "TotalPowerFactor": (62, 2, 1, "float"),

    # --- Energy (kWh) ---
    "ImportActiveEnergy": (72, 2, 1, "float"),
    "ExportActiveEnergy": (74, 2, 1, "float"),
    "TotalActiveEnergy": (342, 2, 1, "float"), # Import + Export
}


# =================================================================
# MAP 2: Chint DTSU666 (Alternative Meter)
# Addresses are hex 0x2000 = 8192 decimal
# =================================================================
REG_METER_CHINT_MAP = {
    # --- Voltage ---
    "Voltage_L1": (8192, 2, 1, "float"), # 0x2000
    "Voltage_L2": (8194, 2, 1, "float"), # 0x2002
    "Voltage_L3": (8196, 2, 1, "float"), # 0x2004

    # --- Current ---
    "Current_L1": (8202, 2, 1, "float"), # 0x200A
    "Current_L2": (8204, 2, 1, "float"), # 0x200C
    "Current_L3": (8206, 2, 1, "float"), # 0x200E

    # --- Active Power (Watt) ---
    # Note: Chint often uses Pt = Total Active Power at 0x2012 ??
    # Individual phases might be at different offsets depending on specific DTSU version.
    # Common mapping for DTSU666-H (Huawei version differs, check specific manual!)
    
    # Standard Modbus DTSU666 often:
    "Power_L1": (8214, 2, 1, "float"), # 0x2016
    "Power_L2": (8216, 2, 1, "float"), # 0x2018
    "Power_L3": (8218, 2, 1, "float"), # 0x201A
    
    "TotalActivePower": (8212, 2, 1, "float"), # 0x2014

    # --- Reactive Power ---
    "TotalReactivePower": (8220, 2, 1, "float"), # 0x201C
    
    # --- Power Factor ---
    "TotalPowerFactor": (8228, 2, 1, "float"), # 0x2024

    # --- Frequency ---
    "Frequency": (8230, 2, 1, "float"), # 0x2026

    # --- Energy (kWh) ---
    # Active Energy Import (Imp)
    "ImportActiveEnergy": (16384, 2, 1, "float"), # 0x4000
    # Active Energy Export (Exp)
    "ExportActiveEnergy": (16394, 2, 1, "float"), # 0x400A
}