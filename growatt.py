#!/usr/bin/env python3
"""
Python Module to implement ModBus RTU connection to Growatt Inverters
"""
import logging
from growatt_TLXH_input_reg import REG_INPUT_MAP as TLXH_REG_INPUT_MAP
from growatt_TL3X_MAX_MID_MAC_MIC_input_reg import REG_INPUT_0_MAP as TL3X_REG_INPUT_MAP
from pymodbus.exceptions import ModbusIOException
from time import sleep
import struct

# Codes
StateCodes = {0: "Waiting", 1: "Normal", 3: "Fault"}

BatteryType = {0: "Lead-acid", 1: "Lithium battery"}

ErrorCodes = {
    0: "None",
    24: "Auto Test Failed",
    25: "No AC Connection",
    26: "PV Isolation Low",
    27: "Residual Current High",
    28: "DC Current High",
    29: "PV Voltage High",
    30: "AC Voltage Outrange",
    31: "AC Freq Outrange",
    32: "Module Hot",
}

for i in range(1, 24):
    ErrorCodes[i] = "Error Code: %s" % str(99 + i)

DeratingMode = {
    0: "No Deratring",
    1: "PV",
    2: "",
    3: "Vac",
    4: "Fac",
    5: "Tboost",
    6: "Tinv",
    7: "Control",
    8: "*LoadSpeed",
    9: "*OverBackByTime",
}

PIDStatus = {1: "Wait Status", 2: "Normal Status", 3: "Fault Status"}


def read_single(row, index, unit=10):
    """reads a value from 1 ModBus register"""
    return float(row.registers[index]) / unit


def read_double(row, index, unit=10):
    """reads values consists of 2 ModBus register"""
    return float((row.registers[index] << 16) + row.registers[index + 1]) / unit


def merge(*dict_args):
    """merges dictionaries"""
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def read_from_map(row, base_index, reg_map):
    """
    Parses a block of Modbus registers based on a provided map.
    
    :param row: The response object from pymodbus (containing .registers)
    :param base_index: The starting register address of the 'row' block (e.g., 3000)
    :param reg_map: The dictionary defining the registers
    :return: A dictionary with parsed values
    """
    results = {}
    
    # Check if we have registers
    if not hasattr(row, 'registers') or not row.registers:
        return {}

    for name, (offset, length, scale, dtype) in reg_map.items():
        # --- Read and Parse Each Register According to the Map ---
        if offset + length > len(row.registers):
            # Out of bounds, skip
            continue

        # extract raw data
        regs = row.registers[offset: offset + length]

        val = 0

        # type-specific parsing
        if dtype == "ascii":
            # ASCII Decoding 
            try:
                # each regiser (16-bit) contains 2 characters
                byte_data = b"".join(struct.pack(">H", r) for r in regs)
                val = byte_data.decode("ascii").strip("\x00")  # remove padding null chars
            except Exception:
                val = str(regs)  # Fallback

        elif dtype == "uint32":
            # 32-Bit Unsigned (High Word First)
            val = (regs[0] << 16) + regs[1]
        
        elif dtype == "int32":
            # 32-Bit Signed (High Word First)
            val = (regs[0] << 16) + regs[1]
            if val > 0x7FFFFFFF:  # Negative Value Adjustment
                val -= 0x100000000

        elif dtype == "int":
            # 16-Bit Signed
            val = regs[0]
            if val > 0x7FFF:
                val -= 0x10000

        else:
            # Default: "uint" (16-Bit Unsigned)
            val = regs[0]

        if scale != 1 and isinstance(val, (int, float)):
            val = float(val) / scale

        results[name] = val

    return results


def parse_inverter_status(value):
    """
    Parses the 16-bit value from InverterStatus register (3000)
    into Status (Lower 8 Bits) and Mode (Higher 8 Bits).
    
    :param value: The raw integer value read from register 3000
    :return: A tuple (status, mode)
    """
    # Lower 8 Bits: Machine Status (e.g., 0=Standby, 1=Normal, 3=Fault)
    # 0xFF is 11111111 in binary. The AND operation masks out the upper bits.
    status = value & 0xFF
    
    # Higher 8 Bits: Run Mode (e.g., 5=PVBATOnline, 6=BatOnline)
    # Shift right by 8 bits to move the high byte to the low position, then mask.
    mode = (value >> 8) & 0xFF
    
    return status, mode

    # --- Usage Example ---
    # Assume the value read from register 3000 is 1281
    # 1281 decimal = 0000 0101 0000 0001 binary
    # High Byte (Mode) = 5 (PVBATOnline)
    # Low Byte (Status) = 1 (Normal)


class Growatt:
    """Class Growatt implements ModBus RTU protocol for growatt inverters"""

    def __init__(self, client, name, unit, protocol_version, log=None):
        self.client = client
        self.name = name
        self.unit = unit
        self.protocol_version = protocol_version
        if log is not None:
            self.__log = log
        else:
            self.__log = logging.getLogger("growatt2mqtt_log")
            self.__log.setLevel(logging.DEBUG)
            if not self.__log.handlers:
                ch = logging.StreamHandler()
                ch.setFormatter(
                    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
                )
                self.__log.addHandler(ch)
        try:
            self.read_info()
        except ModbusIOException:
            self.__log.warning("Inverter not reachable, will retry every hour.")
        for i in range(10):
            sleep(3600)
            try:
                self.read_info()
                self.__log.info("Inverter connection re-established.")
                break
            except ModbusIOException:
                self.__log.warning(f"Retry {i+1}/10 failed, inverter still offline.")
        else:
            self.__log.error(
                "Inverter not reachable after 10 retries. Continuing without data."
            )
            self.modbus_version = None

    def read_info(self):
        """reads holding registers from Growatt inverters"""
        row = self.client.read_holding_registers(73, unit=self.unit)
        if row.isError():
            raise ModbusIOException

        self.modbus_version = row.registers[0]

    def print_info(self):
        """prints basic information about the current Growatt inverter"""
        self.__log.info("Growatt:")
        self.__log.info("\tName: %s\n", str(self.name))
        self.__log.info("\tUnit: %s\n", str(self.unit))
        self.__log.info("\tModbus Version: %s\n", str(self.modbus_version))

    def read(self):
        """this function reads based on the given ModBus RTU protocol version the ModBus data from growatt inverters"""
        if self.protocol_version == "MAXSeries":
            self.__log.info("MAX Series Protocol\n")
            row = self.client.read_input_registers(0, 117, unit=self.unit)
            if row.isError():
                self.__log.error(row.__str__)
                return None
            info = {  # ==================================================================
                # N/A,      Inverter Status,    Inverter run state
                "StatusCode": row.registers[0],
                "Status": StateCodes[row.registers[0]],
                # 0.1W,     Ppv H,              Input power (high)
                "Ppv": read_double(row, 1),
                # 0.1W,     Ppv L,              Input power (low)
                # 0.1V,     Vpv1,               PV1 voltage
                "Vpv1": read_single(row, 3),
                # 0.1A,     PV1Curr,            PV1 input current
                "PV1Curr": read_single(row, 4),
                # 0.1W,     PV1Watt H,          PV1 input power (high)
                "PPV1InPwr": read_double(row, 5),
                # 0.1W,     PV1Watt L,          PV1 input power (low)
                # 0.1V,     Vpv2,               PV2 voltage
                "Vpv2": read_single(row, 7),
                # 0.1A,     PV2Curr,            PV2 input current
                "PV2Curr": read_single(row, 8),
                # 0.1W,     PV2Watt H,          PV2 input watt (high)
                "PPV2inPwr": read_double(row, 9),
                # 0.1W,     PV2Watt L,          PV2 input watt (low)
                # 0.1V,     Vpv3,               PV3 voltage
                "Vpv3": read_single(row, 11),
                # 0.1A,     PV3Curr,            PV3 input current
                "PV3Curr": read_single(row, 12),
                # 0.1W,     PV3Watt H,          PV3 input watt (high)
                "PPV3inPwr": read_double(row, 13),
                # 0.1W,     PV3Watt L,          PV3 input watt (low)
                # 0.1V,     Vpv4,               PV4 voltage
                "Vpv4": read_single(row, 15),
                # 0.1A,     PV4Curr,            PV4 input current
                "PV4Curr": read_single(row, 16),
                # 0.1W,     PV4Watt H,          PV4 input watt (high)
                "PPV4inPwr": read_double(row, 17),
                # 0.1W,     PV4Watt L,          PV4 input watt (low)
                # 0.1V,     Vpv5,               PV5 voltage
                "Vpv5": read_single(row, 19),
                # 0.1A,     PV5Curr,            PV5 input current
                "PV5Curr": read_single(row, 20),
                # 0.1W,     PV5Watt H,          PV5 input watt (high)
                "PPV5inPwr": read_double(row, 21),
                # 0.1W,     PV5Watt L,          PV5 input watt (low)
                # 0.1V,     Vpv6,               PV6 voltage
                "Vpv6": read_single(row, 23),
                # 0.1A,     PV6Curr,            PV6 input current
                "PV6Curr": read_single(row, 24),
                # 0.1W,     PV6Watt H,          PV6 input watt (high)
                "PPV6inPwr": read_double(row, 25),
                # 0.1W,     PV6Watt L,          PV6 input watt (low)
                # 0.1V,     Vpv7,               PV7 voltage
                "Vpv7": read_single(row, 27),
                # 0.1A,     PV7Curr,            PV7 input current
                "PV7Curr": read_single(row, 28),
                # 0.1W,     PV7Watt H,          PV7 input watt (high)
                "PPV7inPwr": read_double(row, 29),
                # 0.1W,     PV7Watt L,          PV7 input watt (low)
                # 0.1V,     Vpv8,               PV8 voltage
                "Vpv8": read_single(row, 31),
                # 0.1A,     PV8Curr,            PV8 input current
                "PV8Curr": read_single(row, 32),
                # 0.1W,     PV8Watt H,          PV8 input watt (high)
                "PPV8inPwr": read_double(row, 33),
                # 0.1W,     PV8Watt L,          PV8 input watt (low)
                # 0.1W,     Pac H,              Output power (high)
                "Pac": read_double(row, 35),
                # 0.1W,     Pac L,              Output power (low)
                # 0.01Hz,   Fac,                Grid frequency
                "Fac": read_single(row, 37, 100),
                # 0.1V,  Vac1,               Three/single phase grid voltage
                "Vac1": read_single(row, 38),
                # 0.1A,  Iac1,               Three/single phase grid output current
                "Iac1": read_single(row, 39),
                # 0.1VA , Pac1 H,             Three/single phase grid output watt (high)
                "Pac1H": read_double(row, 40),
                # 0.1VA, Pac1 L,
                # 0.1V   Vac2                  Three phase grid voltage
                "Vac2": read_single(row, 42),
                # 0.1A,  Iac2,               Three/single phase grid output current
                "Iac2": read_single(row, 43),
                # 0.1VA , Pac2 H,             Three/single phase grid output watt (high)
                "Pac2H": read_double(row, 44),
                # 0.1VA, Pac2 L,
                # 0.1V   Vac3                  Three phase grid voltage
                "Vac3": read_single(row, 46),
                # 0.1A,  Iac3,               Three/single phase grid output current
                "Iac3": read_single(row, 47),
                # 0.1VA , Pac3 H,             Three/single phase grid output watt (high)
                "Pac3H": read_double(row, 48),
                # 0.1VA, Pac3 L,
                # 0.1V   VacRS                  Three phase grid voltage
                "VacRS": read_single(row, 50),
                # 0.1V   VacST                  Three phase grid voltage
                "VacST": read_single(row, 51),
                # 0.1V   VacTR                  Three phase grid voltage
                "VacTR": read_single(row, 52),
                # 0.1kWH   Eac today H         Today generate energy (high)
                "PVPowerToday": read_double(row, 53),
                # 0.1kWH        Eac today L       Today generate energy (low)
                # 0.1kWH   Eac total H         Total generate energy (high)
                "PVPowerTotal": read_double(row, 55),
                # 0.1kWH        Eac total L       Total generate energy (low)
                # ,      # 0.5s   Time total H         Work time total (high)
                "TimeTotal": read_double(row, 57),
                # 0.5s   Time total L       Work time total (low)
                "Epv1Today": read_double(
                    row, 59
                ),  # 0.1kWH   Epv1_today H         PV1 Energy today (high)
                # 0.1kWH        Epv1_today L       PV1 Energy today (low)
                "Epv1Total": read_double(
                    row, 61
                ),  # 0.1kWH   Epv1_total H         PV1 Energy total (high)
                # 0.1kWH        Epv1_total L       PV1 Energy total (low)
                "Epv2Today": read_double(
                    row, 63
                ),  # 0.1kWH   Epv2_today H         PV2 Energy today (high)
                # 0.1kWH        Epv2_today L       PV2 Energy today (low)
                "Epv2Total": read_double(
                    row, 65
                ),  # 0.1kWH   Epv2_total H         PV2 Energy total (high)
                # 0.1kWH        Epv2_total L       PV2 Energy total (low)
                "Epv3Today": read_double(
                    row, 67
                ),  # 0.1kWH   Epv3_today H         PV3 Energy today (high)
                # 0.1kWH        Epv3_today L       PV3 Energy today (low)
                "Epv3Total": read_double(
                    row, 69
                ),  # 0.1kWH   Epv3_total H         PV3 Energy total (high)
                # 0.1kWH        Epv3_total L       PV3 Energy total (low)
                "Epv4Today": read_double(
                    row, 71
                ),  # 0.1kWH   Epv4_today H         PV4 Energy today (high)
                # 0.1kWH        Epv4_today L       PV4 Energy today (low)
                "Epv4Total": read_double(
                    row, 73
                ),  # 0.1kWH   Epv4_total H         PV4 Energy total (high)
                # 0.1kWH        Epv4_total L       PV4 Energy total (low)
                "Epv5Today": read_double(
                    row, 75
                ),  # 0.1kWH   Epv5_today H         PV5 Energy today (high)
                # 0.1kWH        Epv5_today L       PV5 Energy today (low)
                "Epv5Total": read_double(
                    row, 77
                ),  # 0.1kWH   Epv5_total H         PV5 Energy total (high)
                # 0.1kWH        Epv5_total L       PV5 Energy total (low)
                "Epv6Today": read_double(
                    row, 79
                ),  # 0.1kWH   Epv6_today H         PV6 Energy today (high)
                # 0.1kWH        Epv6_today L       PV6 Energy today (low)
                "Epv6Total": read_double(
                    row, 81
                ),  # 0.1kWH   Epv6_total H         PV6 Energy total (high)
                # 0.1kWH        Epv6_total L       PV6 Energy total (low)
                "Epv7Today": read_double(
                    row, 83
                ),  # 0.1kWH   Epv7_today H         PV7 Energy today (high)
                # 0.1kWH        Epv7_today L       PV7 Energy today (low)
                "Epv7Total": read_double(
                    row, 85
                ),  # 0.1kWH   Epv7_total H         PV7 Energy total (high)
                # 0.1kWH        Epv7_total L       PV7 Energy total (low)
                "Epv8Today": read_double(
                    row, 87
                ),  # 0.1kWH   Epv8_today H         PV8 Energy today (high)
                # 0.1kWH        Epv8_today L       PV8 Energy today (low)
                "Epv8Total": read_double(
                    row, 89
                ),  # 0.1kWH   Epv8_total H         PV8 Energy total (high)
                # 0.1kWH        Epv8_total L       PV8 Energy total (low)
                "EpvTotal": read_double(
                    row, 91
                ),  # 0.1kWH   Epv_total H        PV Energy total (high)
                # 0.1kWH        Epv_total L       PV Energy total (low)
                "Temp1": read_single(
                    row, 93
                ),  # 0.1C   Temp1                  Inverter temperature
                "Temp2": read_single(
                    row, 94
                ),  # 0.1C   Temp2                  The inside IPM in inverter Temperature
                "Temp3": read_single(
                    row, 95
                ),  # 0.1C   Temp3                  Boost temperature
                "Temp4": read_single(row, 96),  # 0.1C   Temp4
                "Temp5": read_single(row, 97),  # 0.1C   Temp5
                "PBusV": read_single(
                    row, 98
                ),  # 0.1V   P Bus Voltage         P Bus inside Voltage
                "NBusV": read_single(
                    row, 99
                ),  # 0.1V   N Bus Voltage         N Bus inside Voltage
                "IPF": read_single(
                    row, 100
                ),  # 0.1W   IPF          Inverter output PF now
                "RealOPPercent": read_single(
                    row, 101
                ),  # 1% RealOPPercent Real Output power Percent
                "OPFullwatt": read_double(
                    row, 102
                ),  # 0.1W OPFullwatt H  Output Maxpower Limited high
                "DeratingModeRaw": read_single(
                    row, 104
                ),  # 104. DeratingMode DeratingMode 0:no derate
                "DeratingMode": DeratingMode[read_single(row, 104)],
                "Fault code": read_single(
                    row, 105
                ),  # Fault code Inverter fault code &*1
                "Fault Bitcode": read_double(
                    row, 106
                ),  # 106. Fault Bitcode H Inverter fault code high
                "Fault Bit_II": read_double(
                    row, 108
                ),  # Fault Bit_II H Inverter fault code_II high
                "Warning bit": read_double(row, 110),  # Warning bit H Warning bit H
                "bINVWarnCode": read_single(row, 112),  # bINVWarnCode bINVWarnCode
                "realPowerPercent": read_single(
                    row, 113
                ),  # real Power Percent real Power Percent 0-100%
                "InvStartDelay": read_single(
                    row, 114
                ),  # inv start delay time inv start delay time
                "bINVAllFaultCode": read_single(
                    row, 115
                ),  # bINVAllFaultCode 
                "ACchargePower_H": read_single(row, 116),  # ACchargePower_H
                "AC chargePower_L": read_single(row, 117),  # AC chargePower_L
                "Priority": read_single(row, 118),  # Priority
                "Battery Type":  BatteryType[row.registers[119]],  # Battery Type
                "AutoProofreadCMD": read_single(row, 120),  # AutoProofreadCMD
            }
            # row = self.client.read_input_registers(125, 48, unit=self.unit)#TODO add third group
            # info = merge(info, {
            #     'PIDPV1V': read_single(row, 0),  #ID PV1+ Voltage PID PV1PE Volt 0~1000V 0.1V
            #     'PIDPV1C': read_single(row, 1),  # PID PV1+ Current PID PV1PE Curr -10~10mA 0.1mA
            #     'PIDPV2V': read_single(row, 2),  # PID PV2+ Voltage PID PV2PE Volt 0~1000V 0.1V
            #     'PIDPV2C': read_single(row, 3),  # PID PV2+ Current PID PV1PE Curr -10~10mA 0.1mA
            #     'PIDPV3V': read_single(row, 4),  # PID PV3+ Voltage PID PV2PE Volt 0~1000V 0.1V
            #     'PIDPV3C': read_single(row, 5),  # PID PV3+ Current PID PV1PE Curr -10~10mA 0.1mA
            #     'PIDPV4V': read_single(row, 6),  # PID PV4+ Voltage PID PV2PE Volt 0~1000V 0.1V
            #     'PIDPV4C': read_single(row, 7),  # PID PV4+ Current PID PV1PE Curr -10~10mA 0.1mA
            #     'PIDPV5V': read_single(row, 8),  # PID PV5+ Voltage PID PV2PE Volt 0~1000V 0.1V
            #     'PIDPV5C': read_single(row, 9),  # PID PV5+ Current PID PV1PE Curr -10~10mA 0.1mA
            #     'PIDPV6V': read_single(row, 10),  # PID PV4+ Voltage PID PV2PE Volt 0~1000V 0.1V
            #     'PIDPV6C': read_single(row, 11),  # PID PV4+ Current PID PV1PE Curr -10~10mA 0.1mA
            #     'PIDPV7V': read_single(row, 12),  # PID PV4+ Voltage PID PV2PE Volt 0~1000V 0.1V
            #     'PIDPV7C': read_single(row, 13),  # PID PV4+ Current PID PV1PE Curr -10~10mA 0.1mA
            #     'PIDPV8V': read_single(row, 14),  # PID PV4+ Voltage PID PV2PE Volt 0~1000V 0.1V
            #     'PIDPV8C': read_single(row, 15),  # PID PV4+ Current PID PV1PE Curr -10~10mA 0.1mA
            #     'PID Status Raw': read_single(row, 16), #Bit0~7:PID Working Status 1:Wait Status 2:Normal Status 3:Fault Status Bit8~15:Reversed
            #     'PID Status': PIDStatus[read_single(row, 17)],
            #     'V_String1': read_single(row, 18), #V _String1 PV String1 voltage 0.1V
            #     'Curr_String1': read_single(row, 19), # Curr _String1 PV String1 current -15~15A 0.1A
            #     'V_String2': read_single(row, 20), #V _String2 PV String1 voltage 0.1V
            #     'Curr_String2': read_single(row, 21), # Curr _String2 PV String1 current -15~15A 0.1A
            #     'V_String3': read_single(row, 22), #V _String3 PV String1 voltage 0.1V
            #     'Curr_String3': read_single(row, 23), # Curr _String3 PV String1 current -15~15A 0.1A
            #     'V_String4': read_single(row, 24), #V _String4 PV String1 voltage 0.1V
            #     'Curr_String4': read_single(row, 25), # Curr _String4 PV String1 current -15~15A 0.1A
            #     'V_String5': read_single(row, 26), #V _String5 PV String1 voltage 0.1V
            #     'Curr_String5': read_single(row, 27), # Curr _String5 PV String1 current -15~15A 0.1A
            #     'V_String6': read_single(row, 28), #V _String6 PV String1 voltage 0.1V
            #     'Curr_String6': read_single(row, 29), # Curr _String6 PV String1 current -15~15A 0.1A
            #     'V_String7': read_single(row, 30), #V _String7 PV String1 voltage 0.1V
            #     'Curr_String7': read_single(row, 31), # Curr _String7 PV String1 current -15~15A 0.1A
            #     'V_String8': read_single(row, 32), #V _String8 PV String1 voltage 0.1V
            #     'Curr_String8': read_single(row, 33), # Curr _String8 PV String1 current -15~15A 0.1A
            #     'V_String9': read_single(row, 34), #V _String9 PV String1 voltage 0.1V
            #     'Curr_String9': read_single(row, 35), # Curr _String9 PV String1 current -15~15A 0.1A
            #     'V_String10': read_single(row, 36), #V _String10 PV String1 voltage 0.1V
            #     'Curr_String10': read_single(row, 37), # Curr _String10 PV String1 current -15~15A 0.1A
            #     'V_String11': read_single(row, 38), #V _String11 PV String1 voltage 0.1V
            #     'Curr_String11': read_single(row, 39), # Curr _String11 PV String1 current -15~15A 0.1A
            #     'V_String12': read_single(row, 40), #V _String12 PV String1 voltage 0.1V
            #     'Curr_String12': read_single(row, 41), # Curr _String12 PV String1 current -15~15A 0.1A
            #     'V_String13': read_single(row, 42), #V _String13 PV String1 voltage 0.1V
            #     'Curr_String13': read_single(row, 43), # Curr _String13 PV String1 current -15~15A 0.1A
            #     'V_String14': read_single(row, 44), #V _String14 PV String1 voltage 0.1V
            #     'Curr_String14': read_single(row, 45), # Curr _String14 PV String1 current -15~15A 0.1A
            #     'V_String15': read_single(row, 46), #V _String15 PV String1 voltage 0.1V
            #     'Curr_String15': read_single(row, 47), # Curr _String15 PV String1 current -15~15A 0.1A
            #     'V_String16': read_single(row, 48), #V _String16 PV String1 voltage 0.1V
            #     'Curr_String16': read_single(row, 49) # Curr _String16 PV String1 current -15~15A 0.1A
            # })
            return info

        elif self.protocol_version == "3.04" or self.protocol_version == "3.14":
            row = self.client.read_input_registers(0, 33, unit=self.unit)
            if row.isinstance(ModbusIOException):
                self.__log.error(row.__str__)
                return None
            # http://www.growatt.pl/dokumenty/Inne/Growatt%20PV%20Inverter%20Modbus%20RS485%20RTU%20Protocol%20V3.04.pdf
            #                                           # Unit,     Variable Name,      Description
            info = {  # ==================================================================
                # N/A,      Inverter Status,    Inverter run state
                "StatusCode": row.registers[0],
                "Status": StateCodes[row.registers[0]],
                # 0.1W,     Ppv H,              Input power (high)
                "Ppv": read_double(row, 1),
                # 0.1W,     Ppv L,              Input power (low)
                # 0.1V,     Vpv1,               PV1 voltage
                "Vpv1": read_single(row, 3),
                # 0.1A,     PV1Curr,            PV1 input current
                "PV1Curr": read_single(row, 4),
                # 0.1W,     PV1Watt H,          PV1 input watt (high)
                "PV1Watt": read_double(row, 5),
                # 0.1W,     PV1Watt L,          PV1 input watt (low)
                # 0.1V,     Vpv2,               PV2 voltage
                "Vpv2": read_single(row, 7),
                # 0.1A,     PV2Curr,            PV2 input current
                "PV2Curr": read_single(row, 8),
                # 0.1W,     PV2Watt H,          PV2 input watt (high)
                "PV2Watt": read_double(row, 9),
                # 0.1W,     PV2Watt L,          PV2 input watt (low)
                # 0.1W,     Pac H,              Output power (high)
                "Pac": read_double(row, 11),
                # 0.1W,     Pac L,              Output power (low)
                # 0.01Hz,   Fac,                Grid frequency
                "Fac": read_single(row, 13, 100),
                # 0.1V,     Vac1,               Three/single phase grid voltage
                "Vac1": read_single(row, 14),
                # 0.1A,     Iac1,               Three/single phase grid output current
                "Iac1": read_single(row, 15),
                # 0.1VA,    Pac1 H,             Three/single phase grid output watt (high)
                "Pac1": read_double(row, 16),
                # 0.1VA,    Pac1 L,             Three/single phase grid output watt (low)
                # 0.1V,     Vac2,               Three phase grid voltage
                "Vac2": read_single(row, 18),
                # 0.1A,     Iac2,               Three phase grid output current
                "Iac2": read_single(row, 19),
                # 0.1VA,    Pac2 H,             Three phase grid output power (high)
                "Pac2": read_double(row, 20),
                # 0.1VA,    Pac2 L,             Three phase grid output power (low)
                # 0.1V,     Vac3,               Three phase grid voltage
                "Vac3": read_single(row, 22),
                # 0.1A,     Iac3,               Three phase grid output current
                "Iac3": read_single(row, 23),
                # 0.1VA,    Pac3 H,             Three phase grid output power (high)
                "Pac3": read_double(row, 24),
                # 0.1VA,    Pac3 L,             Three phase grid output power (low)
                # 0.1kWh,   Energy today H,     Today generate energy (high)
                "EnergyToday": read_double(row, 26),
                # 0.1kWh,   Energy today L,     Today generate energy today (low)
                # 0.1kWh,   Energy total H,     Total generate energy (high)
                "EnergyTotal": read_double(row, 28),
                # 0.1kWh,   Energy total L,     Total generate energy (low)
                # 0.5S,     Time total H,       Work time total (high)
                "TimeTotal": read_double(row, 30, 2),
                # 0.5S,     Time total L,       Work time total (low)
                # 0.1C,     Temperature,        Inverter temperature
                "Temp": read_single(row, 32),
            }

            row = self.client.read_input_registers(33, 8, unit=self.unit)
            info = merge(
                info,
                {
                    # 0.1V,     ISO fault Value,    ISO Fault value
                    "ISOFault": read_single(row, 0),
                    # 1mA,      GFCI fault Value,   GFCI fault Value
                    "GFCIFault": read_single(row, 1, 1),
                    # 0.01A,    DCI fault Value,    DCI fault Value
                    "DCIFault": read_single(row, 2, 100),
                    # 0.1V,     Vpv fault Value,    PV voltage fault value
                    "VpvFault": read_single(row, 3),
                    # 0.1V,     Vac fault Value,    AC voltage fault value
                    "VavFault": read_single(row, 4),
                    # 0.01 Hz,  Fac fault Value,    AC frequency fault value
                    "FacFault": read_single(row, 5, 100),
                    # 0.1C,     Temp fault Value,   Temperature fault value
                    "TempFault": read_single(row, 6),
                    # Fault code,         Inverter fault bit
                    "FaultCode": row.registers[7],
                    "Fault": ErrorCodes[row.registers[7]],
                },
            )

            # row = self.client.read_input_registers(41, 1, unit=self.unit)
            # info = merge_dicts(info, {
            #    'IPMTemp': read_single(row, 0),         # 0.1C,     IPM Temperature,    The inside IPM in inverter Temperature
            # })

            row = self.client.read_input_registers(42, 2, unit=self.unit)
            info = merge(
                info,
                {
                    # 0.1V,     P Bus Voltage,      P Bus inside Voltage
                    "PBusV": read_single(row, 0),
                    # 0.1V,     N Bus Voltage,      N Bus inside Voltage
                    "NBusV": read_single(row, 1),
                },
            )

            # row = self.client.read_input_registers(44, 3, unit=self.unit)
            # info = merge_dicts(info, {
            #                                            #           Check Step,         Product check step
            #                                            #           IPF,                Inverter output PF now
            #                                            #           ResetCHK,           Reset check data
            # })
            #
            # row = self.client.read_input_registers(47, 1, unit=self.unit)
            # info = merge_dicts(info, {
            #    'DeratingMode': row.registers[6],       #           DeratingMode,       DeratingMode
            #    'Derating': DeratingMode[row.registers[6]]
            # })

            row = self.client.read_input_registers(48, 16, unit=self.unit)
            info = merge(
                info,
                {
                    # 0.1kWh,   Epv1_today H,       PV Energy today
                    "Epv1_today": read_double(row, 0),
                    # 0.1kWh,   Epv1_today L,       PV Energy today
                    # 0.1kWh,   Epv1_total H,       PV Energy total
                    "Epv1_total": read_double(row, 2),
                    # 0.1kWh,   Epv1_total L,       PV Energy total
                    # 0.1kWh,   Epv2_today H,       PV Energy today
                    "Epv2_today": read_double(row, 4),
                    # 0.1kWh,   Epv2_today L,       PV Energy today
                    # 0.1kWh,   Epv2_total H,       PV Energy total
                    "Epv2_total": read_double(row, 6),
                    # 0.1kWh,   Epv2_total L,       PV Energy total
                    # 0.1kWh,   Epv_total H,        PV Energy total
                    "Epv_total": read_double(row, 8),
                    # 0.1kWh,   Epv_total L,        PV Energy total
                    # 0.1Var,   Rac H,              AC Reactive power
                    "Rac": read_double(row, 10),
                    # 0.1Var,   Rac L,              AC Reactive power
                    # 0.1kVarh, E_rac_today H,      AC Reactive energy
                    "E_rac_today": read_double(row, 12),
                    # 0.1kVarh, E_rac_today L,      AC Reactive energy
                    # 0.1kVarh, E_rac_total H,      AC Reactive energy
                    "E_rac_total": read_double(row, 14),
                    # 0.1kVarh, E_rac_total L,      AC Reactive energy
                },
            )

            # row = self.client.read_input_registers(64, 2, unit=self.unit)
            # info = merge_dicts(info, {
            #    'WarningCode': row.registers[0],        #           WarningCode,        Warning Code
            #    'WarningValue': row.registers[1],       #           WarningValue,       Warning Value
            # })
            #
            # info = merge_dicts(info, self.read_fault_table('GridFault', 90, 5))

            return info
        elif self.protocol_version == "TLXH":
            self.__log.debug("Using TLXH protocol")
            return self.read_register_TLXH()
        elif self.protocol_version == "TL3X":
            self.__log.debug("Using TL3X protocol")
            return self.read_register_TL3X()
        else:
            self.__log.error("Error unknown protocol %s\n", self.protocol_version)
    
    def read_register_TL3X(self, count=238):
        """
        Reads register block starting at address 0.
        """
        row = self.client.read_input_registers(0, count, unit=self.unit)
        if row.isError():
            self.__log.error("Error reading register block 0+")
            return None

        if not TL3X_REG_INPUT_MAP:
            self.__log.warning(
                "REG_INPUT_MAP for TL3X inverters is empty. Fill it according to your protocol PDF."
            )
            return {}

        return read_from_map(row, 0, TL3X_REG_INPUT_MAP)

    def read_register_TLXH(self, count=232):
        """
        Reads register block starting at address 3000.
        """
        row = self.client.read_input_registers(3000, count, unit=self.unit)
        if row.isError():
            self.__log.error("Error reading register block 3000+")
            return None

        if not TLXH_REG_INPUT_MAP:
            self.__log.warning(
                "REG_INPUT_MAP for TLXH inverters is empty. Fill it according to your protocol PDF."
            )
            return {}

        return read_from_map(row, 0, TLXH_REG_INPUT_MAP)

    # def read_fault_table(self, name, base_index, count):
    #     fault_table = {}
    #     for i in range(0, count):
    #         fault_table[name + '_' + str(i)] = self.read_fault_record(base_index + i * 5)
    #     return fault_table
    #
    # def read_fault_record(self, index):
    #     row = self.client.read_input_registers(index, 5, unit=self.unit)
    #     # TODO: Figure out how to read the date for these records?
    #     print(row.registers[0],
    #             ErrorCodes[row.registers[0]],
    #             '\n',
    #             row.registers[1],
    #             row.registers[2],
    #             row.registers[3],
    #             '\n',
    #             2000 + (row.registers[1] >> 8),
    #             row.registers[1] & 0xFF,
    #             row.registers[2] >> 8,
    #             row.registers[2] & 0xFF,
    #             row.registers[3] >> 8,
    #             row.registers[3] & 0xFF,
    #             row.registers[4],
    #             '\n',
    #             2000 + (row.registers[1] >> 4),
    #             row.registers[1] & 0xF,
    #             row.registers[2] >> 4,
    #             row.registers[2] & 0xF,
    #             row.registers[3] >> 4,
    #             row.registers[3] & 0xF,
    #             row.registers[4]
    #           )
    #     return {
    #         'FaultCode': row.registers[0],
    #         'Fault': ErrorCodes[row.registers[0]],
    #         #'Time': int(datetime.datetime(
    #         #    2000 + (row.registers[1] >> 8),
    #         #    row.registers[1] & 0xFF,
    #         #    row.registers[2] >> 8,
    #         #    row.registers[2] & 0xFF,
    #         #    row.registers[3] >> 8,
    #         #    row.registers[3] & 0xFF
    #         #).timestamp()),
    #         'Value': row.registers[4]
    #     }
