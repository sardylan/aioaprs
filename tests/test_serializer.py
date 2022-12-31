import pytest

from aioaprs.packets import PacketType
from aioaprs.serializer import PacketSerializer


def test_serializer_none():
    data_input = None

    packet_serializer: PacketSerializer = PacketSerializer(data_input)
    with pytest.raises(ValueError):
        packet_serializer.serialize()


def test_serializer_empty():
    data_input: dict = dict()

    packet_serializer: PacketSerializer = PacketSerializer(data_input)
    with pytest.raises(ValueError):
        packet_serializer.serialize()


def test_serializer_source():
    data_input: dict = {
        "source": "IR0AAA"
    }

    packet_serializer: PacketSerializer = PacketSerializer(data_input)
    with pytest.raises(KeyError):
        packet_serializer.serialize()


def test_serializer_source_destination():
    data_input: dict = {
        "source": "IR0AAA",
        "destination": "APDW16"
    }

    packet_serializer: PacketSerializer = PacketSerializer(data_input)
    with pytest.raises(KeyError):
        packet_serializer.serialize()


def test_serializer_source_destination_path():
    data_input: dict = {
        "source": "IR0AAA",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "IS0AAA-12"]
    }

    packet_serializer: PacketSerializer = PacketSerializer(data_input)
    with pytest.raises(KeyError):
        packet_serializer.serialize()


def test_serializer_source_destination_path_type():
    data_input: dict = {
        "source": "IR0AAA",
        "destination": "APDW16",
        "path": ["WIDE1-1", "qAR", "IS0AAA-12"],
        "type": PacketType.UNUSED
    }

    data_expected: str = "IR0AAA>APDW16,WIDE1-1,qAR,IS0AAA-12:"

    packet_serializer: PacketSerializer = PacketSerializer(data_input)
    data_actual: str = packet_serializer.serialize()

    assert data_actual == data_expected


def test_serializer_source_destination_via_type():
    data_input: dict = {
        "source": "IR0AAA",
        "destination": "APDW16",
        "via": "WIDE1-1",
        "type": PacketType.UNUSED
    }

    data_expected: str = "IR0AAA>APDW16,WIDE1-1:"

    packet_serializer: PacketSerializer = PacketSerializer(data_input)
    data_actual: str = packet_serializer.serialize()

    assert data_actual == data_expected
