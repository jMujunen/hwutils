"""Contains the classes for sensor readings and system statistic."""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from random import randint
from typing import Any


class SensorType(Enum):
    TEMP = "C"
    VOLTAGE = "V"
    CLOCK_SPEED = "MHz"
    PING = "ms"


@dataclass
class SensorReading:
    id: int = field(init=True, repr=True, default_factory=int)
    sensor_type: SensorType = field(
        init=True,
        repr=True,
        default_factory=lambda: list(SensorType)[randint(0, len(list(SensorType)) - 1)],
    )
    value: float = field(init=True, repr=True, default_factory=float)
    timestamp: datetime = field(init=True, repr=True, default_factory=datetime.now)
    func: Callable = field(init=True, repr=True, default_factory=lambda x: x)

    def update(self):
        self.value = self.func()  # Call the callable to get the current value
        self.timestamp = datetime.now()
        return self

    def __repr__(self) -> str:
        return f"SensorReading({self.sensor_type}, {self.value} {self.sensor_type.value}) at {self.timestamp}"


@dataclass
class SensorGroup:
    """A group of sensor readings.

    Attributes
        readings (list[SensorReading]): A list of SensorReading objects.
        group_id (int): The unique identifier for the sensor group.
        group_name (str): The name of the sensor group.
        group_description (str): A description of the sensor group.
    """

    readings: list[SensorReading] = field(default_factory=list, init=False, repr=True)
    group_id: int = field(init=True, repr=True, default_factory=int)
    group_name: str = field(init=True, repr=True, default="")
    group_description: str = ""

    def add_reading(self, reading: SensorReading):
        """Add a sensor reading to the group.

        Args:
            reading (SensorReading): The sensor reading to be added.
        """
        self.readings.append(reading)

    def __init__(self, name: str, id: int):
        """Initialize a new SensorGroup object.

        Args:
            name (str): The name of the sensor group.
            id (int): The unique identifier for the sensor group.
        """
        self.group_id = id
        self.group_name = name
        self.readings = []

    def __str__(self):
        """Return a string representation of the SensorGroup object.

        Returns
            str: A string representing the SensorGroup object.
        """
        return f"{self.group_name} ({self.group_id}): {[str(reading) for reading in self.readings]}"


@dataclass
class SystemStats:
    CPU: SensorGroup = field(default_factory=lambda: SensorGroup("CPU", 1))  # CPU sensor group
    GPU: SensorGroup = field(default_factory=lambda: SensorGroup("GPU", 2))  # GPU sensor group
    MISC: SensorGroup = field(default_factory=lambda: SensorGroup("MISC", 3))  # Misc sensor group
    cpu_temp: SensorReading | None = None
    cpu_voltage: SensorReading | None = None
    gpu_memory_clock: SensorReading | None = None
    ping: SensorReading | None = None

    def update(self) -> int:
        """Update the system stats with current readings."""
        for group in [self.CPU.readings, self.GPU.readings, self.MISC.readings]:
            for reading in group:
                if isinstance(reading, SensorReading):
                    print(reading.update())
        return 0


class Sensor:
    """Base class for all hardware objects."""

    def __init__(self, sensor_type: str) -> None:
        """Construct the object."""
        self.sensor_type = sensor_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


if __name__ == "__main__":
    from .CPU import CpuData
    from .GPU import GpuData

    gpudata = GpuData()
    cpudata = CpuData()
    system_stats = SystemStats()

    cpu_group = SensorGroup(name="CPU", id=1)
    cpu_group.add_reading(
        SensorReading(id=1, sensor_type=SensorType.TEMP, func=lambda: cpudata.average_temp)
    )
    cpu_group.add_reading(
        SensorReading(id=2, sensor_type=SensorType.CLOCK_SPEED, func=lambda: cpudata.average_clock)
    )

    gpu_group = SensorGroup("GPU", 2)
    gpu_group.add_reading(
        SensorReading(
            id=2,
            sensor_type=SensorType.CLOCK_SPEED,
            func=lambda: gpudata.update().get("memory_clock"),
        )
    )
    gpu_group.add_reading(
        SensorReading(
            id=1, sensor_type=SensorType.TEMP, func=lambda: gpudata.update().get("core_temp")
        )
    )
