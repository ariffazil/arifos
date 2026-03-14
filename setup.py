"""
Setup.py for backward compatibility with pip wheel
pyproject.toml is the authoritative source
"""

from setuptools import setup

setup(
    name="arifosmcp",
    version="2026.3.14",
    description="arifOS v2026.03.14-VALIDATED — Constitutional AI Governance",
    author="Muhammad Arif bin Fazil",
    author_email="arifbfazil@gmail.com",
    url="https://arifos.arif-fazil.com",
    packages=["arifosmcp", "core", "scripts"],
    python_requires=">=3.12",
)

