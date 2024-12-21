"""Query network information."""

import subprocess
from dataclasses import dataclass, field

import psutil


@dataclass
class Connections:
    num_conns: int = field(default_factory=int, init=False)
    listening: list = field(
        init=False,
        repr=False,
        default_factory=lambda: list(
            filter(lambda x: x.status == "LISTEN", psutil.net_connections(kind="inet"))
        ),
    )
    established: list = field(
        init=False,
        repr=False,
        default_factory=lambda: list(
            filter(lambda x: x.status == "ESTABLISHED", psutil.net_connections(kind="inet"))
        ),
    )
    listening_ports: set = field(
        init=False,
        repr=False,
        default_factory=lambda: ({
            conn.laddr.port  # type:ignore
            for conn in psutil.net_connections(kind="inet")
            if conn.status == "LISTEN"
        }),
    )

    def __post_init__(self):
        self.num_conns = len(self.listening) + len(self.established)


@dataclass
class Interface:
    interface: str = field(default="wlan0")
    hosts: list[str] = field(default_factory=list[str])
    online: bool = field(default_factory=bool, init=False)
    ip: str = field(default="", init=False)
    mac: str = field(default="", init=False)
    num_conns: int = field(default_factory=int, init=False)
    latency: float = field(default_factory=float, init=False)
    type = "Net"

    def __post_init__(self):
        self.online = self.status()
        self.ip, self.mac = self.addresses()[:2]
        self.num_conns = self.connections().num_conns
        self.latency = self.ping()

    def addresses(self) -> tuple[str, str, str, str]:
        """Retrieve network information for a specific interface.

        Returns
            Tuple containing the IP address, netmask, broadcast and MAC address of the specified interface.
        """
        netmask = ""
        broadcast = ""
        for interface, values in psutil.net_if_addrs().items():
            if self.interface in interface:
                self.ip = values[0].address
                netmask = values[0].netmask or ""
                broadcast = values[0].broadcast or ""
                for item in values:
                    if item.family == 17:
                        # AF_PACKET is the family of socket addresses from packet sockets (e.g., those returned by socket.SOCK_PACKET)
                        self.mac = item.address
        return (self.ip, self.mac, netmask, broadcast)

    def connections(self) -> Connections:
        """Return interface connections."""
        return Connections()

    def io(self, human_readable=True) -> tuple | None:
        """Return the accumulated IO for the interface.

        Parameters
        -----------
            human_readable (bool): Specify True to return a human readable format
        """
        from size import Size

        if self.interface not in psutil.net_io_counters(pernic=True):
            raise ValueError(f"Interface {self.interface} does not exist.")
        io_counters = psutil.net_io_counters()[:2]
        return io_counters if not human_readable else tuple(map(Size, io_counters))

    def ping(self, destination="1.1.1.1") -> float:
        """Ping a destination and return the time taken."""
        ping = subprocess.getoutput(
            f'ping -c 1 -W 1.5 {destination} | sed -u "s/^.*time=//g; s/ ms//g; s/^PING.*//g; s/^---.*//g; s/^.*packets.*//g; s/^rtt.*//g"',
        ).strip()
        try:
            self.latency = round(float(ping), 2)
        except ValueError:
            self.latency = -1.0
        return self.latency

    def status(self) -> bool:
        """Get current status of the interface."""
        self.online = psutil.net_if_stats().get(self.interface, "wlan0").isup  # type: ignore
        return self.online

    def neighbors(self) -> list[str]:
        """Scan for hosts on the network."""
        self.hosts = subprocess.getoutput(
            r'nmap -T4 -sn 10.0.0.0/24 | grep -oP "\d{2}\.\d\.\d\.\d+"'
        ).splitlines()
        return self.hosts

    def dict(self) -> dict[str, float]:
        return {"ping": self.ping()}


"""
    def port_info(self, verbose_level=0, host='10.0.0.1', entire_subnet=False):
        # Verbose levels:
        # 0 - Show which ports are open
        # 1 - Show which ports are open,their services and versions
        # 2 - Show everything -- WARNING: This can take a while
        nm = nmap.PortScanner()
        print('Scanning...')

        if entire_subnet:
            nm.scan(host, arguments='-sn')
        else:
            nm.scan(host, arguments='-sP')

        if verbose_level == 0:
            nm.scan(host, arguments='-sS')
        elif scan == 'services':
            nm.scan(host, arguments='-sV')
            for host in nm.all_hosts():
                for protocol in nm[host].all_protocols():
                    lport = nm[host][protocol].keys()
                    for port in lport:
                        service = nm[host][protocol][port]['name']
                        version = nm[host][protocol][port]['version']

        return nm
    """
