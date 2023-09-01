from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def parse_requirements(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        requirements = [line for line in lines if line and not line.startswith("#")]
        return requirements
    
contributor_emails = os.popen("git log --format='%ae' | sort -u").read()
contributor_names = os.popen("git log --format='%aN' | sort -u").read()

requirements = parse_requirements("auxillary/requirements.txt")

setup(
    name="cvtool",
    version="0.0.3",
    author="CMIP-IPO+WIP. Contributors: "+contributor_names.replace('\n',';'),
    author_email="daniel.ellis@ext.esa.int",
    description="A tool for computer vision tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cmip-ipo-internal/CVTool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License** change",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)

