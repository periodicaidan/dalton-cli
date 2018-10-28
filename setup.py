from setuptools import setup, find_packages

setup(
    name="dalton_cli",
    author="Aidan T. Manning",
    author_email="periodicaidan@gmail.com",
    description="The stoichiometric command line tool",
    license="MIT",
    version="0.1.0",
    packages=find_packages(),
    include_package_date=True,
    install_requires=[
        "Click",
        "pyyaml"
    ],
    entry_points="""
        [console_scripts]
        dalton=__init__:main
    """
)
