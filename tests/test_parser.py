import pytest

from aioaprs.parser import PacketParser


def test_parser_none():
    data_input = None

    packet_parser: PacketParser = PacketParser(data_input)
    with pytest.raises(ValueError):
        packet_parser.parse()


def test_parser_empty_raw():
    data_input = ""

    packet_parser: PacketParser = PacketParser(data_input)
    with pytest.raises(ValueError):
        packet_parser.parse()


def test_parser_empty_header_body():
    data_input = ":"

    packet_parser: PacketParser = PacketParser(data_input)
    with pytest.raises(ValueError):
        packet_parser.parse()


def test_parser_empty_header():
    data_input = ": "

    packet_parser: PacketParser = PacketParser(data_input)
    with pytest.raises(ValueError):
        packet_parser.parse()


def test_parser_empty_body():
    data_input = " :"

    packet_parser: PacketParser = PacketParser(data_input)
    with pytest.raises(ValueError):
        packet_parser.parse()


def test_parser_empty():
    data_input = " : "

    packet_parser: PacketParser = PacketParser(data_input)
    with pytest.raises(ValueError):
        packet_parser.parse()


def test_parser_empty_both():
    data_input: str = "IR0AAA>APDW16,WIDE1-1,qAR,IS0AAA-12:T#123"
    data_expected: dict = {
        "raw": "IR0AAA>APDW16,WIDE1-1,qAR,IS0AAA-12:T#123",
        "header": "IR0AAA>APDW16,WIDE1-1,qAR,IS0AAA-12",
        "body": "T#123",
        "source": "IR0AAA",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "IS0AAA-12"],
        "via": "IS0AAA-12"
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    for key in data_expected.keys():
        assert key in data_actual and data_actual[key] == data_expected[key]
