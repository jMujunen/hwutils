from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SensorType(Enum):
    TEMP = "TEMP"
    VOLTAGE = "VOLTAGE"
    CLOCK_SPEED = "CLOCK_SPEED"
    PING = "PING"
    USAGE = "USAGE"


@dataclass
class SensorReading:
    id: int  # Unique identifier for the sensor reading
    sensor_type: SensorType
    value: float  # Value of the sensor reading (e.g. temperature in Celsius, voltage in volts)
    timestamp: datetime  # Timestamp when the sensor reading was taken


@dataclass
class SystemStats:
    cpu_temp: SensorReading | None = None
    cpu_voltage: SensorReading | None = None
    gpu_memory_clock: SensorReading | None = None
    ping: SensorReading | None = None

    def update(self):
        return 1


system_stats = SystemStats()
system_stats.cpu_temp = SensorReading(
    id=1,
    sensor_type=SensorType.TEMP,
    value=40.0,  # Temperature in Celsius
    timestamp=datetime.now(),
)
system_stats.gpu_memory_clock = SensorReading(
    id=2,
    sensor_type=SensorType.CLOCK_SPEED,
    value=1500.0,  # Memory clock speed in MHz
    timestamp=datetime.now(),
)


class Sensor:
    """Base class for all hardware objects."""

    def __init__(self, sensor_type: str) -> None:
        """Construct the object."""
        self.sensor_type = sensor_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"
