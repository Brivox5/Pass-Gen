# Pass-Gen

A cryptographically secure password generation library for Python that follows OWASP Top 10 and NIST SP 800-63B security guidelines.

## Features

-  **Cryptographically Secure**: Uses `secrets.SystemRandom()` for true randomness
-  **Configurable**: Customizable character sets and password length
-  **Batch Generation**: Generate multiple passwords at once
-  **Memorable Passwords**: Generate human-readable passwords with words
-  **Comprehensive Testing**: >95% test coverage with pytest
-  **Full Documentation**: Complete API documentation with examples
-  **Security Validation**: Automatic entropy checking and pattern prevention

## Installation

```bash
pip install pass-gen
```

## Quick Start

```python
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
```

## Advanced Usage

### Custom Configuration

```python
# Custom configuration
generator = PasswordGenerator(
    length=20,
    include_uppercase=True,
    include_lowercase=True,
    include_digits=True,
    include_special=True,
    custom_chars="!@#$"
)

password = generator.generate()
```

### Memorable Passwords

```python
# Generate memorable password with custom options
memorable = generator.generate_memorable(
    word_count=4,
    separator="-",
    capitalize_words=True,
    add_numbers=True
)
# Example: "Apple23-Banana45-Carrot67-Dolphin89"
```

### Batch Operations

```python
# Generate 10 passwords with same configuration
passwords = generator.generate_batch(10)
for i, pwd in enumerate(passwords, 1):
    print(f"Password {i}: {pwd}")
```

## Security Features

### OWASP Compliance
- Minimum password length: 8 characters
- Support for multiple character sets
- Prevention of common patterns and sequences
- Cryptographically secure random number generation

### NIST SP 800-63B Compliance
- Minimum entropy of 64 bits
- No arbitrary complexity requirements
- Support for all printable ASCII characters
- No password composition rules

### Entropy Calculation

The library automatically calculates and validates password entropy:
- **64+ bits**: Recommended for most use cases
- **80+ bits**: High security applications
- **100+ bits**: Maximum security requirements

## API Reference

### PasswordGenerator Class

#### `__init__`
```python
PasswordGenerator(
    length=16,
    include_uppercase=True,
    include_lowercase=True,
    include_digits=True,
    include_special=True,
    custom_chars=None
)
```

#### Methods

- **`generate()`** → `str`: Generate a single password
- **`generate_batch(count)`** → `List[str]`: Generate multiple passwords
- **`generate_memorable()`** → `str`: Generate a memorable password
- **`get_configuration()`** → `dict`: Get current configuration

## Examples

### Basic Usage
```python
from pass_gen import PasswordGenerator

# Simple password generation
pwd = PasswordGenerator().generate()
print(pwd)  # e.g., "xK8!pL2@qR9#sT4%"
```

### Custom Character Sets
```python
# Only letters and numbers
generator = PasswordGenerator(
    include_special=False,
    custom_chars=""
)
```

### High Security
```python
# 24-character password with all character sets
generator = PasswordGenerator(length=24)
password = generator.generate()
```

## Testing

Run the test suite:

```bash
pip install -e .
pip install pytest pytest-cov
pytest --cov=pass_gen --cov-report=html tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Security Issues

If you discover a security vulnerability, please report it responsibly:
- Email: brivox5@protonmail.com
- Do not disclose vulnerabilities publicly

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OWASP Foundation for security guidelines
- NIST for password security recommendations
- Python `secrets` module team for cryptographic security

## Support

For questions and support:
- GitHub Issues: [Report bugs](https://github.com/brivox5/pass-gen/issues)
- Documentation: [Read the docs](https://pass-gen.readthedocs.io/)
- Email: brivox5@protonmail.com
