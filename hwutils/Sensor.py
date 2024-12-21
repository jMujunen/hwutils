"""Contains the classes for sensor readings and system statistic."""

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field, fields
from datetime import datetime
from enum import Enum
from random import randint
from typing import Any
from ThreadPoolHelper import Pool

from hwutils import CpuData, GpuData, Interface
from hwutils.SYS import Misc


type Hwinfo = GpuData | CpuData | Interface | Misc
pool = Pool()


class SensorType(Enum):
    """Enum for the type of a sensor."""

    TEMP = ("C", 0)
    VOLTAGE = ("V", 5)
    CLOCK = ("MHz", 2)
    PING = ("ms", 9)
    USAGE = ("%", 1)
    POWER = ("W", 4)
    FAN = ("%", 11)

    def __init__(self, unit: int, id: str) -> None:  # noqa: A002
        """Initialize the enum with a unit and id."""
        self.unit = unit
        self.id = id


@dataclass
class SensorReading:
    """A class representing a sensor reading with its value, timestamp and type.

    Attributes
        id (str): The ID of the reading.
        name (str): The name of the reading.
        sensor_type (SensorType): The type of the reading.
        value (float): The value of the reading.
        timestamp (datetime): The timestamp of the reading.
    """

    # __slots__ = ["id", "name", "sensor_type", "timestamp", "value"]

    id: str = field(init=True, repr=True, default_factory=str)
    name: str = field(init=True, repr=True, default_factory=str)
    sensor_type: SensorType = field(
        init=True,
        repr=True,
        default_factory=lambda: list(SensorType)[randint(0, len(list(SensorType)) - 1)],
    )
    value: float = field(init=True, repr=True, default_factory=float)
    timestamp: datetime = field(init=True, repr=True, default_factory=datetime.now)
    func: Callable = field(init=True, repr=False, default_factory=lambda x: x)

    def __post_init__(self) -> "SensorReading":
        """Post-initialization hook."""
        self.value = self.func()
        return self

    def update(self) -> float:
        """Update the value and timestamp."""
        self.value = self.func()
        self.timestamp = datetime.now()
        return self.value

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"SensorReading({self.name}, {self.value} {self.sensor_type.unit})"


def generate_readings(instance: Hwinfo) -> list[SensorReading]:
    """Create a list of SensorReading objects from an instance.

    Args:
        instance (Hwinfo): The instance to create SensorReading objects from.

    Returns:
        list[SensorReading]: A list of SensorReading objects.
    """
    readings = []
    for f in fields(instance):
        attr_value = getattr(instance, f.name)
        if isinstance(attr_value, int | float):
            sensor_type = f.name.upper()
            for enum in SensorType:
                if enum.name in sensor_type:
                    sensor_type = enum
                    break

            reading = SensorReading(
                id=instance.type,
                name=f.name,
                sensor_type=sensor_type,
                func=lambda x=f: instance.dict().get(x.name),
            )
            readings.append(reading)
    return readings


@dataclass
class SensorGroup:
    """A group of sensor readings.

    Attributes
        cls: GpuData | CpuData: The data source
        name (str): The name of the sensor group.
        description (str): A description of the sensor group.
        readings (list[SensorReading]): A list of SensorReading objects.
    """

    cls: Hwinfo
    name: str = field(repr=True, init=False)
    description: str = field(default_factory=str, kw_only=True, repr=True)
    readings: list[SensorReading] = field(default_factory=list, repr=False, kw_only=True)

    def __post_init__(self) -> None:
        if not hasattr(self, "name"):
            self.name = self.cls().__class__.__name__.upper()  # type: ignore
            self.readings = list(generate_readings(self.cls()))  # type: ignore

    def add_reading(self, reading: SensorReading) -> None:
        """Add a sensor reading to the group.

        Args:
            reading (SensorReading): The sensor reading to be added.
        """
        self.readings.append(reading)

    def update(self) -> dict[str, Any]:
        """Update the sensor group and return a dictionary of readings."""
        # if not hasattr(self, "name"):
        # self.name = self.cls().__class__.__name__.upper()  # type: ignore
        # self.readings = create_sensor_readings_from_instance(self.cls())  # type: ignore
        updated_values = self.cls().dict()  # type: ignore
        return {reading.name: updated_values[reading.name] for reading in self}

    def __iter__(self) -> Iterator[SensorReading]:
        """Iterate over the sensor group's readings."""
        yield from self.readings

    def __getitem__(self, index, /) -> SensorReading:
        """Get a specific sensor reading by index."""
        return self.readings[index]

    def __len__(self) -> int:
        return len(list(self.__iter__()))


@dataclass
class SystemStats(tuple):
    """A class to represent a collection of sensor groups and miscellaneous readings.

    Attributes
        CPU (SensorGroup): A sensor group representing CPU data.
        GPU (SensorGroup): A sensor group representing GPU data.
        MISC (SensorGroup): A sensor group for miscellaneous readings.
        ping (SensorReading | None): An optional sensor reading for network latency.
    """

    CPU: SensorGroup = field(default_factory=lambda: SensorGroup(CpuData, description="Cpu Stats"))
    GPU: SensorGroup = field(default_factory=lambda: SensorGroup(GpuData, description="Gpu Stats"))
    MISC: SensorGroup = field(
        default_factory=lambda: SensorGroup(Misc, description="Miscellaneous stats")
    )
    _pool = Pool()

    def update(self) -> tuple[dict, ...]:
        """Update the system stats with current readings."""
        return tuple(self._pool.execute(lambda x: x.update(), self, progress_bar=False))
        # yield result

    def __iter__(self) -> Iterator:
        """Iterate over the system stats' sensor groups."""
        for v in self.__dict__.values():
            if v:
                yield v

    def __str__(self) -> str:
        """Return a string representation of the system stats."""
        return "\n".join([str(sensor_group) for sensor_group in self])

    def __len__(self) -> int:
        """Return the number of sensor groups in the system stats."""
        return len(list(self.__iter__()))

    def __getitem__(self, index, /):
        """Get a specific sensor group by index."""
        return list(self.__iter__())[index]

    def dict(self) -> dict[str, int]:
        return {k: v for group in self.update() for k, v in group.items()}
