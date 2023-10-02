from setuptools import setup, find_packages
import os
import ast

name = "cvtool"


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def parse_requirements(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        requirements = [line for line in lines if line and not line.startswith("#")]
        return requirements
    


def get_variable_value(file_path, variable_name):
    with open(file_path, 'r') as file:
        # Read the Python code from the file
        python_code = file.read()

    # Parse the Python code into an abstract syntax tree (AST)
    parsed_code = ast.parse(python_code)

    # Iterate through the AST nodes to find the assignment statement for the variable
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == variable_name:
                    # If the variable is found, return its value
                    return ast.literal_eval(node.value)

    # If the variable is not found, return None or raise an error, depending on your use case
    return None


contributor_emails = os.popen("git log --format='%ae' | sort -u").read()
contributor_names = os.popen("git log --format='%aN' | sort -u").read()from cmor import CMOR_VERSION_PATCH as m

requirements = parse_requirements("auxillary/requirements.txt")

setup(
    name=name,
    version=get_variable_value(f'./{name}/__init__.py','version'),
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

