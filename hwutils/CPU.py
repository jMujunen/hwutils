# TODO:
# *  - [x] Add suppport for specifying which CPU to query

import datetime
import pandas as pd
import re
import subprocess
from pathlib import Path

clock_speed_regex = re.compile(r"(cpu MHz)\s+:\s+([\d.]+)")
cpu_voltage_regex = re.compile(r"([^+]\d{1,3}\.\d{2,})")
cpu_temp_regex = re.compile(r"(Core \d+).*(\d\d\.\d).*\(high.*\)")
name_regex = re.compile(r"Model name:\s+(.*)")
digit_regex = re.compile(r"\d+\.?\d*")


class CpuData:
    """The object contains information about the CPU, including its clock speed,
    voltage, temperature and name."""

    def __init__(self):
        """Initialize an instance of `CpuData`.

        Returns
        ------
            CpuData: An instance of a class containing data about the CPU.
        """
        self.type = "CPU"
        self.update()

    def update(self, spec="All") -> tuple[pd.DataFrame, ...]:  # dict[str, int]:
        """Read values from /proc/cpuinfo and parse accordingly."""

        # Parse CPU clocks
        self.__dict__.update({"clocks": self.clocks, "temps": self.temps})
        return self.clocks, self.temps

    @property
    def clocks(self) -> pd.DataFrame:
        """Return a DataFrame containing information about each CPU's clock speed."""
        content = Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines()
        raw_data = [tuple(line.split(":")) for line in content if ":" in line]
        clocks = (round(float(value.strip())) for key, value in raw_data if "cpu MHz" in key)
        return pd.DataFrame(clocks, columns=["Value"], dtype="int")

    @property
    def temps(self) -> pd.DataFrame:
        """Return a DataFrame containing information about each CPU's temperature."""
        sensors = subprocess.check_output("sensors").decode().split("\n")
        sensorinfo = [tuple(line.split(":")) for line in sensors if ":" in line]
        temps = (
            round(float(value.split()[0].strip("°C+")))
            for key, value in sensorinfo
            if "Core" in key
        )
        return pd.DataFrame(temps, columns=["Value"], dtype="int")

    @property
    def voltage(self) -> float:
        """Queries the voltage of the CPU and returns it.
        The voltage is rounded to three decimal places.
        """
        cpu_voltage_subproccess = subprocess.run(
            ["echo $(sensors | grep VIN3)"], shell=True, stdout=subprocess.PIPE, check=False
        ).stdout.decode("utf-8")
        raw_value = cpu_voltage_regex.search(cpu_voltage_subproccess).group(1)
        cpu_voltage = raw_value.strip()
        if len(cpu_voltage) == 4:
            return round(float(cpu_voltage.strip()), 3)
        if len(cpu_voltage) == 6:
            return round((float(cpu_voltage) / 1000), 3)
        return 0.0

    def dict(self) -> dict:
        """Return a dictionary containing all the information."""

        return {
            "cpu_temp": round(self.temps["Value"].mean()),
            "cpu_clock": round(self.clocks["Value"].mean()),
            "cpu_voltage": self.voltage,
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(avg_clock={round(self.clocks['Value'].mean())} MHz, avg_temp={round(self.temps['Value'].mean())}°C, voltage={self.voltage}V)"
