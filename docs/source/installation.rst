Installation
============

Installing Pass-Gen is straightforward using pip.

From PyPI
---------

Once published, you can install the latest stable version from PyPI:

.. code-block:: bash

   pip install pass-gen

From Source
-----------

To install from the source code:

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/your-username/pass-gen.git
      cd pass-gen

2. Install in development mode:

   .. code-block:: bash

      pip install -e .

   This installs the package in editable mode, allowing you to make changes to the source code.

Development Dependencies
------------------------

For development, install with all development dependencies:

.. code-block:: bash

   pip install -e .[dev]

This includes:
- pytest for testing
- pytest-cov for coverage reporting
- Sphinx for documentation
- Pre-commit hooks for code quality

Verification
------------

After installation, verify that the package works correctly:

.. code-block:: python

   import pass_gen
   print(pass_gen.__version__)
   
   # Create a password generator instance
   generator = pass_gen.PasswordGenerator()
   password = generator.generate()
   print(f"Generated password: {password}")

Requirements
------------

- Python 3.7 or higher
- No external dependencies (uses Python's built-in `secrets` module)