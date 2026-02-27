from typing import NamedTuple


class PortRange(NamedTuple):
	start: int
	end: int


class PortConfig(NamedTuple):
	standard: PortRange
	services: PortRange
	private: PortRange


PORT_RANGES = PortConfig(
	standard=PortRange(0, 1024),
	services=PortRange(1024, 49152),
	private=PortRange(49152, 65536),
)
