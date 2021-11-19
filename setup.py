from bdbf import __version__
import setuptools

import os
import sys
sys.path.insert(0, os.path.abspath('../bdbf'))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bdbf",  # Replace with your own username
    version=__version__,
    author="Bertik23",
    author_email="bertikxxiii@gmail.com",
    description="Bertik23's discord bot framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bertik23/bdbf",
    packages=["bdbf"],  # setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["discord.py>=1.7.3", "discord-py-slash-command==3.0.1"],
    keywords="discord, bot, framework"
)
