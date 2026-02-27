import asyncio
import sys

from port_range import PortRange


class PortScanner:
	def __init__(self, target_ip: str, max_concurrency: int = 200) -> None:
		self._target_ip = target_ip
		self._max_concurrency = max_concurrency
		self._ranges: list[PortRange] = []
		self._open_ports: list[int] = []

	@property
	def target_ip(self) -> str:
		return self._target_ip

	@property
	def open_ports(self) -> list[int]:
		return list(self._open_ports)

	def register_range(self, port_range: PortRange) -> None:
		self._ranges.append(port_range)

	async def scan(self) -> list[int]:
		self._open_ports.clear()

		for port_range in self._ranges:
			await self._scan_range(port_range)

		return sorted(self._open_ports)

	async def _scan_range(
		self, port_range: PortRange, update_interval: int = 200
	) -> None:
		semaphore = asyncio.Semaphore(self._max_concurrency)
		total_ports = len(port_range)
		bar_width = 20

		async def probe(port: int) -> int | None:
			async with semaphore:
				return await self._check_port(port)

		tasks = [asyncio.create_task(probe(port)) for port in port_range]

		for i, task in enumerate(asyncio.as_completed(tasks), 1):
			result = await task

			if i % update_interval == 0 or i == total_ports:
				filled = int(bar_width * i / total_ports)
				bar = "\u2588" * filled + "\u2591" * (bar_width - filled)
				sys.stdout.write(f"\r{bar} {i}/{total_ports} ({port_range.name})")
				sys.stdout.flush()

			if result is not None:
				self._open_ports.append(result)

		sys.stdout.write(
			f"\r\u2713 {total_ports}/{total_ports} ({port_range.name})\n"
		)

	async def _check_port(self, port: int, timeout: float = 0.1) -> int | None:
		try:
			_, writer = await asyncio.wait_for(
				asyncio.open_connection(self._target_ip, port),
				timeout=timeout,
			)
		except (ConnectionRefusedError, OSError, TimeoutError):
			return None

		writer.close()
		await writer.wait_closed()
		return port
