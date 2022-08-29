import pytest

from packets import PacketType
from parser import PacketParser


def test_telemetry_no_seq():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T"

    packet_parser: PacketParser = PacketParser(data_input)
    with pytest.raises(ValueError):
        packet_parser.parse()


def test_telemetry_short_seq():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T23"

    packet_parser: PacketParser = PacketParser(data_input)
    with pytest.raises(ValueError):
        packet_parser.parse()


def test_telemetry_no_seq_with_sharp():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#"

    packet_parser: PacketParser = PacketParser(data_input)
    with pytest.raises(ValueError):
        packet_parser.parse()


def test_telemetry_short_seq_with_sharp():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#23"

    packet_parser: PacketParser = PacketParser(data_input)
    with pytest.raises(ValueError):
        packet_parser.parse()


def test_telemetry_no_value_no_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": []
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_no_value_with_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [0.0]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_one_value_no_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_one_value_with_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 0.0]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_two_values_with_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,3.40,"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,3.40,",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 3.4, 0.0]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_three_values_no_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,3.40,5.60"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,3.40,5.60",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 3.4, 5.6]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_three_values_with_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,3.40,5.60,"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,3.40,5.60,",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 0.0]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_four_values_no_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,3.40,5.60,7.80"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,3.40,5.60,7.80",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_four_values_with_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,3.40,5.60,7.80,"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,3.40,5.60,7.80,",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 0.0]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_no_bits_no_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,3.40,5.60,7.80,9.00"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,3.40,5.60,7.80,9.00",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_no_bits_with_comma():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,3.40,5.60,7.80,9.00,"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,3.40,5.60,7.80,9.00,",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [False, False, False, False, False, False, False, False]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_few_bits():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,3.40,5.60,7.80,9.00,101"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,3.40,5.60,7.80,9.00,101",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [True, False, True, False, False, False, False, False]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_completed():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,3.40,5.60,7.80,9.00,10101010"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,3.40,5.60,7.80,9.00,10101010",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [True, False, True, False, True, False, True, False]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_too_many_bits():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,1.20,3.40,5.60,7.80,9.00,1010101011"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,1.20,3.40,5.60,7.80,9.00,1010101011",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [True, False, True, False, True, False, True, False]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_completed_8bit():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,123,234,122,151,0,10101010"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,123,234,122,151,0,10101010",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA_DATA,
        "seq": 123,
        "values": [123, 234, 122, 151, 0],
        "bits": [True, False, True, False, True, False, True, False]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected


def test_telemetry_completed_some_8bit():
    data_input: str = "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA:T#123,123,234,12.2,151,0,10101010"

    data_expected: dict = {
        "header": "AA0ZZZ>APDW16,WIDE1-1,qAR,ZZ9AAA",
        "body": "T#123,123,234,12.2,151,0,10101010",
        "source": "AA0ZZZ",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "ZZ9AAA"],
        "via": "ZZ9AAA",
        "type": PacketType.TELEMETRY_DATA,
        "seq": 123,
        "values": [123.0, 234.0, 12.2, 151.0, 0.0],
        "bits": [True, False, True, False, True, False, True, False]
    }

    packet_parser: PacketParser = PacketParser(data_input)
    data_actual: dict = packet_parser.parse()

    assert data_actual == data_expected
