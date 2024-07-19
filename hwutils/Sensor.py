#!/usr/bin/env python3
"""Contains the base `Sensor`
`Sensor` is a child of every other object defined in this package"""


class Sensor:
    """Base class for all hardware objects."""

    def __init__(self, sensor_type: str) -> None:
        """Constructor method for the `Sensor` class."""
        self.sensor_type = sensor_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"
