from typing import Callable
import colorama
import operator
import types

color: Callable[
    [str], Callable[[str], str]
] = lambda clr: lambda text: f"{clr}{text}{colorama.Style.RESET_ALL}"

red = color(colorama.Fore.LIGHTRED_EX)
green = color(colorama.Fore.LIGHTGREEN_EX)
yellow = color(colorama.Fore.LIGHTYELLOW_EX)
blue = color(colorama.Fore.LIGHTBLUE_EX)
magenta = color(colorama.Fore.LIGHTMAGENTA_EX)
cyan = color(colorama.Fore.LIGHTCYAN_EX)


clr_version = green
clr_packet = magenta
clr_value = yellow
clr_length = clr_length_type = red
clr_begin = clr_end = cyan

VERSION_SIZE = 3
PACKET_TYPE_SIZE = 3
LENGTH_TYPE_SIZE = 1
LENGTH_TYPES = types.SimpleNamespace()
LENGTH_TYPES.BITS = 0
LENGTH_TYPES.PACKETS = 1
BITS_LENGTH_TYPE_SIZE = 15
PACKETS_LENGTH_TYPE_SIZE = 11
PACKET_TYPES = types.SimpleNamespace()
PACKET_TYPES.SUM = 0
PACKET_TYPES.PRODUCT = 1
PACKET_TYPES.MINIMUM = 2
PACKET_TYPES.MAXIMUM = 3
PACKET_TYPES.CONSTANT = 4
PACKET_TYPES.GREATER_THAN = 5
PACKET_TYPES.LESS_THAN = 6
PACKET_TYPES.EQUAL_TO = 7

class Packet:
    def __init__(self, pointer: int = 0, parent=None):
        self.begin = self.pointer = pointer
        self.version = self.read_version()
        self.type = self.read_packet_type()
        self.parent = parent
        if self.type != PACKET_TYPES.CONSTANT:
            self.length_type = self.read_length_type()
            self.length = self.read_length()
            self.packets = self.get_packets()
            self.value = self.get_value()
        else:
            self.value = self.get_constant()

    def get_packets_by_bits(self) -> list["Packet"]:
        end = self.length + self.pointer
        packets: list["Packet"] = []
        while self.pointer < end:
            packets += [Packet(self.pointer)]
            self.pointer = packets[-1].pointer
        return packets

    def get_packets_by_length(self) -> list["Packet"]:
        packets: list["Packet"] = []
        for _packet in range(self.length):
            packets.append(Packet(self.pointer))
            self.pointer = packets[-1].pointer
        return packets

    def get_packets(self) -> list["Packet"]:
        match self.length_type:
            case LENGTH_TYPES.BITS:
                return self.get_packets_by_bits()
            case LENGTH_TYPES.PACKETS:
                return self.get_packets_by_length()
            case _:
                raise ValueError(
                    f"Unknown length type in get_packets {self.length_type}"
                )

    def get_constant(self) -> int:
        value = 0
        is_end = False
        while not is_end:
            is_end = not self.read_int(1)
            value <<= 4
            value += self.read_int(4)
        return value

    def get_value(self) -> int:
        func = None
        match self.type:
            case PACKET_TYPES.SUM:
                func = operator.add
            case PACKET_TYPES.PRODUCT:
                func = operator.mul
            case PACKET_TYPES.MINIMUM:
                func = min
            case PACKET_TYPES.MAXIMUM:
                func = max
            case PACKET_TYPES.GREATER_THAN:
                func = operator.gt
            case PACKET_TYPES.LESS_THAN:
                func = operator.lt
            case PACKET_TYPES.EQUAL_TO:
                func = operator.eq
            case _:
                raise ValueError(f"Invalid packet type in get_value {self.type}")
        return int(reduce(func, [packet.value for packet in self.packets]))

    def read_version(self) -> int:
        return self.read_int(VERSION_SIZE)

    def read_packet_type(self) -> int:
        return self.read_int(PACKET_TYPE_SIZE)

    def read_length_type(self) -> int:
        return self.read_int(LENGTH_TYPE_SIZE)

    def read_length(self) -> int:
        match self.length_type:
            case LENGTH_TYPES.BITS:
                return self.read_int(BITS_LENGTH_TYPE_SIZE)
            case LENGTH_TYPES.PACKETS:
                return self.read_int(PACKETS_LENGTH_TYPE_SIZE)
            case _:
                raise ValueError(
                    f"Unknown length type in read_length {self.length_type}"
                )

    def read_bits(self, length: int) -> str:
        res = binary[self.pointer : self.pointer + length]
        self.pointer += length
        return res

    def read_int(self, length: int) -> int:
        return int(self.read_bits(length), 2)

    def get_all(self):
        yield self
        if self.type != PACKET_TYPES.CONSTANT:
            for packet in self.packets:
                for sub_packet in packet.get_all():
                    yield sub_packet

    def find_packet(self, key) -> "Packet":
        for packet in self.get_all():
            if key(packet):
                return packet

    def packet_type_str(self):
        match self.type:
            case PACKET_TYPES.SUM:
                return "+"
            case PACKET_TYPES.PRODUCT:
                return "*"
            case PACKET_TYPES.MINIMUM:
                return "min"
            case PACKET_TYPES.MAXIMUM:
                return "max"
            case PACKET_TYPES.CONSTANT:
                return "int"
            case PACKET_TYPES.GREATER_THAN:
                return ">"
            case PACKET_TYPES.LESS_THAN:
                return "<"
            case PACKET_TYPES.EQUAL_TO:
                return "=="
            case _:
                return str(self.type)

    def __str__(self):
        version = clr_version(self.version)
        packet_type = clr_packet(self.packet_type_str())
        value = clr_value(self.value)
        begin = clr_begin(self.begin)
        end = clr_end(self.pointer)
        if self.type == PACKET_TYPES.CONSTANT:
            return f"Version : {version} Packet type : {packet_type} Value : {value} Begin : {begin} End : {end}"
        else:
            res = f"Version : {version} Packet type : {packet_type} Length type: {clr_length_type(self.length_type)} Length: {clr_length(self.length)} Value : {value}  Begin : {begin} End : {end}\n"
            for packet in self.packets:
                res += "".join(
                    ["  " + spacket + "\n" for spacket in str(packet).split("\n")]
                )
            return res[:-1]

    def __repr__(self):
        return str(self)