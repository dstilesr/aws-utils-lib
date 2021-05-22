from setuptools import setup, find_packages

setup(
    name="aws_utils_lib",
    version="0.0.3",
    description="A utilities library to interact with aws",
    author="David Stiles Rosselli",
    install_requires=[
        "boto3",
        "fire<1.0.0",
        "python-dotenv",
        "tensorflow>=2.0.0",
        "numpy>1.0.0"
    ],
    packages=find_packages()
)
