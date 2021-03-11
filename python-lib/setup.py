from setuptools import setup, find_packages

setup(
    name="ds_utils_lib",
    version="0.0.1",
    description="A data science utilities library",
    author="David Stiles Rosselli",
    install_requires=[
        "boto3",
        "fire<1.0.0",
        "python-dotenv"
    ],
    packages=find_packages()
)
