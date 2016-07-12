from cx_Freeze import setup, Executable

setup(
    name = "VkClear",
    version = "0.1",
    description = "VkClear",
    executables = [Executable("vkclear.py")]
)
