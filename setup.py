import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flightplan",
    version="1.0.0",
    author="Craig Opie",
    author_email="craigopie@gmail.com",
    description="A flight plan update program.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CraigOpie/flightplan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
