import re
import subprocess
from dataclasses import dataclass, field

import psutil

temp_regex = re.compile(r"(\d{2})")


@dataclass
class Temp:
    """Dataclass for temperature sensor data."""

    type: str = "SYS"
    temp: int = field(default_factory=int)

    def update(self) -> int:
        """Get the temperature data from the sensors using a subprocess."""

        command_output = subprocess.run(
            "sensors | grep 'Sensor 2' | awk  '{print $3}'",
            shell=True,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        self.temp = int(temp_regex.search(command_output).group())  # type: ignore

        # Extract the first matching temperature value
        return self.temp

    def __str__(self):
        """Return a string representation of the temperature data."""
        current_temp = self.temp
        return f"{current_temp}°C"

    def __int__(self):
        """Return current temperature as int."""
        current_temp = self.temp
        return int(current_temp) if int(current_temp) else 0

    def dict(self) -> dict[str, float]:
        """Return a dictionary representation of the temperature data."""
        return {"sys_temp": int(self.temp)}


@dataclass
class Misc:
    ram_usage: int = field(default_factory=int)
    sys_temp: int = field(default_factory=int)
    ping: float = field(default_factory=float)
    type: str = "SYS"

    def update(self) -> "Misc":
        command_output = subprocess.run(
            "sensors | grep 'Sensor 2' | awk  '{print $3}'",
            shell=True,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()

        result = subprocess.getoutput(
            'ping -c 1 -W 1.5 1.1.1.1 | sed -u "s/^.*time=//g; s/ ms//g; s/^PING.*//g; s/^---.*//g; s/^.*packets.*//g; s/^rtt.*//g"',
        ).strip()
        try:
            self.ping = round(float(result), 2)
        except ValueError:
            self.ping = -1.0

        self.sys_temp = int(temp_regex.search(command_output).group())  # type: ignore
        self.ram_usage = int(psutil.virtual_memory().percent)

        return self

    def dict(self) -> dict[str, float | int]:
        self.update()
        return {"ram_usage": self.ram_usage, "sys_temp": self.sys_temp, "ping": self.ping}

    @staticmethod
    def uptime():
        command_output = subprocess.run(
            "uptime -p", shell=True, capture_output=True, text=True, check=False
        ).stdout.strip()
        return re.search(r"(\d+\s+\w+.*)+", command_output).group()  # type: ignore

    @staticmethod
    def users() -> list[tuple]:
        users = psutil.users()
        names = []
        terminals = []
        for user in users:
            names.append(user.name)
            terminals.append(user.terminal)
        return list(zip(names, terminals, strict=False))
