import importlib
from typing import Type

from .AbstractDataHandler import AbstractDataHandler

_cache = {}


def get_data_handler_class(name: str) -> Type[AbstractDataHandler]:
    """
    Import Data Handler with given name
    :param name: Data Handler name
    :return:
    """
    package_path = f"doba.data_handlers.{name}"

    if package_path in _cache:
        data_handler = _cache[package_path]

    else:
        try:
            module = importlib.import_module(package_path)
            class_name = name.capitalize() + "Handler"
            data_handler = getattr(module, class_name)
        except Exception:
            raise ImportError(f"Error importing '{package_path}'")

        _cache[package_path] = data_handler

    return data_handler
