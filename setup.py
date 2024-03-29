import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()
try:
    CHANGES = open(os.path.join(here, "CHANGES.md")).read()
except:
    CHANGES = ""

requires = [
    "black",
    "boto",
    "boto3",
    "pytest-cov",
]

setup(
    name="glacierputter",
    version="0.0",
    description="glacierputter",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
    ],
    author="",
    author_email="",
    url="",
    keywords="backups ec2 ebs",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="glacierputter",
    install_requires=requires,
)
