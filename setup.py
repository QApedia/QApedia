from setuptools import setup, find_packages
from os import path

# The directory containing this file
this_directory = path.abspath(path.dirname(__file__))

# The text of the README file
with open(path.join(this_directory, "README.md"), encoding="utf-8") as fid:
    README = fid.read()

with open(path.join(this_directory, "LICENSE")) as f:
    license = f.read()

setup(
    name="QA-pedia",
    version="v0.0.0-alpha",
    description="Geração de pares questão-sparql",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/QApedia/QApedia",
    author="Ivan Pereira, Jessica Sousa",
    author_email="navi1921@gmail.com, jessicasousa.pc@gmail.com",
    license="MIT",
    classifiers=[
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["SPARQLWrapper", "pandas", "lxml"],
    tests_require=["pytest"],
    entry_points={"console_scripts": ["qapedia=QApedia.qapedia:_run"]},
    package_data={"QApedia": ["data/*"]},
    zip_safe=False,
)
