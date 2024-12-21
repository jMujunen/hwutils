import re
from statistics import mean
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

clock_speed_regex = re.compile(r"(cpu MHz)\s+:\s+([\d.]+)")
cpu_voltage_regex = re.compile(r"([^+]\d{1,3}\.\d{2,})")
cpu_temp_regex = re.compile(r"(Core \d+).*(\d\d\.\d).*\(high.*\)")
name_regex = re.compile(r"Model name:\s+(.*)")
digit_regex = re.compile(r"\d+\.?\d*")


@dataclass
class CpuData:
    """A class for querying CPU data.


    | Attributes           | Description                                        |
    |:--------------------|:--------------------------------------------------- |
    | cpu_max_temp  (int) | The maximum value of all the cores                  |
    | cpu_avg_temp (int)  | Current temperature of the CPU core.                |
    | cpu_max_clock (int) | The maximum value of all cores clock speed.         |
    | cpu_voltage (float) | Current voltage of the CPU core in Volts.           |
    | cpu_avg_clock (int) | Current gpu memory clock speed in MHz.              |
    | type (str)          | Type of the device, always 'CPU'.                   |



    | Method              | Description                                         |
    |:--------------------|:--------------------------------------------------- |
    | update() -> CpuData | Read values from /proc/cpuinfo and parse accordingly. |
    | dict() -> dict[str, float| int] | Return a dictionary containing all the information. |

    """

    cpu_voltage: float = field(default_factory=float)
    cpu_avg_clock: int = field(default_factory=int)
    cpu_avg_temp: int = field(default_factory=int)
    cpu_max_clock: int = field(default_factory=int)
    cpu_max_temp: int = field(default_factory=int)

    def __post_init__(self):
        """Update upon initialization."""
        self.type = "CPU"
        self.update()

    def update(self) -> "CpuData":
        """Read values from /proc/cpuinfo and parse accordingly.

        Returns
        -------
            CpuData: The updated instance of the class.
        """
        # Extract clock speeds from /proc/cpuinfo
        content = Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines()
        raw_data = [tuple(line.split(":")) for line in content if ":" in line]
        clocks = [round(float(value.strip())) for key, value in raw_data if "cpu MHz" in key]

        # Extract temperatures from sensors
        sensors = subprocess.check_output("sensors").decode().split("\n")
        sensorinfo = [tuple(line.split(":")) for line in sensors if ":" in line]
        temps = [
            round(float(value.split()[0].strip("°C+")))
            for key, value in sensorinfo
            if "Core" in key
        ]
        # Extract voltage from sensors output

        voltage = next(item for item in sensorinfo if "VIN2" in item[0])[1].split()[0]

        # Calculate max | mean clock, temperature
        self.cpu_max_clock = round(max(clocks))
        self.cpu_max_temp = round(max(temps))
        self.cpu_avg_clock = round(mean(clocks))
        self.cpu_avg_temp = round(mean(temps))

        # Convert voltage to a standardized format
        self.cpu_voltage = self._voltage_unit_conversion(voltage)
        return self

    def dict(self) -> dict[str, float | int]:
        """Return a dictionary containing all the information.

        Returns
        -------
            dict[str, float | int]: A dictionary with CPU data.
        """
        self.update()
        return {
            "cpu_max_temp": self.cpu_max_temp,
            "cpu_avg_temp": self.cpu_avg_temp,
            "cpu_max_clock": self.cpu_max_clock,
            "cpu_avg_clock": self.cpu_avg_clock,
            "cpu_voltage": self.cpu_voltage,
        }

    @staticmethod
    def _voltage_unit_conversion(value) -> float:
        """Convert voltage value to a standardized format.

        Parameters
        ----------
            value (str):  The raw voltage value from sensors output.

        Returns
        -------
            float: The converted voltage value.
        """
        if len(value) == 4:
            return round(float(value.strip()), 3)
        if len(value) == 6:
            return round((float(value) / 1000), 3)
        return 0.0
