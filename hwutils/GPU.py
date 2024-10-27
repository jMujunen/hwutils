import datetime
import re
import subprocess
from dataclasses import dataclass

digit_regex = re.compile(r"\d+\.?\d*")


@dataclass
class GpuData:
    """A class for querying GPU data using nvidia-smi tool.

    Attributes
    ----------
        type (str): Type of the device, always 'GPU'.
        name (str): Name of the GPU.

    Properties:
    -----------
        temp : str
            Current temperature of the GPU core.
        core_temp : str
            Current temperature of the GPU core.
        memory_temp : str
            Current temperature of the GPU memory.
        core_clock : str
            Current graphics clock speed of the GPU in MHz.
        max_core_clock : str
            Maximum graphics clock speed of the GPU in MHz.
        memory_clock : str
            Current memory clock speed of the GPU in MHz.
        max_memory_clock : str
            Maximum memory clock speed of the GPU in MHz.
        memory_usage : str
            Current utilization of the GPU memory as a percentage.
        voltage : float
            Voltage of the GPU in volts.
        power : int
            Current power draw of the GPU in Watts.
        core_usage : str
            Current utilization of the GPU cores as a percentage.
        timestamp : str
            The time when nvidia-smi was last run.

    Methods
        gpu_name(short=False) -> str:
            Return the name of the GPU. If short is True, return only model number.

    """

    def __init__(self):
        self.type = "GPU"
        print(self.update())

    def update(self):
        """Update all properties."""
        cmd = "nvidia-smi --query-gpu=temperature.gpu,clocks.current.graphics,clocks.current.memory,utilization.memory,power.draw,utilization.gpu,fan.speed --format=csv,noheader"
        output = subprocess.getoutput(cmd).splitlines()
        output = [digit_regex.findall(line) for line in output]
        (
            self.gpu_temp,
            self.gpu_core_clock,
            self.gpu_memory_clock,
            self.memory_usage,
            self.power,
            self.core_usage,
            self.fan_speed,
        ) = (round(float(x)) for x in output[0])
        self.gpu_voltage = self.voltage
        self.__dict__.update({"voltage": float(self.voltage)})
        return self.__dict__

    @property
    def voltage(self) -> float:
        """Get the voltage of the GPU in volts.

        Returns
        -----------

            float: Voltage of the GPU in volts.
        """
        voltage_regex = re.compile(r"(\d+.\d+)")
        voltage_subprocess = subprocess.run(
            'nvidia-smi  -q  --display=Voltage  |  grep -o -P "Graphics.*"',
            shell=True,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        matches = "  ".join(voltage_regex.findall(voltage_subprocess))
        volts = round(float(matches) / 1000, 2)
        return float(volts)

    def gpu_name(self, short=False) -> str:
        """Get the name of GPU."""
        name_regex = re.compile(
            r"(AMD|NVIDIA|Intel)\s?(\s?GeForce\s?|\s?Radeon\s?)\s?(\sGTX\s?|\s?RTX\s?)(.*)"
        )
        subout = subprocess.run(
            "nvidia-smi  --query-gpu=name  --format=csv,noheader",
            shell=True,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        matches = name_regex.findall(subout)
        if short:
            self.name = matches[0][-1]
        else:
            self.name = "  ".join(matches[0])
        return self.name

    @property
    def timestamp(self) -> datetime.datetime:
        """Return the current time as a formatted string.

        Returns

            str : Current time as formatted string

        """
        return datetime.datetime.now()

    def dict(self) -> dict[str, int]:
        """Return dictionary representation of GPU object."""
        self.update()
        return {k: v for k, v in vars(self).items() if k not in ["type", "name"]}

    def __repr__(self):
        """Return Class representation."""
        return f"{self.__class__.__name__}(temp={self.gpu_temp}, usage={self.core_usage}, voltage={self.gpu_voltage}"


# Example
if __name__ == "__main__":
    gpu = GpuData()
