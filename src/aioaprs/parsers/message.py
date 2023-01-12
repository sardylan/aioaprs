import logging
from typing import List

_logger = logging.getLogger(__name__)


def parse_body_message(raw_body: str, strict_mode: bool = False) -> dict:
    if not raw_body:
        raise ValueError("Invalid raw body")

    items: List[str] = raw_body.split(":")
    if len(items) < 3:
        raise ValueError("Invalid message raw body")

    raw_addressee: str = items[1]
    if len(raw_addressee) != 9:
        raise ValueError("Invalid addressee length")

    packet: dict = {
        "addressee": raw_addressee.strip().upper(),
        "message": ":".join(items[2:]).strip()
    }

    message_items: List[str] = packet["message"].split(".")
    if len(message_items) >= 2 and message_items[0].upper() in ["PARM", "UNIT", "EQNS", "BITS"]:
        telemetry_type = message_items[0].strip().upper()
        telemetry_items = (".".join(message_items[1:])).split(",")

        packet.update({
            "telemetry_data": {
                "type": telemetry_type,
                "items": telemetry_items
            }
        })

        if packet["telemetry_data"]["type"] == "EQNS":
            equations: List[dict] = list()

            for pos in range(len(telemetry_items)):
                analog_value_index: int = int(pos / 3)
                if len(equations) < analog_value_index + 1:
                    equations.append(dict())
                equations[analog_value_index]["abc"[pos % 3]] = float(telemetry_items[pos])

            packet["telemetry_data"].update({
                "equations": equations
            })

        elif packet["telemetry_data"]["type"] == "BITS":
            if telemetry_items[0]:
                packet["telemetry_data"].update({
                    "bits": [int(x) == 1 for x in telemetry_items[0]]
                })

            if telemetry_items[1]:
                packet["telemetry_data"].update({
                    "project_name": ",".join(telemetry_items[1:]).strip()
                })

    return packet
