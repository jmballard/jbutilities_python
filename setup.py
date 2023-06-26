from setuptools import setup, find_packages
import re

# we get the description from the README file
with open("README.md", "r") as f:
    description = f.read()

# We get the version from the _version.py file, using the below
# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
VERSION_FILE = "_version.py"
version_file_str = open(VERSION_FILE, "r").read()
VERSION_STR_RE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.research(VERSION_STR_RE, version_file_str, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSION_FILE,))


# We reas the requirements file
def list_requirements(fname="requirements.txt"):
    with open(fname) as fd:
        return fd.read().splitlines()


# We setup the package
setup(
    name="pyjbutilities",
    version=version,
    author="Julie Ballard",
    author_email="bronnimannj@gmail.com",
    url="https://github.com/bronnimannj/jbutilities_python",
    description="My useful Python functions",
    long_description=description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=list_requirements(),
)
