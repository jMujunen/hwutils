import re
import subprocess
from dataclasses import dataclass, field

digit_regex = re.compile(r"\d+\.?\d*")


@dataclass
class GpuData:
    """A class for querying GPU data using nvidia-smi tool.

    Attributes
    ----------
        gpu_core_temp : int
            Current temperature of the GPU core.
        gpu_core_clock : str
            Current gpu core clock speed of the GPU in MHz.
        gpu_memory_clock : int
            Current gpu memory clock speed in MHz.
        gpu_memory_usage : int
            Current gpu memory usage as a percentage

        gpu_power : int
            Current power draw of the GPU in Watts.
        gpu_core_usage
            Current gpu core usage as a percentage
        gpu_voltage : float
            Voltage of the GPU in volts.
        gpu_fanspeed: int
            Current Fan speed as a percentage
        name: str
            Gpu friendly name
        type : str
            Type of the device, always 'GPU'.

    Methods
    -------
       update : GpuData
            Update all properties.
       dict : dict[str, int]
            Return dictionary representation of GPU object.
       _gpu_name : str
            Get the name of the GPU.
       _voltage : float
            Get the voltage of the GPU in volts.

    """

    gpu_core_temp: int = field(default_factory=int)
    gpu_core_clock: int = field(default_factory=int)
    gpu_memory_clock: int = field(default_factory=int)
    gpu_memory_usage: int = field(default_factory=int)
    gpu_power: int = field(default_factory=int)
    gpu_core_usage: int = field(default_factory=int)
    gpu_fanspeed: int = field(default_factory=int)
    gpu_voltage: float = field(default_factory=float)
    name: str = field(default_factory=str)
    type: str = "GPU"

    def __post_init__(self) -> None:
        self.name = self._gpu_name()
        self.update()

    def update(self) -> "GpuData":
        """Update all properties."""
        cmd = "nvidia-smi --query-gpu=temperature.gpu,clocks.current.graphics,clocks.current.memory,utilization.memory,power.draw,utilization.gpu,fan.speed --format=csv,noheader"
        output = subprocess.getoutput(cmd).splitlines()
        output = [digit_regex.findall(line) for line in output]
        (
            self.gpu_core_temp,
            self.gpu_core_clock,
            self.gpu_memory_clock,
            self.gpu_memory_usage,
            self.gpu_power,
            self.gpu_core_usage,
            self.gpu_fanspeed,
        ) = (round(float(x)) for x in output[0])
        self.gpu_voltage = round(self._voltage(), 2)
        return self

    def dict(self) -> dict[str, int]:
        """Return dictionary representation of GPU object."""
        self.update()
        return {k: v for k, v in vars(self).items() if k not in {"type", "name"}}

    @staticmethod
    def _voltage() -> float:
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
        if not matches:
            return 0.0
        volts = round(float(matches) / 1000, 2)
        return float(volts)

    def _gpu_name(self, short=False) -> str:
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


# Example
if __name__ == "__main__":
    gpu = GpuData()
    print(gpu)
