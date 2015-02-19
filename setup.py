from setuptools import setup, find_packages
import sys
import re

def find_version(path):
    with open(path, "r") as f:
        match = re.search(r'^__version__ = "([^"]+)"', f.read(), re.M)
    if match is None:
        raise Exception("Could not find __version__")
    return match.group(1)

version = find_version("ditail.py")
url = "https://github.com/ASzc/ditail"
long_description = "For more information see the `README <{url}/blob/{version}/README.md>`_".format(**locals())

install_requires = ["pyinotify>=0.9.5"]
if sys.version_info < (3,4,2):
    install_requires.append("asyncio>=3.4.2")

setup(
    name="ditail",
    version=version,
    description="Tail for directories",
    long_description=long_description,
    url=url,

    author="Alex Szczuczko",
    author_email="alex@szc.ca",

    license="GPLv3+",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    keywords="tail directory recursive inotify",

    py_modules=["ditail"],
    scripts=["scripts/ditail"],

    install_requires=install_requires,
)
