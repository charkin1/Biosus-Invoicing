from setuptools import setup, find_packages

setup(
    name="biosus_invoicing",
    version="0.0.1",
    packages=find_packages(),   # ensures both outer + inner are included
    include_package_data=True,
)