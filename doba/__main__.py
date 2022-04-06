from typing import List, Set

from doba.lib.docker import get_containers
from doba.structures import Container
from doba.data_handlers import get_data_handler_class


def get_required_handlers(containers: List[Container]) -> Set[str]:
    """
    Get set of required handlers
    :param containers: List of doba-enabled containers
    :return:
    """
    handlers = set()
    for container in containers:
        handlers.add(container.doba.handler)
    return handlers


def preflight_data_handlers(handlers: Set[str]):
    """
    Preflight given set of data handlers names
    :param handlers:
    :return:
    """
    for handler_name in handlers:
        data_handler_class = get_data_handler_class(handler_name)
        data_handler_class.preflight()


def backup(container: Container):
    data_handler_class = get_data_handler_class(container.doba.handler)
    data_handler = data_handler_class(container)
    data_handler.before_backup()
    data_handler.backup()
    data_handler.after_backup()


def run():
    """
    Run doba
    :return:
    """
    containers = get_containers()
    required_handlers = get_required_handlers(containers)
    preflight_data_handlers(required_handlers)

    for container in containers:
        backup(container)


if __name__ == "__main__":
    run()
