import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bdbf", # Replace with your own username
    version="0.2.1",
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
)