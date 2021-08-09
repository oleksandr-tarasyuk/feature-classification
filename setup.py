import sys
import toml
from setuptools import setup
import logging

version = sys.argv[1]
del sys.argv[1]


def get_requirements(get_dev=False) -> list:
    """
    Read pipfile packages and return list of packages with specific version if specified in pipfile.
    :param get_dev: boolean to get development extra packages. Default to false
    :return: List of packages like [package==1.0.0, package2]
    """
    try:
        with open("Pipfile", "r") as f:
            pipfile = f.read()

        pipfile_toml = toml.loads(pipfile)
        if get_dev:
            required_packages = pipfile_toml['dev-packages'].items()
        else:
            required_packages = pipfile_toml['packages'].items()

    except FileNotFoundError as e:
        logging.error(f"Pipfile not found {e}")
        return []

    except KeyError as ke:
        logging.error(f"Could not load packages from pipfile {ke}")
        return []

    return [f"{package}{version}" if version != "*" else package for package, version in required_packages]


setup(
    version=version,
    install_requires=get_requirements(),
    extras_require={
        "dev": get_requirements(get_dev=True)
    }
)
