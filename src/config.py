from default import *


class AioAPRSConfig:
    _host: str
    _port: int
    _callsign: str
    _server_filter: str
    _heartbeat: int

    def __init__(self) -> None:
        super().__init__()

        self._host = DEFAULT_HOST
        self._port = DEFAULT_PORT
        self._callsign = DEFAULT_CALLSIGN
        self._server_filter = DEFAULT_SERVER_FILTER
        self._heartbeat = DEFAULT_HEARTBEAT

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, host: str) -> None:
        self._host = host

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, port: int) -> None:
        self._port = port

    @property
    def callsign(self) -> str:
        return self._callsign

    @callsign.setter
    def callsign(self, callsign: str) -> None:
        self._callsign = callsign

    @property
    def server_filter(self) -> str:
        return self._server_filter

    @server_filter.setter
    def server_filter(self, server_filter: str) -> None:
        self._server_filter = server_filter

    @property
    def heartbeat(self) -> int:
        return self._heartbeat

    @heartbeat.setter
    def heartbeat(self, heartbeat: int) -> None:
        self._heartbeat = heartbeat
