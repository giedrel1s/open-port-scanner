import asyncio
import ipaddress
from src.port_definitions import PORT_RANGES
from src.scan_utils import scan_port_range

OPEN_PORTS: list[int] = []


async def main() -> None:
	target_ip = None

	while target_ip is None:
		user_input = input("Enter target IPv4 address: ").strip()

		if validate_ip(user_input):
			target_ip = user_input
		else:
			print("Invalid IPv4 address.", flush=True)

	for item in PORT_RANGES:
		await scan_port_range(item, target_ip, cache_port)

	print(f"\nOpen ports: {OPEN_PORTS}")


def cache_port(port: int, cache: list[int] | None = None) -> None:
	if cache is None:
		cache = OPEN_PORTS

	cache.append(port)


def validate_ip(target: str) -> bool:
	try:
		ipaddress.IPv4Address(target)
		return True
	except ipaddress.AddressValueError:
		return False


if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("\nScan cancelled by user.")
	except Exception as e:
		print(f"\nAn error occurred: {e}")
