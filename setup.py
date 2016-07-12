"""
Distutils script for cx_Freeze.
"""

from cx_Freeze import setup, Executable


setup(name = "VkClear",
        description = "Automatic cleaning of the VK account",
        version = "0.1",
        maintainer="Dmytro Kazanzy",
        maintainer_email="dkazanzhy@gmail.com",
        executables = [Executable("vkclear.py")])

