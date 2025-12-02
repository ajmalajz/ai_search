from setuptools import setup, find_packages

setup(
    name='ai_search',
    version='0.0.1',
    description='Custom search engine override for ERPNext link search',
    author='Your Name',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['frappe','fuzzywuzzy','sqlite-utils'],
)