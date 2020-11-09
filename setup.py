import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bdbf", # Replace with your own username
    version="1.0.0",
    author="Bertik23",
    author_email="bertikxxiii@gmail.com",
    description="Bertik23's discord bot framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bertik23/bdbf",
    packages=["bdbf"],#setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["discord.py>=1.4.1"],
    keywords="discord, bot, framework"
)