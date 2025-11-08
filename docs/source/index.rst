Pass-Gen Documentation
======================

Pass-Gen is a cryptographically secure password generation library for Python that follows OWASP Top 10 and NIST SP 800-63B security guidelines.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   security
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Features
--------

- **Cryptographically Secure**: Uses ``secrets.SystemRandom()`` for true randomness
- **Configurable**: Customizable character sets and password length
- **Batch Generation**: Generate multiple passwords at once
- **Memorable Passwords**: Generate human-readable passwords with words
- **Comprehensive Testing**: >95% test coverage with pytest
- **Security Validation**: Automatic entropy checking and pattern prevention

Quick Start
-----------

.. code-block:: python

   from pass_gen import PasswordGenerator

   # Create a generator with default settings
   generator = PasswordGenerator()

   # Generate a single secure password
   password = generator.generate()
   print(f"Generated password: {password}")

   # Generate multiple passwords
   passwords = generator.generate_batch(5)
   print(f"Batch passwords: {passwords}")

   # Generate a memorable password
   memorable = generator.generate_memorable()
   print(f"Memorable password: {memorable}")

Installation
------------

.. code-block:: bash

   pip install pass-gen

Requirements
^^^^^^^^^^^^

- Python 3.7+
- No external dependencies

Security Features
-----------------

- **OWASP Compliance**: Minimum password length, multiple character sets
- **NIST SP 800-63B Compliance**: 64+ bits entropy, no arbitrary complexity rules
- **Entropy Validation**: Automatic calculation and validation
- **Pattern Prevention**: Prevention of common patterns and sequences

API Reference
-------------

Comprehensive API documentation is available in the :doc:`api` section.

.. toctree::
   :hidden:

   installation
   usage
   api
   security
   contributing

License
-------

This project is licensed under the MIT License.