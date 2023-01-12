import logging
from typing import List

_logger = logging.getLogger(__name__)


def parse_body_telemetry(raw_body: str, strict_mode: bool = False) -> dict:
    packet: dict = dict()

    body_data = raw_body[1:]
    if body_data.startswith("#"):
        body_data = body_data[1:]

    items: List[str] = body_data.split(",")

    if len(items[0]) != 3:
        _logger.warning(f"Wrong value for seq number: {items[0]}")
        if strict_mode:
            raise ValueError(f"Invalid seq number: {items[0]}")

    packet["seq"] = int(items[0])
    packet["values"] = []

    raw_values_analog: List[str] = items[1:6]

    for value in raw_values_analog:
        float_value: float = 0.0

        try:
            float_value = float(value)
        except ValueError:
            _logger.error(f"Unable to convert \"{value}\" to float")

        packet["values"].append(float_value)

    if all("." not in x for x in raw_values_analog) and all(0 <= x <= 255 for x in packet["values"]):
        map(int, packet["values"])

    if len(items) >= 7 and set(items[6][:8]) <= set("01"):
        packet["bits"] = []

        for bit in items[6][:8]:
            bool_value: bool = False

            try:
                bool_value = bool(bit == "1")
            except ValueError:
                _logger.error(f"Unable to convert \"{bit}\" to float")

            packet["bits"].append(bool_value)

        while len(packet["bits"]) < 8:
            packet["bits"].append(False)

    return packet
