import logging
from typing import List

from aioaprs.packets import DATA_TYPE_IDENTIFIER, PacketType
from aioaprs.parsers.message import parse_body_message
from aioaprs.parsers.telemetry import parse_body_telemetry

_logger = logging.getLogger(__name__)


class PacketParser:
    _raw_packet: str
    _packet: dict

    def __init__(self, raw_packet: str) -> None:
        super().__init__()

        self._raw_packet = raw_packet
        self._packet = {}

    def parse(self, strict_mode: bool = False) -> dict:
        if self._raw_packet is None:
            raise ValueError("Raw packet is None")

        if self._raw_packet.startswith("#"):
            return dict()

        self._packet["raw"] = self._raw_packet

        marker_position: int = self._raw_packet.find(":")
        raw_header: str = self._raw_packet[:marker_position]
        raw_body: str = self._raw_packet[marker_position + 1:]

        if not raw_header:
            raise ValueError("Empty header")
        if not raw_body:
            raise ValueError("Empty body")

        self._parse_header(raw_header, strict_mode=strict_mode)
        self._parse_body(raw_body, strict_mode=strict_mode)

        return self._packet

    def _parse_header(self, raw_header: str, strict_mode: bool = False) -> None:
        self._packet["header"] = raw_header

        items: List[str] = raw_header.split(",")
        if len(items) < 2:
            raise ValueError("Invalid header")

        srcdest_items: List[str] = items[0].split(">")
        self._packet["source"] = srcdest_items[0].upper()

        try:
            self._packet["destination"] = srcdest_items[1].upper()
        except IndexError:
            _logger.error(f"No destination parsing header: \"{self._raw_packet}\"")

        self._packet["path"] = items[1:]
        self._packet["via"] = items[-1]

    def _parse_body(self, raw_body: str, strict_mode: bool = False) -> None:
        self._packet["body"] = raw_body

        packet_type_char: str = raw_body[0]

        if packet_type_char in DATA_TYPE_IDENTIFIER:
            packet_type: PacketType = DATA_TYPE_IDENTIFIER[packet_type_char]
            self._packet["type"] = packet_type

        else:
            self._packet["type"] = None

        updated_body: dict = dict()

        if self._packet["type"] == PacketType.TELEMETRY_DATA:
            updated_body = parse_body_telemetry(raw_body, strict_mode=strict_mode)
        elif self._packet["type"] == PacketType.MESSAGE:
            updated_body = parse_body_message(raw_body, strict_mode=strict_mode)

        self._packet.update(updated_body)
