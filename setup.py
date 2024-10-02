from setuptools import setup, find_packages

setup(
    name="csu2controller",
    version="0.1.1",
    author="Antoine BLASIAK",
    author_email="antoineblasiak66@gmail.com",
    description="A Python library to control the CSU2 device.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abpydev/CSU2Controller",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
    ],
)
