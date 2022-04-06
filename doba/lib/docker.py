from typing import List, Union

import json
from httpunixsocketconnection import HTTPUnixSocketConnection
from doba.structures import Container, Image, Port, Volume


_conn = HTTPUnixSocketConnection("/var/run/docker.sock")


def _get_json(url: str) -> Union[dict, List[dict]]:
    """
    Get JSON response from URL
    :return:
    """
    _conn.request("GET", url)
    res = _conn.getresponse()

    if res.status != 200:
        raise Exception("Error receiving data from docker.sock")

    content = res.read().decode("utf-8")
    return json.loads(content)


def fetch_containers() -> List[dict]:
    """
    Get list of Docker Containers
    :return:
    """
    return _get_json("/containers/json")


def inspect_container(container_id: str):
    """
    Inspect given Docker Container
    :return:
    """
    return _get_json(f"/containers/{container_id}/json")


def get_containers() -> List[Container]:
    """
    Get containers that have label doba.enable=="true"
    :return: List of dictionaries
    """
    containers = fetch_containers()
    doba_containers = []
    for container in containers:
        if "doba.enable" in container["Labels"]:
            labels = container["Labels"]
            if labels["doba.enable"].lower() == "true":
                container_detailed = inspect_container(container["Id"])
                doba_containers.append(factory_container(container_detailed))
    return doba_containers


def factory_port(port_str: str) -> Port:
    port, protocol = port_str.split("/")
    return Port(int(port), protocol, port)


def factory_container(container) -> Container:
    """
    Create a simplified container dictionary object
    :param container: Detailed container information (dict)
    :return:
    """
    name: str = container["Name"][1:]
    mounts: List[dict] = container["Mounts"]
    config: dict = container["Config"]
    image = Image(*config["Image"].split(":"))
    env = {k: v for (k, v) in [i.split("=") for i in config["Env"]]}
    labels: dict = config["Labels"]
    volumes = []
    networks: dict = container["NetworkSettings"]["Networks"]
    ip_address: str = networks[list(networks.keys())[0]]["IPAddress"]
    ports = list(map(factory_port, config["ExposedPorts"].keys()))
    for mount in mounts:
        if mount["RW"]:
            volumes.append(
                Volume(mount["Source"], mount["Destination"])
            )
    return Container(name, image, env, ip_address, ports, volumes, labels["doba.handler"])
