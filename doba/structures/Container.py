from typing import List

from .DobaContainersConfig import DobaContainersConfig
from .Image import Image
from .Port import Port
from .Volume import Volume


class Container:

    def __init__(self, name: str, image: Image, env: dict, ip_address: str, ports: List[Port], volumes: List[Volume],
                 doba_handler: str):
        self.name = name
        self.image = image
        self.env = env
        self.ip_address = ip_address
        self.ports = ports
        self.volumes = volumes
        self.doba = DobaContainersConfig(doba_handler)
