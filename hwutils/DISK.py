#!/usr/bin/env python3
"""Disk.py - Query disk information for HWINFO"""

import psutil

from .Sensor import Sensor


class Disk(Sensor):
    def __init__(self, mountpoint: str, friendly_name: str | None = None):
        self.mountpoint = mountpoint
        self.friendly_name = friendly_name
        super().__init__("disk")

    def percent_used(self) -> float:
        return psutil.disk_usage(self.mountpoint).percent

    def __str__(self) -> str:
        return str(
            f"""{self.mountpoint}
    {self.friendly_name} Usage: {self.percent_used()}%\n"""
        )


# Example
if __name__ == "__main__":
    ROOTFS = Disk("/", "Root")
    HOME = Disk("/home/", "Home")
    WD40_external = Disk("/mnt/hdd/", "4TB External")
    # SSD = Disk('/mnt/ssd/')
    print(ROOTFS)
    print(WD40_external)
    print(HOME)
