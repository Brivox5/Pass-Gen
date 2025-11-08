"""
Test suite for Pass-Gen password generation library.

This module contains comprehensive tests for the PasswordGenerator class,
ensuring cryptographic security, parameter validation, and functionality.
"""

import pytest
import string
from pass_gen import PasswordGenerator


class TestPasswordGenerator:
    """Test class for PasswordGenerator functionality."""
    
    def test_default_initialization(self):
        """Test that generator initializes with default parameters."""
        generator = PasswordGenerator()
        config = generator.get_configuration()
        
        assert config["length"] == 16
        assert config["include_uppercase"] is True
        assert config["include_lowercase"] is True
        assert config["include_digits"] is True
        assert config["include_special"] is True
        assert config["custom_chars"] is None
    
    def test_custom_initialization(self):
        """Test generator with custom parameters."""
        generator = PasswordGenerator(
            length=20,
            include_uppercase=False,
            include_lowercase=False,
            include_digits=True,
            include_special=False,
            custom_chars="!@#"
        )
        config = generator.get_configuration()
        
        assert config["length"] == 20
        assert config["include_uppercase"] is False
        assert config["include_lowercase"] is False
        assert config["include_digits"] is True
        assert config["include_special"] is False
        assert config["custom_chars"] == "!@#"
    
    def test_length_validation(self):
        """Test password length validation."""
        # Test minimum length
        with pytest.raises(ValueError, match="must be between"):
            PasswordGenerator(length=7)
        
        # Test maximum length
        with pytest.raises(ValueError, match="must be between"):
            PasswordGenerator(length=257)
        
        # Test valid lengths
        for length in [8, 16, 256]:
            generator = PasswordGenerator(length=length)
            assert generator.length == length
    
    def test_character_set_validation(self):
        """Test character set validation."""
        # Test no character sets selected
        with pytest.raises(ValueError, match="At least one character set"):
            generator = PasswordGenerator(
                include_uppercase=False,
                include_lowercase=False,
                include_digits=False,
                include_special=False
            )
            generator.generate()
    
    def test_password_generation(self):
        """Test basic password generation."""
        generator = PasswordGenerator()
        password = generator.generate()
        
        assert isinstance(password, str)
        assert len(password) == 16
        
        # Check that password contains expected character types
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_digit = any(c in string.digits for c in password)
        has_special = any(c in PasswordGenerator.SPECIAL for c in password)
        
        assert has_upper
        assert has_lower
        assert has_digit
        assert has_special
    
    def test_custom_character_sets(self):
        """Test password generation with custom character sets."""
        generator = PasswordGenerator(
            length=24,  # Increased length for sufficient entropy
            include_uppercase=False,
            include_lowercase=False,
            include_digits=False,
            include_special=False,
            custom_chars="abc1234567890!@#$"  # Larger character set
        )
        
        password = generator.generate()
        
        # Password should only contain custom characters
        assert all(c in "abc1234567890!@#$" for c in password)
        assert len(password) == 24
    
    def test_batch_generation(self):
        """Test batch password generation."""
        generator = PasswordGenerator(length=12)
        passwords = generator.generate_batch(5)
        
        assert isinstance(passwords, list)
        assert len(passwords) == 5
        
        for password in passwords:
            assert isinstance(password, str)
            assert len(password) == 12
        
        # All passwords should be different (high probability)
        assert len(set(passwords)) == 5
    
    def test_batch_validation(self):
        """Test batch generation parameter validation."""
        generator = PasswordGenerator()
        
        with pytest.raises(ValueError, match="positive integer"):
            generator.generate_batch(0)
        
        with pytest.raises(ValueError, match="positive integer"):
            generator.generate_batch(-1)
    
    def test_memorable_password_generation(self):
        """Test memorable password generation."""
        generator = PasswordGenerator()
        memorable = generator.generate_memorable()
        
        assert isinstance(memorable, str)
        assert len(memorable) > 0
        
        # Should contain separators and likely numbers
        assert "-" in memorable
        assert any(c.isdigit() for c in memorable)
    
    def test_memorable_custom_options(self):
        """Test memorable password with custom options."""
        generator = PasswordGenerator()
        
        # Test without numbers
        memorable = generator.generate_memorable(add_numbers=False)
        assert not any(c.isdigit() for c in memorable)
        
        # Test custom separator
        memorable = generator.generate_memorable(separator="_")
        assert "_" in memorable
        
        # Test word count
        memorable = generator.generate_memorable(word_count=3)
        parts = memorable.split("-")
        assert len([p for p in parts if not p.isdigit()]) == 3
    
    def test_entropy_validation(self):
        """Test entropy validation for weak configurations."""
        # This configuration should trigger entropy warning
        generator = PasswordGenerator(
            length=8,
            include_uppercase=False,
            include_lowercase=True,
            include_digits=False,
            include_special=False
        )
        
        with pytest.raises(ValueError, match="entropy"):
            generator.generate()
    
    def test_password_uniqueness(self):
        """Test that generated passwords are unique."""
        generator = PasswordGenerator()
        passwords = set()
        
        # Generate multiple passwords and check for uniqueness
        for _ in range(100):
            password = generator.generate()
            passwords.add(password)
        
        # With 100 generations, we should have very few duplicates by chance
        assert len(passwords) > 95  # Allow for some random collisions
    
    def test_configuration_method(self):
        """Test get_configuration method."""
        generator = PasswordGenerator(
            length=24,
            include_uppercase=False,
            custom_chars="@#$"
        )
        
        config = generator.get_configuration()
        
        assert config["length"] == 24
        assert config["include_uppercase"] is False
        assert config["custom_chars"] == "@#$"
        assert config["include_lowercase"] is True  # Default should remain
    
    def test_character_set_exclusion(self):
        """Test password generation with excluded character sets."""
        # Test without uppercase
        generator = PasswordGenerator(include_uppercase=False)
        password = generator.generate()
        assert not any(c in string.ascii_uppercase for c in password)
        
        # Test without digits
        generator = PasswordGenerator(include_digits=False)
        password = generator.generate()
        assert not any(c in string.digits for c in password)
        
        # Test without special characters
        generator = PasswordGenerator(include_special=False)
        password = generator.generate()
        assert not any(c in PasswordGenerator.SPECIAL for c in password)


def test_module_import():
    """Test that the module can be imported correctly."""
    from pass_gen import PasswordGenerator
    from pass_gen import __version__
    
    assert __version__ == "1.0.0"
    assert callable(PasswordGenerator)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])