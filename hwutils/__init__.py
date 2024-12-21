"""__init__.py - Initializes the hwutils package."""

from .CPU import CpuData as CpuData
from .DISK import Disk as Disk
from .FAN import Fan as Fan
from .GPU import GpuData as GpuData
from .NET import Interface as Interface

# from .PROC import Proc
from .Sensor import SensorReading, SystemStats

__all__ = [
    "CpuData",
    "Disk",
    "Fan",
    "GpuData",
    "Interface",
    # "Proc",
    "SensorReading",
    "SystemStats",
]


# print(GpuData().__doc__)
