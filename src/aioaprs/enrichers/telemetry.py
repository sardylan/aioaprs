import logging
from typing import Dict, List

from aioaprs.packets import PacketType

_logger = logging.getLogger(__name__)


class TelemetryEnricher:
    _parameter_names: Dict[str, List[str]]
    _unit_labels: Dict[str, List[str]]
    _equation_coefficients: Dict[str, List[Dict[str, float]]]
    _project_names: Dict[str, str]

    def __init__(self) -> None:
        super().__init__()

        self._parameter_names = dict()
        self._unit_labels = dict()
        self._equation_coefficients = dict()
        self._project_names = dict()

    def parse(self, packet: dict) -> None:
        self._validate_packet(packet)

        if packet["type"] != PacketType.MESSAGE:
            raise ValueError("Packet type not supported for parsing")

        if packet["telemetry_data"]["type"] == "PARM":
            self._parameter_names[packet["addressee"]] = packet["telemetry_data"]["items"]

        elif packet["telemetry_data"]["type"] == "UNIT":
            self._unit_labels[packet["addressee"]] = packet["telemetry_data"]["items"]

        elif packet["telemetry_data"]["type"] == "EQNS":
            self._equation_coefficients[packet["addressee"]] = packet["telemetry_data"]["equations"]

        elif packet["telemetry_data"]["type"] == "BITS":
            self._project_names[packet["addressee"]] = packet["telemetry_data"]["project_name"]

    def enrich(self, packet: dict) -> None:
        self._validate_packet(packet)

        if packet["type"] != PacketType.TELEMETRY_DATA:
            raise ValueError("Packet type not supported for enriching")

        if packet["source"] in self._parameter_names:
            packet["parameter_names"] = self._parameter_names[packet["source"]]

        if packet["source"] in self._unit_labels:
            packet["unit_labels"] = self._unit_labels[packet["source"]]

        if packet["source"] in self._equation_coefficients:
            packet["equation_coefficients"] = self._equation_coefficients[packet["source"]]

            packet["values_real"] = []
            for pos in range(min(len(packet["values"]), 5)):
                value_raw: float = packet["values"][pos]
                a: float = packet["equation_coefficients"][pos]["a"]
                b: float = packet["equation_coefficients"][pos]["b"]
                c: float = packet["equation_coefficients"][pos]["c"]
                real_value: float = (a * value_raw * value_raw) + (b * value_raw) + c
                packet["values_real"].append(real_value)

        if packet["source"] in self._project_names:
            packet["project_name"] = self._project_names[packet["source"]]

    @staticmethod
    def _validate_packet(packet: dict) -> None:
        if packet is None:
            raise ValueError("Invalid packet")

        if not packet:
            raise ValueError("Empty packet")

        if "type" not in packet or packet["type"] not in [PacketType.TELEMETRY_DATA, PacketType.MESSAGE]:
            raise ValueError("Packet type not valid")
