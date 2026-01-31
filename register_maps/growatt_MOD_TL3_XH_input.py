REG_INPUT_MOD_TL3_XH_MAP = {
    # 3000: Status (Index 0)
    "InverterStatus": (0, 1, 1, "uint"),
    
    # 3001-3002: PV Leistung (Index 1, Länge 2)
    "PpvInput": (1, 2, 10, "uint32"),
    
    # 3003: Spannung (Index 3)
    "Vpv1": (3, 1, 10, "uint"),
    
    # 3004: Strom (Index 4)
    "Ipv1": (4, 1, 10, "uint"),
    
    # 3005-3006: PV1 Leistung (Index 5, Länge 2)
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
    "DeratingMode": (88, 1, 1, "uint"),
    "TempInverter": (89, 1, 10, "uint"),
    "TempIPM": (90, 1, 10, "uint"),
    "TempBoost": (91, 1, 10, "uint"),
    "FaultCode": (101, 1, 1, "uint"),
    "WarnCode": (102, 1, 1, "uint"),
}