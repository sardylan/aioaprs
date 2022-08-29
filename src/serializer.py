from typing import List

from packets import PACKET_TYPE_TELEMETRY


class PacketSerializer:
    _packet: dict

    def __init__(self, packet: dict) -> None:
        super().__init__()

        self._packet = packet

    def serialize(self) -> str:
        return "%s:%s" % (
            self._serialize_header(),
            self._serialize_body(),
        )

    def _serialize_header(self) -> str:
        header = "%s>%s" % (self._packet["source"], self._packet["destination"])

        if self._packet["path"]:
            header += "," + ",".join(self._packet["path"])

        return header

    def _serialize_body(self) -> str:
        if self._packet["type"] == PACKET_TYPE_TELEMETRY:
            return self._serialize_body_telemetry()

        else:
            return "body" in self._packet and self._packet["body"] or ""

    def _serialize_body_telemetry(self) -> str:
        serialized_packet: str = f"{PACKET_TYPE_TELEMETRY}#"

        if 0 <= self._packet["seq"] <= 255:
            serialized_packet += "%03d" % self._packet["seq"]
        else:
            serialized_packet += "MIC"

        if "values" in self._packet and self._packet["values"]:
            serialized_packet += ","

            values: List[str] = []
            for value in self._packet["values"][:5]:
                values.append("%.02f" % value)

            serialized_packet += ",".join(values)

            if len(self._packet["values"]) >= 5 and "bits" in self._packet and self._packet["bits"]:
                serialized_packet += ","

                for bit in self._packet["bits"][:8]:
                    serialized_packet += (bit is True) and "1" or "0"

        return serialized_packet
