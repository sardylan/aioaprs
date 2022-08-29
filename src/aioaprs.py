import asyncio
import logging
from asyncio import StreamReader, StreamWriter, IncompleteReadError, Task, CancelledError
from typing import Optional, Awaitable, Callable

from config import AioAPRSConfig

__VERSION__: str = "0.1.0"

_logger = logging.getLogger(__name__)


class AioAPRS(object):
    _lock: asyncio.Lock
    _keep_running: bool
    _task_rx: Optional[Task]

    _config: AioAPRSConfig
    _callback: Optional[Callable[[str], Awaitable[None]]]

    _sock_reader: Optional[StreamReader]
    _sock_writer: Optional[StreamWriter]

    def __init__(self, config: AioAPRSConfig, callback: Optional[Callable[[str], Awaitable[None]]] = None) -> None:
        super().__init__()

        self._lock = asyncio.Lock()
        self._keep_running = False
        self._task_rx = None

        self._config = config
        self._callback = callback

        self._sock_reader = None
        self._sock_writer = None

    async def connect(self) -> None:
        async with self._lock:
            if self._sock_reader is not None \
                    or self._sock_writer is not None \
                    or self._task_rx is not None:
                return

            self._sock_reader, self._sock_writer = await asyncio.open_connection(
                host=self._config.host,
                port=self._config.port
            )

            self._keep_running = True
            self._task_rx = asyncio.create_task(self._loop())

            password: str = self.passcode(self._config.callsign)
            version: str = "aioaprs 0.0.0"

            filter_string: str = ""
            if self._config.server_filter:
                filter_string = f" filter {self._config.server_filter}"

            login_line: str = f"user {self._config.callsign} pass {password} vers {version}{filter_string}"
            await self._write(login_line)

    async def close(self) -> None:
        async with self._lock:
            self._keep_running = False

            if self._task_rx is not None:
                self._task_rx.cancel()
                self._task_rx = None

            if self._sock_reader is not None:
                self._sock_reader = None

            if self._sock_writer is not None:
                self._sock_writer.close()
                self._sock_writer = None

    async def gather(self) -> None:
        try:
            await asyncio.gather(self._task_rx)
        except CancelledError:
            pass

    async def _write(self, data: str) -> None:
        _logger.debug(f"[     TX >>> ] {data}")

        rawdata: bytes = data.encode() + b"\r\n"
        self._sock_writer.write(rawdata)
        await self._sock_writer.drain()

    async def _loop(self) -> None:
        while self._keep_running:
            try:
                raw_line: bytes = await self._sock_reader.readuntil()
            except CancelledError:
                break
            except IncompleteReadError:
                break

            line: str = raw_line.decode("utf-8", "ignore").strip()
            if not line:
                break

            _logger.debug(f"[ <<< RX     ] {line}")

            if self._callback is not None:
                await self._callback(line)

    @staticmethod
    def passcode(callsign: str) -> str:
        callsign = callsign.split("-")[0].upper()

        code = 0x73e2
        for i, char in enumerate(callsign):
            code ^= ord(char) << (8 if not i % 2 else 0)

        return "%d" % (code & 0x7fff)

    @staticmethod
    def version() -> str:
        return __VERSION__
