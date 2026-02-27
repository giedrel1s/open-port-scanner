from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class PortRange:
	name: str
	start: int
	end: int

	def __post_init__(self) -> None:
		if self.start < 0 or self.end > 65536:
			raise ValueError("Port range must be between 0 and 65536")
		if self.start >= self.end:
			raise ValueError("Start port must be less than end port")

	def __len__(self) -> int:
		return self.end - self.start

	def __iter__(self) -> Iterator[int]:
		return iter(range(self.start, self.end))


DEFAULT_RANGES: list[PortRange] = [
	PortRange(name="standard", start=0, end=1024),
	PortRange(name="services", start=1024, end=49152),
	PortRange(name="private", start=49152, end=65536),
]
