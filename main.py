import sys
import asyncio
import ipaddress

from port_range import DEFAULT_RANGES
from port_scanner import PortScanner


async def main() -> None:
	target_ip = None

	while target_ip is None:
		user_input = input("Enter target IPv4 address: ").strip()

		if validate_ip(user_input):
			target_ip = user_input
		else:
			print("Invalid IPv4 address.", flush=True)

	scanner = PortScanner(target_ip)

	for port_range in DEFAULT_RANGES:
		scanner.register_range(port_range)

	open_ports = await scanner.scan()

	print(f"\nOpen ports: {open_ports}")


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
		sys.exit(1)
	except Exception as e:
		print(f"\nAn error occurred: {e}")
		sys.exit(1)
