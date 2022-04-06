import secrets
from string import digits, ascii_letters


RANDOM_STRING_POOL = digits + ascii_letters


def generate_random_string(length: int = 32) -> str:
    """
    Generate random string
    :param length: Length of string
    :return: A random string
    """
    return ''.join(secrets.choice(RANDOM_STRING_POOL) for _ in range(length))
