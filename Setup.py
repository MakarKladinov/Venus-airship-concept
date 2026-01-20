"""
Setup файл для установки пакета
"""
from setuptools import setup, find_packages
import os

# Чтение README.md для длинного описания
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Simulation of Venus atmospheric entry with aerodynamics, thermal loads and parachute systems"

# Чтение requirements.txt
requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
else:
    # Базовые зависимости
    requirements = [
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "scipy>=1.7.0",
    ]

setup(
    name="venus_atmospheric_simulation",
    version="1.0.0",
    author="Venus Simulation Team",
    author_email="example@example.com",
    description="Simulation of Venus atmospheric entry with aerodynamics, thermal loads and parachute systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/venus_atmospheric_simulation",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "venus-sim=venus_atmospheric_simulation.main:main",
        ],
    },
    include_package_data=True,
    keywords="venus atmosphere simulation aerospace physics",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/venus_atmospheric_simulation/issues",
        "Source": "https://github.com/yourusername/venus_atmospheric_simulation",
    },
)