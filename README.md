# Pass-Gen 🔐

A cryptographically secure password generation library for Python that follows OWASP Top 10 and NIST SP 800-63B security guidelines.

## 📖 Table of Contents

- [ Features](#-features)
- [ Installation](#-installation)
- [ Quick Start](#-quick-start)
- [ Advanced Usage](#️-advanced-usage)
- [ Security Features](#-security-features)
- [ Benchmarking and Security Analysis](#-benchmarking-and-security-analysis)
- [ Testing](#-testing)
- [ Contributing](#-contributing)
- [ Security Issues](#️-security-issues)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)
- [ Support](#-support)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security](https://img.shields.io/badge/Security-Cryptographic-green)](https://owasp.org/)
[![Tests](https://img.shields.io/badge/Tests-95%25%20coverage-success)](https://pytest.org/)

## ✨ Features

- **Cryptographically Secure**: Uses `secrets.SystemRandom()` for true randomness
- **Configurable**: Customizable character sets and password length
- **Batch Generation**: Generate multiple passwords at once
- **Memorable Passwords**: Generate human-readable passwords using EFF wordlist
- **Comprehensive Testing**: >95% test coverage with pytest
- **Full Documentation**: Complete API documentation with examples
- **Security Validation**: Automatic entropy checking and pattern prevention
- **Benchmarking**: Built-in performance and security comparison tools

## 📦 Installation

### From GitHub
```bash
pip install git+https://github.com/Brivox5/Pass-Gen.git
```

### From Source
```bash
git clone https://github.com/Brivox5/Pass-Gen.git
cd Pass-Gen
pip install -e .
```

### Upgrading
```bash
pip install --upgrade git+https://github.com/Brivox5/Pass-Gen.git
```

## 🚀 Quick Start

```python
from pass_gen import PasswordGenerator

# Create a generator with default settings
generator = PasswordGenerator()

# Generate a single secure password
password = generator.generate()
print(f"Generated password: {password}")
# Example: "xK8!pL2@qR9#sT4%"

# Generate multiple passwords
passwords = generator.generate_batch(5)
print(f"Batch passwords: {passwords}")
# Example: ['aB3$cD5&eF7*gH9@', 'iJ1!kL3#mN5^oP7&', 'qR9@sT1*uV3%wX5#', 'yZ7$bC1^dE3&fG5*', 'hI9@jK1#lM3^nO5%']

# Generate a memorable password
memorable = generator.generate_memorable()
print(f"Memorable password: {memorable}")
# Example: "apple23-banana45-carrot67-dolphin89"
```

## 🛠️ Advanced Usage

### Custom Configuration

```python
# Custom configuration with all options
generator = PasswordGenerator(
    length=20,                    # Password length (default: 16)
    include_uppercase=True,       # Include A-Z (default: True)
    include_lowercase=True,       # Include a-z (default: True)
    include_digits=True,         # Include 0-9 (default: True)
    include_special=True,        # Include special chars (default: True)
    custom_chars="!@#$%^&*"      # Additional custom characters
)

password = generator.generate()
# Example: "K8!pL2@qR9#sT4%vW6^yX7&"
```

### Memorable Passwords

```python
# Generate memorable password with custom options
memorable = generator.generate_memorable(
    word_count=4,           # Number of words (default: 4)
    separator="-",         # Word separator (default: "-")
    capitalize_words=True,  # Capitalize each word (default: False)
    add_numbers=True       # Add random numbers (default: True)
)
# Example: "Apple23-Banana45-Carrot67-Dolphin89"
```

### Batch Operations

```python
# Generate 10 passwords with same configuration
passwords = generator.generate_batch(10)
for i, pwd in enumerate(passwords, 1):
    print(f"Password {i}: {pwd}")
    # Password 1: "xK8!pL2@qR9#sT4%"
    # Password 2: "yL9$mN3^oP5&qR7*"
    # ... etc
```

## 🔒 Security Features

### OWASP Compliance ✅
- **Minimum length**: 8+ characters (configurable)
- **Character diversity**: Multiple character sets supported
- **Pattern prevention**: Blocks common sequences and patterns
- **Cryptographic security**: Uses `secrets.SystemRandom()`
- **No dictionary words**: In random password generation

### NIST SP 800-63B Compliance ✅
- **Entropy-based**: 64+ bits minimum (configurable)
- **No complexity rules**: Follows modern password guidelines
- **All ASCII characters**: Full printable ASCII support
- **Memorable passphrases**: EFF wordlist with 7776 words
- **No arbitrary restrictions**: Focus on actual security

### Entropy Calculation 🔢

The library uses NIST-compliant entropy calculations:

| Security Level | Entropy Bits | Use Case |
|----------------|-------------|----------|
| **🔐 Minimum** | 64+ bits | Basic web accounts |
| **🛡️ Recommended** | 80+ bits | Email, social media |
| **🔒 High Security** | 100+ bits | Banking, crypto wallets |
| **🚀 Maximum Security** | 128+ bits | Government, military |

### EFF Wordlist Security 📊

Memorable passwords use the EFF Large Wordlist with 7,776 words:

| Word Count | Entropy Bits | Security Level |
|-----------|-------------|----------------|
| 3 words | 38.76 bits | Basic |
| 4 words | 51.68 bits | **Recommended** |
| 5 words | 64.60 bits | High Security |
| 6 words | 77.52 bits | Maximum Security |
| 7 words | 90.44 bits | Extreme Security |
| 8 words | 103.36 bits | Ultra Security |

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

## 📊 Benchmarking and Security Analysis

### Comparative Performance Testing (Based on 200 samples per library)

#### Security and Performance Comparison

| Library |  Avg Time |  Avg Entropy |  Min Entropy |  Max Entropy |  Avg Crack Time |
|---------|------------|---------------|---------------|---------------|-------------------|
| **Pass-Gen Memorable** | 2.64 ms | **51.70 bits** | 51.68 bits | 51.72 bits | **1.02 hours** |
| **Pass-Gen** | 0.02 ms | 114.98 bits | 78.66 bits | 157.31 bits | 1.80e+27 years |
| PasswordGenerator | 72.40 ms | 162.67 bits | 117.98 bits | 196.64 bits | 1.03e+38 years |
| Crypto Secure | 0.01 ms | 113.70 bits | 70.30 bits | 157.31 bits | 1.53e+27 years |
| Simple Random | 0.004 ms | 114.67 bits | 70.30 bits | 157.31 bits | 1.66e+27 years |
| Passlib | 0.009 ms | 106.96 bits | 68.41 bits | 142.90 bits | 8.25e+22 years |
| Faker | 1.16 ms | 65.55 bits | 65.55 bits | 65.55 bits | 1.71 years |

#### Performance Comparison Visualization

![Password Benchmark Comparison](password_benchmark.png)

### 🔍 Detailed Analysis

#### 1. **Pass-Gen Memorable** 🧠
- **Entropy**: 51.70 bits (4 words from 7776-word list)
- **Security Level**: Good for most personal accounts
- **Usability**: Excellent - easy to remember and type
- **Use Case**: Email, social media, personal accounts

#### 2. **Standard Pass-Gen** 🔐
- **Entropy**: 114.98 bits (extremely high security)
- **Security Level**: Maximum security
- **Performance**: Fastest cryptographic generation
- **Use Case**: Banking, crypto, government systems

#### 3. **PasswordGenerator** ⚡
- **Entropy**: 162.67 bits (highest in test)
- **Performance**: Very slow due to subprocess execution
- **Use Case**: When absolute maximum entropy is required

#### 4. **Other Cryptographic Methods** 🔒
- Similar security to Pass-Gen but without advanced features
- Good alternatives for basic password generation

### 🎯 Recommendations

| Use Case | Recommended Method | Entropy | Security Level |
|----------|-------------------|---------|----------------|
| **Personal Accounts** | Pass-Gen Memorable | 51.70 bits | ✅ Good |
| **Email & Social Media** | Pass-Gen Memorable | 51.70 bits | ✅ Good |
| **Banking & Financial** | Standard Pass-Gen | 114.98 bits | 🔒 Excellent |
| **Cryptocurrency** | Standard Pass-Gen | 114.98 bits | 🔒 Excellent |
| **Government Systems** | Standard Pass-Gen | 114.98 bits | 🔒 Excellent |
| **Maximum Security** | PasswordGenerator | 162.67 bits | 🚀 Extreme |

### 🔬 Security Methodology

- **Entropy Calculation**: NIST SP 800-63B compliant
- **Crack Time Estimation**: 1000 attempts/second attack scenario
- **Wordlist**: EFF Large Wordlist (7776 words)
- **Memorable Password Formula**: `(Number of words) × log₂(7776)`
- **Random Password Formula**: `(Password length) × log₂(Character pool size)`

### 🧪 Running Benchmarks

To reproduce these benchmarks:

```bash
# Install dependencies
pip install matplotlib numpy passlib passwordgenerator faker

# Run benchmark
python test/benchmark_passwords.py
```

The script generates:
- `password_benchmark.png`: Visual comparison graph
- `benchmark_data.json`: Raw statistical data
- Console output with detailed metrics

### 📈 Real-World Security Assessment

| Password Type | Entropy Bits | Time to Crack (1000 guesses/sec) | Security Assessment |
|---------------|-------------|-----------------------------------|---------------------|
| 4-word Passphrase | 51.70 bits | 1.02 hours | ✅ Good for personal use |
| 16-char Random | 114.98 bits | 1.80e+27 years | 🔒 Excellent security |
| 12-char Simple | 45.60 bits | 2.3e+03 years | ⚠️ Basic security |
| 8-char Common | ~28 bits | ~3 minutes | ❌ Insecure |

> **Note**: Memorable passphrases provide excellent usability with good security, while random passwords provide maximum security for critical applications.

## 📞 Support

For questions, support, and bug reports:

- **🐛 Bug Reports**: [GitHub Issues](https://github.com/Brivox5/pass-gen/issues)
- **📚 Documentation**: [Read the Docs](https://pass-gen.readthedocs.io/)
- **📧 Email**: brivox5@protonmail.com
- **💬 Discussions**: [GitHub Discussions](https://github.com/Brivox5/pass-gen/discussions)

### 🚨 Security Vulnerabilities

If you discover a security vulnerability, please report it responsibly:
- **Email**: brivox5@protonmail.com (encrypted preferred)
- **Do NOT** disclose vulnerabilities publicly
- We follow responsible disclosure practices

### 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### 📊 Changelog

- **V1.0.3**: Fixed entropy calculation for memorable passwords
- **V1.0.2**: Added EFF wordlist data file
- **V1.0.1**: Comprehensive benchmarking implementation
- **V1.0.0**: Initial release with cryptographic security

---

**Pass-Gen** 🔐 - Making password security simple and effective for everyone.