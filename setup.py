# setup.py
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name='ai_search',
    version='0.0.1',
    description='Custom app for fuzzy search functionality in ERPNext.',
    author='Your Name',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
