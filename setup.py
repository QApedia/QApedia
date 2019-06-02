from setuptools import setup, find_packages
from os import path

# The directory containing this file
this_directory = path.abspath(path.dirname(__file__))

# with open(path.join(this_directory, "README.md")) as f:
#     long_description = f.read()

with open(path.join(this_directory, "LICENSE")) as f:
    license = f.read()

setup(name="QApedia",
      version="0.1.0",
      description="",
    #   long_description=long_description,
    #   long_description_content_type="text/markdown",
      url="https://github.com/JessicaSousa/QApedia",
      author="Jessica Sousa",
      author_email="jessicasousa.pc@gmail.com",
      license=license,
      packages=find_packages(),
      install_requires=["SPARQLWrapper", "pandas"],
      tests_require=["pytest"],
      zip_safe=False)
