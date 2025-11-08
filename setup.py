from setuptools import setup, find_packages
import codecs
import os

# Read the contents of the README file
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="pass-gen",
    version="1.0.0",
    author="Pass-Gen Team",
    author_email="your-email@example.com",
    description="A cryptographically secure password generation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=["password", "security", "cryptography", "generator", "owasp", "nist"],
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
    python_requires=">=3.7",
    project_urls={
        "Source Code": "https://github.com/your-username/pass-gen",
        "Bug Tracker": "https://github.com/your-username/pass-gen/issues",
        "Documentation": "https://pass-gen.readthedocs.io/",
    },
)