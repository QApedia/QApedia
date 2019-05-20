import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / "LICENSE").read_text()
    
setup(name="qapedia",
      version="0.1.0",
      description="",
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://github.com/JessicaSousa/qapedia",
      author="Jessica Sousa",
      author_email="jessicasousa.pc@gmail.com",
      license=LICENSE,
      packages=find_packages(),
      install_requires = ["SPARQLWrapper"],
      tests_require = ['pytest'],
      zip_safe=False)