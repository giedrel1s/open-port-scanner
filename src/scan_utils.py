import asyncio
import sys
from typing import Callable
from src.port_definitions import PortRange

MAX_CONCURRENCY = 200


async def check_port(target_ip: str, port: int) -> int | None:
	try:
		_, writer = await asyncio.open_connection(target_ip, port)
	except (ConnectionRefusedError, OSError):
		return None

	writer.close()
	await writer.wait_closed()
	return port


async def scan_port_range(
	port_range: PortRange,
	target: str,
	cache: Callable[[int], None],
	update_interval: int = 200,
) -> None:
	semaphore = asyncio.Semaphore(MAX_CONCURRENCY)
	total_ports = port_range.end - port_range.start
	label = f"range {port_range.start}-{port_range.end}"
	bar_width = 20

	async def probe(port: int) -> int | None:
		async with semaphore:
			return await check_port(target, port)

	tasks = [
		asyncio.create_task(probe(port))
		for port in range(port_range.start, port_range.end)
	]

	for i, task in enumerate(asyncio.as_completed(tasks), 1):
		result = await task

		if i % update_interval == 0 or i == total_ports:
			filled = int(bar_width * i / total_ports)
			bar = "\u2588" * filled + "\u2591" * (bar_width - filled)
			sys.stdout.write(f"\r{bar} {i}/{total_ports} (range {label})")
			sys.stdout.flush()

		if result is not None:
			cache(result)

	sys.stdout.write(f"\r \u2713 {total_ports}/{total_ports} (range {label})\n")
