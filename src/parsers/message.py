import logging
from typing import List

_logger = logging.getLogger(__name__)


def parse_body_message(raw_body: str) -> dict:
    packet: dict = dict()

    packet["message"] = raw_body

    items: List[str] = raw_body.split(":")
    if len(items) >= 3:
        message_callsign = items[1].strip().upper()
        if message_callsign != packet["source"]:
            return packet

        message_items: List[str] = items[2].split(".")
        if len(message_items) >= 2:
            message_raws = (".".join(message_items[1:])).split(",")
            message_type = message_items[0].strip().upper()

            packet[message_type] = {
                "values": message_raws[:5],
            }

            if len(message_raws) >= 6:
                bits = message_raws[5]

                if set(bits) <= set("10"):
                    packet[message_type]["bits"] = [x == "1" for x in bits[:8]]

    return packet
