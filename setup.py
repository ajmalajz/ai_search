
from setuptools import setup, find_packages

setup(
    name='ai_search',
    version='1.0.0',
    description='AI-like Arabic & English search for ERPNext using Meilisearch',
    author='Your Company',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests'],
)
