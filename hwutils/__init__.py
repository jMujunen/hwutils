#!/usr/bin/env python3
"""__init__.py - Initializes the hwdata package"""

from .GPU import GpuData
from .CPU import CpuData
from .FAN import Fan
from .DISK import Disk
from .SYS import Temp, Ram, Misc
from .NET import Interface
from .PROC import Proc


__all__ = [
    "GpuData",
    "CpuData",
    "Fan",
    "Ram",
    "Misc",
    "Interface",
    "Disk",
    "Temp",
    # 'Proc',
]

# print(GpuData().__doc__)
