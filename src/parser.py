import logging
from typing import List

from packets import PacketType, DATA_TYPE_IDENTIFIER

_logger = logging.getLogger(__name__)


class PacketParser:
    _raw_packet: str
    _packet: dict

    def __init__(self, raw_packet: str) -> None:
        super().__init__()

        self._raw_packet = raw_packet
        self._packet = {}

    def parse(self) -> dict:
        if self._raw_packet.startswith("#"):
            return dict()

        self._packet["raw"] = self._raw_packet

        marker_position: int = self._raw_packet.find(":")
        raw_header: str = self._raw_packet[:marker_position]
        raw_body: str = self._raw_packet[marker_position + 1:]

        self._parse_header(raw_header)
        self._parse_body(raw_body)

        return self._packet

    def _parse_header(self, raw_header: str) -> None:
        self._packet["header"] = raw_header

        items: List[str] = raw_header.split(",")

        srcdest_items: List[str] = items[0].split(">")
        self._packet["source"] = srcdest_items[0].upper()

        try:
            self._packet["destination"] = srcdest_items[1].upper()
        except IndexError:
            _logger.error(f"No destination parsing header: \"{self._raw_packet}\"")

        self._packet["path"] = items[1:]
        self._packet["via"] = items[-1]

    def _parse_body(self, raw_body: str) -> None:
        self._packet["body"] = raw_body

        packet_type_char: str = raw_body[0]
        if packet_type_char in DATA_TYPE_IDENTIFIER:
            packet_type: PacketType = DATA_TYPE_IDENTIFIER[packet_type_char]
            self._packet["type"] = packet_type
        else:
            self._packet["type"] = None

        if self._packet["type"] == PacketType.TELEMETRY_DATA:
            self._parse_body_telemetry(raw_body)
        elif self._packet["type"] == PacketType.MESSAGE:
            self._parse_body_message(raw_body)

    def _parse_body_telemetry(self, raw_body: str) -> None:
        body_data = raw_body[1:]
        if body_data.startswith("#"):
            body_data = body_data[1:]

        items: List[str] = body_data.split(",")

        if len(items[0]) != 3:
            raise ValueError(f"Invalid seq number: {items[0]}")

        self._packet["seq"] = int(items[0])
        self._packet["values"] = []

        raw_values_analog: List[str] = items[1:6]

        for value in raw_values_analog:
            float_value: float = 0

            try:
                float_value = float(value)
            except ValueError:
                _logger.error(f"Unable to convert \"{value}\" to float")

            self._packet["values"].append(float_value)

        if all("." not in x for x in raw_values_analog) and all(0 <= x <= 255 for x in self._packet["values"]):
            map(int, self._packet["values"])

        if len(items) >= 7 and set(items[6][:8]) <= set("01"):
            self._packet["bits"] = []

            for bit in items[6][:8]:
                bool_value: bool = False

                try:
                    bool_value = bool(bit == "1")
                except ValueError:
                    _logger.error(f"Unable to convert \"{bit}\" to float")

                self._packet["bits"].append(bool_value)

            while len(self._packet["bits"]) < 8:
                self._packet["bits"].append(False)

    def _parse_body_message(self, raw_body: str) -> None:
        self._packet["message"] = raw_body

        items: List[str] = raw_body.split(":")
        if len(items) >= 3:
            message_callsign = items[1].strip().upper()
            if message_callsign != self._packet["source"]:
                return

            message_items: List[str] = items[2].split(".")
            if len(message_items) >= 2:
                message_raws = (".".join(message_items[1:])).split(",")
                message_type = message_items[0].strip().upper()

                self._packet[message_type] = {
                    "values": message_raws[:5],
                }

                if len(message_raws) >= 6:
                    bits = message_raws[5]

                    if set(bits) <= set("10"):
                        self._packet[message_type]["bits"] = [x == "1" for x in bits[:8]]
