import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modded-pytonapi",
    version="0.0.3",
    author="spencerwilf",
    description="Separate implementation of pytonapi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonkeeper/pytonapi/",
    packages=setuptools.find_packages(exclude=["examples", "tests"]),
    install_requires=[
        "httpx>=0.26.0",
        "websockets>=12.0",
        "pydantic==2.*",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "": ["*py.typed"],
    },
)
