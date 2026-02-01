#!/usr/bin/env python3
"""
growatt_MOD_TL3_XH_holding.py

Modbus Holding Register Map for Growatt MOD TL3-XH Inverters.
Based on "New-Modbus.RS485.RTU.Protocal.Latest.Ver.pdf" (V1.24)

Covers two main ranges:
1. Basic Settings:    0 - 124   (Pages 9-15)
2. Advanced Settings: 3000 - 3124 (Pages 35-42) - Critical for XH Battery & Time

Tuple structure: (Offset, Length, Scale, Type)
"""

# ==============================================================================
# MAP 1: BASIC SETTINGS (Register 0 - 124)
# Basis-Adresse für read_block: 0
# ==============================================================================
REG_HOLDING_MOD_TL3_XH_BASIC = {
    # --- System Control ---
    # Register 0: 0=Off, 1=On
    "OnOff": (0, 1, 1, "uint"),
    
    # Register 1: Grid Standard (e.g. VDE0126)
    "GridStandard": (1, 1, 1, "uint"),
    
    # --- Power Limits ---
    # Register 3: Active Power (0-100%)
    "ActivePowerRate": (3, 1, 1, "uint"),
    
    # Register 4: Reactive Power (0-100%)
    "ReactivePowerRate": (4, 1, 1, "uint"),
    
    # Register 5: Power Factor (0-10000, 10000=1.0)
    "PowerFactor": (5, 1, 10000, "uint"),
    
    # --- Grid Protection Settings (Wichtig für Diagnose) ---
    # Register 17: PV Start Voltage (e.g. 160V)
    "VpvStart": (17, 1, 10, "uint"),
    
    # Register 18-21: Grid Voltage/Freq Limits
    "GridVoltLow": (18, 1, 10, "uint"),
    "GridVoltHigh": (19, 1, 10, "uint"),
    "GridFreqLow": (20, 1, 100, "uint"),
    "GridFreqHigh": (21, 1, 100, "uint"),
    
    # --- Communication ---
    # Register 30: Modbus Address
    "ComAddress": (30, 1, 1, "uint"),
    
    # --- Restart ---
    # Register 64: Auto Restart (0=Disable, 1=Enable)
    "AutoRestart": (64, 1, 1, "uint"),
}


# ==============================================================================
# MAP 2: ADVANCED / BATTERY (Register 3000 - 3124)
# Basis-Adresse für read_block: 3000
# Alle Offsets sind relativ zu 3000! (z.B. Register 3025 -> Offset 25)
# ==============================================================================
REG_HOLDING_MOD_TL3_XH_ADVANCED = {
    # --- Export Limit Settings ---
    # Register 3000: Power rate when Export Limit fails
    "ExportLimitFailedPowerRate": (0, 1, 10, "uint"),

    # --- System Info (New Area for XH) ---
    # Register 3001-3015: Serial Number (30 Chars ASCII)
    "SerialNumber": (1, 15, 1, "ascii"),
    
    # Register 3016-3020: Model Number (10 Chars ASCII)
    "ModelNumber": (16, 5, 1, "ascii"),
    
    # Register 3021-3024: Firmware Version (8 Chars ASCII)
    "FirmwareVersion": (21, 4, 1, "ascii"),

    # --- System Time (RTC) ---
    # Register 3025-3030
    "Year": (25, 1, 1, "uint"),      # 2000-2099
    "Month": (26, 1, 1, "uint"),
    "Day": (27, 1, 1, "uint"),
    "Hour": (28, 1, 1, "uint"),
    "Minute": (29, 1, 1, "uint"),
    "Second": (30, 1, 1, "uint"),

    # --- General Settings ---
    # Register 3031: Language
    "Language": (31, 1, 1, "uint"),

    # --- Export Limit Control ---
    # Register 3038: Enable (0/1)
    "ExportLimitEnable": (38, 1, 1, "uint"),
    
    # Register 3039: Rate (0-100%)
    "ExportLimitRate": (39, 1, 1, "uint"),
    
    # Register 3040: Fail Safe Enable
    "ExportLimitFailSafe": (40, 1, 1, "uint"),

    # --- BATTERY MANAGEMENT (BDC) - WICHTIG! ---
    
    # Register 3047: Battery Priority
    # 0 = Load First (Standard)
    # 1 = Battery First
    # 2 = Grid First
    "BatPriority": (47, 1, 1, "uint"),

    # Register 3049: Max Charge Power %
    "BatChargePowerLimit": (49, 1, 1, "uint"),
    
    # Register 3050: Max Discharge Power %
    "BatDischargePowerLimit": (50, 1, 1, "uint"),

    # --- AC Charge Settings (Laden aus dem Netz) ---
    
    # Register 3070: AC Charge Enable (Globally)
    "ACChargeEnable": (70, 1, 1, "uint"),
    
    # Time Slot 1 (Register 3055-3059)
    "ACChargeTime1_StartH": (55, 1, 1, "uint"),
    "ACChargeTime1_StartM": (56, 1, 1, "uint"),
    "ACChargeTime1_EndH": (57, 1, 1, "uint"),
    "ACChargeTime1_EndM": (58, 1, 1, "uint"),
    "ACChargeTime1_Enable": (59, 1, 1, "uint"),

    # Time Slot 2 (Register 3060-3064)
    "ACChargeTime2_StartH": (60, 1, 1, "uint"),
    "ACChargeTime2_StartM": (61, 1, 1, "uint"),
    "ACChargeTime2_EndH": (62, 1, 1, "uint"),
    "ACChargeTime2_EndM": (63, 1, 1, "uint"),
    "ACChargeTime2_Enable": (64, 1, 1, "uint"),

    # Time Slot 3 (Register 3065-3069)
    "ACChargeTime3_StartH": (65, 1, 1, "uint"),
    "ACChargeTime3_StartM": (66, 1, 1, "uint"),
    "ACChargeTime3_EndH": (67, 1, 1, "uint"),
    "ACChargeTime3_EndM": (68, 1, 1, "uint"),
    "ACChargeTime3_Enable": (69, 1, 1, "uint"),
    
    # --- Battery Type ---
    # Register 3080: 0=Lead-acid, 1=Lithium
    "BatType": (80, 1, 1, "uint"),
}