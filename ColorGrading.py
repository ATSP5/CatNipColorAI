"""Tonal colour correction settings applied after colorization.

Every value at its default leaves the colours exactly as DDColor made them.
The settings live in ColorAIConfig.grading; KROK 2 run arguments such as
"temperature=25 saturation=1.3" override them for one run.
"""

from dataclasses import dataclass, fields, replace
from typing import Dict, Iterable, Tuple


@dataclass(frozen=True)
class ColorGrading:
	temperature: float = 0.0
	tint: float = 0.0
	saturation: float = 1.0
	vibrance: float = 0.0
	hue_shift: float = 0.0
	highlight_warmth: float = 0.0
	shadow_warmth: float = 0.0
	cast_removal: float = 0.0

	# Allowed range of each setting, inclusive.
	RANGES = {
		"temperature": (-100.0, 100.0),
		"tint": (-100.0, 100.0),
		"saturation": (0.0, 3.0),
		"vibrance": (-100.0, 100.0),
		"hue_shift": (-180.0, 180.0),
		"highlight_warmth": (-100.0, 100.0),
		"shadow_warmth": (-100.0, 100.0),
		"cast_removal": (0.0, 1.0),
	}

	def __post_init__(self):
		for name, (low, high) in self.RANGES.items():
			value = getattr(self, name)
			if not low <= value <= high:
				raise ValueError("Korekta barw: %s=%g poza zakresem %g..%g" % (name, value, low, high))

	@property
	def is_neutral(self) -> bool:
		return self == ColorGrading()

	def with_args(self, args: Iterable[str]) -> "ColorGrading":
		"""A copy with "name=value" run arguments applied; other arguments are ignored."""
		names = [f.name for f in fields(self)]
		changes: Dict[str, float] = {}
		for arg in args:
			if "=" not in arg:
				continue
			name, value = arg.lstrip("-").split("=", 1)
			name = name.strip().lower().replace("-", "_")
			if name not in names:
				raise ValueError("Nieznane ustawienie korekty barw '%s' - dozwolone: %s" % (name, ", ".join(names)))
			try:
				changes[name] = float(value.replace(",", "."))
			except ValueError:
				raise ValueError("Korekta barw: '%s' nie jest liczba (%s)" % (value, name))
		return replace(self, **changes)

	def summary(self) -> str:
		changed: Tuple[str, ...] = tuple(
			"%s=%g" % (f.name, getattr(self, f.name))
			for f in fields(self) if getattr(self, f.name) != f.default)
		return ", ".join(changed) or "brak (kolory DDColor bez zmian)"
