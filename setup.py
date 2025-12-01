from setuptools import setup, find_packages

setup(
    name='ai_search',
    version='0.0.1',
    description='Custom search engine for ERPNext using SQLite',
    author='Your Name',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['frappe', 'sqlite-utils', 'fuzzywuzzy'],
)