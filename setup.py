from setuptools import setup, find_packages
import codecs
import os

# Read the contents of the README file
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pass-gen",
    version="1.0.0",
    description="A cryptographically secure password generation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pass-Gen Team",
    author_email="your-email@example.com",
    url="https://github.com/Brivox5/Pass-Gen",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["password", "security", "cryptography", "generator"],
    python_requires=">=3.7",
    package_data={
        "pass_gen": ["py.typed"],
    },
    project_urls={
        "Homepage": "https://github.com/Brivox5/Pass-Gen",
        "Documentation": "https://pass-gen.readthedocs.io/",
        "Repository": "https://github.com/Brivox5/Pass-Gen",
        "Issues": "https://github.com/Brivox5/Pass-Gen/issues",
    },
)