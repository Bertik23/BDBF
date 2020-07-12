import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bdbf", # Replace with your own username
    version="0.1.1.3",
    author="Bertik23",
    author_email="bertikxxiii@gmail.com",
    description="My discord bot framework",
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