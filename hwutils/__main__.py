"""__main__.py - Command-line interface for HWINFO."""

import argparse

from .CPU import CpuData
from .DISK import Disk
from .GPU import GpuData
from .NET import Interface
from .SYS import Ram, Temp


def parse_args():  # -> argparse.Namespace:
    """Parse command-line arguments."""
    # Main parser
    parser = argparse.ArgumentParser(description="Query hardware information.")
    subparsers = parser.add_subparsers(dest="command")

    # CPU command
    subparsers.add_parser("cpu", help="Display CPU information.")

    # GPU command
    subparsers.add_parser("gpu", help="Display GPU information.")

    # Disk command
    disk_parser = subparsers.add_parser("disk", help="Display disk usage information.")
    disk_parser.add_argument("mountpoint", type=str, help="The mount point of the disk to query.")

    # RAM command
    ram_parser = subparsers.add_parser("ram", help="Display RAM information.")
    ram_parser.add_argument(
        "--swap", action="store_true", help="Query swap memory instead of physical RAM."
    )
    ram_parser.add_argument("--usage", action="store_true", help="Query RAM usage as a percent.")

    # Network interface command
    net_parser = subparsers.add_parser("net", help="Display network interface information.")
    net_parser.add_argument(
        "--interface", type=str, default="wlan0", help="Specify the network interface to query."
    )

    # Temperature command
    subparsers.add_parser("temp", help="Display temperature information.")

    # Parse arguments and execute commands
    return parser.parse_args()


def main(args) -> str | None:
    ret = None
    if hasattr(args, "command"):
        # hwdata_init()  # Ensure the package is initialized
        match args.command:
            case "cpu":
                ret = repr(CpuData())
            case "gpu":
                ret = repr(GpuData())
            case "disk":
                ret = repr(Disk(args.mountpoint))
            case "ram" | "mem":
                ret = repr(Ram())
            case "net":
                ret = repr(Interface(args.interface))
            case _:
                ret = None
    else:
        ret = "Error parsing subparser: No attribute 'command'"
    return ret


if __name__ == "__main__":
    args = parse_args()
    print(main(args))
