from dataclasses import dataclass
from pathlib import Path

import numpy as np
from ycecream import y as ic

hex_to_binary = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


@dataclass
class Packet:
    version: int
    ptype: int
    literal: int = None
    sub_packets: list = None

    def evaluate(self):
        if self.ptype == 0:
            return sum([sub.evaluate() for sub in self.sub_packets])
        elif self.ptype == 1:
            return np.prod([sub.evaluate() for sub in self.sub_packets])
        elif self.ptype == 2:
            return min([sub.evaluate() for sub in self.sub_packets])
        elif self.ptype == 3:
            return max([sub.evaluate() for sub in self.sub_packets])
        elif self.ptype == 4:
            return self.literal
        elif self.ptype == 5:
            return int(self.sub_packets[0].evaluate() > self.sub_packets[1].evaluate())
        elif self.ptype == 6:
            return int(self.sub_packets[0].evaluate() < self.sub_packets[1].evaluate())
        elif self.ptype == 7:
            return int(self.sub_packets[0].evaluate() == self.sub_packets[1].evaluate())


class Parser:
    def __init__(self, data):
        self.buffer = data

    def read(self, nchars):
        if len(self.buffer) >= nchars:
            result = self.buffer[:nchars]
            self.buffer = self.buffer[nchars:]
            return result
        else:
            return None

    def bits2num(self, nbits):
        return int(self.read(nbits), 2)

    def version_id(self):
        return self.bits2num(3)

    def packet_type(self):
        return self.bits2num(3)

    def standard_header(self):
        return self.version_id(), self.packet_type()

    def literal_payload(self):
        ic("literal")
        result = ""
        keep_going = 1
        while keep_going:
            keep_going = self.bits2num(1)
            result += self.read(4)
        return int(result, 2)

    def operator_payload(self):
        ic("operator")
        length_type_id = self.bits2num(1)
        if length_type_id == 0:
            ic("length-flavor")
            sub_packets_length = self.bits2num(15)
            buffer = self.read(sub_packets_length)
            sub_parser = Parser(buffer)
            sub_packets = []
            while len(sub_parser.buffer) > 6:
                sub_packets.append(sub_parser.read_packet())
        else:
            ic("num flavor")
            num_sub_packets = self.bits2num(11)
            sub_packets = [self.read_packet() for _ in range(num_sub_packets)]
        return sub_packets

    def read_packet(self):
        version, packet_type = self.standard_header()
        packet = Packet(version=version, ptype=packet_type)
        ic(version, packet_type)

        if packet_type == 4:
            packet.literal = self.literal_payload()
            return packet
        else:
            packet.sub_packets = self.operator_payload()
            return packet


def version_sum(packet):
    total_score = packet.version
    if packet.sub_packets:
        for sub in packet.sub_packets:
            total_score += version_sum(sub)
    return total_score


def solve1(data):
    packet = Parser(data).read_packet()
    return version_sum(packet)


def solve2(data):
    packet = Parser(data).read_packet()
    return packet.evaluate()


def parsetext(text):
    binary = "".join([hex_to_binary[ch] for ch in text])
    return ic(binary)


def mydata():
    return Path("input.txt").read_text().strip()


def part1():
    TEST_1 = "8A004A801A8002F478", 16
    TEST_2 = "620080001611562C8802118E34", 12
    TEST_3 = "C0015000016115A2E0802F182340", 23
    TEST_4 = "A0016C880162017C3686B18A3D4780", 31

    ic.enabled = False
    for test in [TEST_1, TEST_2, TEST_3, TEST_4]:
        text, expected = test
        data = parsetext(text)
        result = solve1(data)
        assert result == expected
        ic(text, "PASS")

    ic.enabled = False
    data = parsetext(mydata())
    result = solve1(data)
    return result


def part2():
    tests = [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ]

    ic.enabled = True
    for test in tests:
        text, expected = test
        data = parsetext(text)
        result = solve2(data)
        assert result == expected
        ic(text, "PASS")

    ic.enabled = False
    return solve2(parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
