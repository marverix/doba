import os

"""
Is running inside docker?
"""
IS_INSIDE_DOCKER = os.getenv("INSIDE_DOCKER", "0") == "1"
