"""Scenario inputs. Distances are metres, times seconds, angles degrees."""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class OrbitGroup:
    name: str
    count: int
    altitude_m: float
    inclination_deg: float
    color: tuple[int, int, int, int]
    raan_offset_deg: float = 0.0


DEFAULT_GROUPS = (
    OrbitGroup("LEO", 5, 550_000.0, 53.0, (0, 190, 255, 255)),
    OrbitGroup("MEO", 2, 10_000_000.0, 56.0, (255, 160, 30, 255), 45.0),
)


@dataclass(frozen=True)
class SimulationConfig:
    duration_s: float = 12 * 3600.0
    step_s: float = 10.0
    groups: tuple[OrbitGroup, ...] = DEFAULT_GROUPS

    def validate(self):
        if not all(isfinite(x) and x > 0 for x in (self.duration_s, self.step_s)):
            raise ValueError("Duration and time step must be finite and positive.")
        if self.step_s > self.duration_s:
            raise ValueError("Time step cannot exceed duration.")
        if not self.groups or len({g.name for g in self.groups}) != len(self.groups):
            raise ValueError("Provide orbit groups with unique names.")
        for group in self.groups:
            if not isinstance(group.count, int) or group.count < 1:
                raise ValueError("Each group needs a positive integer satellite count.")
            if not isfinite(group.altitude_m) or group.altitude_m <= 0:
                raise ValueError("Altitude must be finite and positive.")
            if not isfinite(group.inclination_deg) or not 0 <= group.inclination_deg <= 180:
                raise ValueError("Inclination must be between 0 and 180 degrees.")
            if not isfinite(group.raan_offset_deg):
                raise ValueError("RAAN offset must be finite.")
