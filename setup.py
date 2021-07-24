import setuptools

setuptools.setup(
    name="Pupper Hardware Interface",
    version="0.1",
    author="Nathan Kau",
    author_email="nathankau@gmail.com",
    description="Library for controlling M2006-based & C610-based Pupper",
    packages=["pupper_hardware_interface"],
    install_requires=[
        "msgpack",
        "pyserial",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
