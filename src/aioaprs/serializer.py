from aioaprs.packets import PacketType
from aioaprs.serializers.telemetry import serialize_body_telemetry


class PacketSerializer:
    _packet: dict

    def __init__(self, packet: dict) -> None:
        super().__init__()

        self._packet = packet

    def serialize(self) -> str:
        if self._packet is None:
            raise ValueError("Invalid packet")

        if not self._packet:
            raise ValueError("Empty packet")

        return "%s:%s" % (
            self._serialize_header(),
            self._serialize_body(),
        )

    def _serialize_header(self) -> str:
        header = "%s>%s" % (self._packet["source"], self._packet["destination"])

        if "path" in self._packet and isinstance(self._packet["path"], list) and self._packet["path"]:
            header += "," + ",".join(self._packet["path"])
        elif "via" in self._packet and isinstance(self._packet["via"], str) and self._packet["via"]:
            header += "," + self._packet["via"]

        return header

    def _serialize_body(self) -> str:
        if self._packet["type"] == PacketType.TELEMETRY_DATA:
            return serialize_body_telemetry(self._packet)

        else:
            return "body" in self._packet and self._packet["body"] or ""
