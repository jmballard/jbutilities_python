from setuptools import setup, find_packages

setup(
    name='pyjbutilities',
    version='0.1', 
    author = "Julie Ballard",
    author_email= "bronnimannj@gmail.com",
    url = "https://github.com/bronnimannj/jbutilities_python",
    description = "My useful Python functions",
    package_dir={"": "src"},
    packages=find_packages(where = 'src'))