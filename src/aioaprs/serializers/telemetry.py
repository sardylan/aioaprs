import logging
from typing import List

from aioaprs.packets import PacketType, PACKET_TYPE_IDENTIFIER

_logger = logging.getLogger(__name__)


def serialize_body_telemetry(packet: dict) -> str:
    serialized_packet: str = f"{PACKET_TYPE_IDENTIFIER[PacketType.TELEMETRY_DATA]}#"

    if 0 <= packet["seq"] <= 255:
        serialized_packet += "%03d" % packet["seq"]
    else:
        serialized_packet += "MIC"

    if "values" in packet and packet["values"]:
        serialized_packet += ","

        values: List[str] = []
        for value in packet["values"][:5]:
            values.append("%.02f" % value)

        serialized_packet += ",".join(values)

        if len(packet["values"]) >= 5 and "bits" in packet and packet["bits"]:
            serialized_packet += ","

            for bit in packet["bits"][:8]:
                serialized_packet += (bit is True) and "1" or "0"

    return serialized_packet
