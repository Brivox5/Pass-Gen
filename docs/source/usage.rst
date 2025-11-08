Usage Guide
============

This guide demonstrates how to use the Pass-Gen library for secure password generation.

Basic Usage
-----------

Import and create a PasswordGenerator instance:

.. code-block:: python

   from pass_gen import PasswordGenerator
   
   # Create a generator with default settings
   generator = PasswordGenerator()
   
   # Generate a single password
   password = generator.generate()
   print(f"Generated password: {password}")

Custom Configuration
--------------------

Configure the password generator with custom parameters:

.. code-block:: python

   # Custom configuration
   generator = PasswordGenerator(
       length=20,
       include_uppercase=True,
       include_lowercase=True,
       include_digits=True,
       include_special=True,
       custom_chars=None  # Optional custom character set
   )

Batch Generation
----------------

Generate multiple passwords at once:

.. code-block:: python

   # Generate 5 passwords
   passwords = generator.generate_batch(5)
   
   for i, password in enumerate(passwords, 1):
       print(f"Password {i}: {password}")

Memorable Passwords
-------------------

Generate memorable passwords using word-based patterns:

.. code-block:: python

   # Generate a memorable password
   memorable_password = generator.generate_memorable()
   print(f"Memorable password: {memorable_password}")
   
   # Custom memorable password options
   memorable_password = generator.generate_memorable(
       word_count=4,
       separator="-",
       capitalize=True,
       add_numbers=True
   )

Configuration Methods
---------------------

You can also configure the generator after creation:

.. code-block:: python

   generator = PasswordGenerator()
   
   # Configure individual settings
   generator.configure(
       length=24,
       include_special=False
   )
   
   # Or set individual properties
   generator.length = 32
   generator.include_digits = False

Security Validation
------------------

The library automatically validates security requirements:

.. code-block:: python

   # This will raise ValueError due to insufficient entropy
   try:
       weak_generator = PasswordGenerator(
           length=8,
           include_uppercase=False,
           include_lowercase=False,
           include_digits=False,
           include_special=False,
           custom_chars="ab"
       )
       password = weak_generator.generate()
   except ValueError as e:
       print(f"Security validation failed: {e}")

Advanced Examples
-----------------

Generate passwords for specific requirements:

.. code-block:: python

   # Numeric-only passwords (e.g., for PIN codes)
   numeric_generator = PasswordGenerator(
       include_uppercase=False,
       include_lowercase=False,
       include_special=False,
       custom_chars="0123456789"
   )
   
   # Alphanumeric passwords
   alphanumeric_generator = PasswordGenerator(
       include_special=False
   )
   
   # Special character-heavy passwords
   special_generator = PasswordGenerator(
       include_uppercase=True,
       include_lowercase=True,
       include_digits=True,
       custom_chars="!@#$%^&*()_+-=[]{}|;:,.<>?"
   )

Integration with Applications
----------------------------

Integrate Pass-Gen into your applications:

.. code-block:: python

   from pass_gen import PasswordGenerator
   
   class UserRegistration:
       def __init__(self):
           self.password_generator = PasswordGenerator(length=16)
       
       def create_user(self, username):
           temporary_password = self.password_generator.generate()
           # Store user with temporary password
           return temporary_password

Best Practices
--------------

- Always use the default settings for maximum security
- Consider increasing length for sensitive applications
- Use batch generation for creating multiple user accounts
- Validate generated passwords meet your specific requirements
- Store passwords securely using proper encryption