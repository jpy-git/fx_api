from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests>=2", "pandas>=1.2"]

setup(
    name="fx_api",
    version="0.0.1",
    author="Joseph Young",
    author_email="josephyoung.jpy@gmail.com",
    description="A Python API interface for querying exchange rates from exchangeratesapi.io",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jpy-git/fx_api",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)