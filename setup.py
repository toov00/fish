from setuptools import setup

setup(
    name="fish",
    version="1.0.0",
    description="Terminal wait animation (fish) while a command runs",
    packages=["fish", "teakettle"],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "fish=fish.cli:main",
        ],
    },
)
