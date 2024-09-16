#!/usr/bin/env python3
"""__init__.py - Initializes the hwutils package."""

from .CPU import CpuData
from .DISK import Disk
from .FAN import Fan
from .GPU import GpuData
from .NET import Interface

# from .PROC import Proc
from .Sensor import Sensor, SensorReading, SystemStats
from .SYS import Misc, Ram, Temp

__all__ = [
    "GpuData",
    "CpuData",
    "Fan",
    "Ram",
    "Misc",
    "Interface",
    "Disk",
    "Temp",
    # "Proc",
    "Sensor",
    "SensorReading",
    "SystemStats",
]


# print(GpuData().__doc__)
