"""
Main password generation module for Pass-Gen library.

This module provides the PasswordGenerator class for creating
cryptographically secure passwords with configurable parameters.
"""

import secrets
import string
from typing import List, Optional, Set


class PasswordGenerator:
    """
    A cryptographically secure password generator.
    
    This class generates passwords using secrets.SystemRandom() for
    cryptographic security and follows OWASP Top 10 and NIST SP 800-63B
    guidelines for password security.
    
    Attributes:
        DEFAULT_LENGTH (int): Default password length (16 characters)
        MIN_LENGTH (int): Minimum allowed password length (8 characters)
        MAX_LENGTH (int): Maximum allowed password length (256 characters)
    """
    
    DEFAULT_LENGTH: int = 16
    MIN_LENGTH: int = 8
    MAX_LENGTH: int = 256
    
    # Character sets
    LOWERCASE: str = string.ascii_lowercase
    UPPERCASE: str = string.ascii_uppercase
    DIGITS: str = string.digits
    SPECIAL: str = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def __init__(
        self,
        length: int = DEFAULT_LENGTH,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_special: bool = True,
        custom_chars: Optional[str] = None
    ) -> None:
        """
        Initialize the password generator with configuration.
        
        Args:
            length: Password length (8-256 characters)
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_special: Include special characters
            custom_chars: Custom character set to use (optional)
            
        Raises:
            ValueError: If invalid parameters are provided
        """
        self._validate_length(length)
        
        self.length = length
        self.include_uppercase = include_uppercase
        self.include_lowercase = include_lowercase
        self.include_digits = include_digits
        self.include_special = include_special
        self.custom_chars = custom_chars
        
        self._random = secrets.SystemRandom()
    
    def _validate_length(self, length: int) -> None:
        """Validate password length meets security requirements."""
        if not self.MIN_LENGTH <= length <= self.MAX_LENGTH:
            raise ValueError(
                f"Password length must be between {self.MIN_LENGTH} "
                f"and {self.MAX_LENGTH} characters"
            )
    
    def _get_character_set(self) -> str:
        """
        Get the combined character set based on configuration.
        
        Returns:
            Combined character set string
            
        Raises:
            ValueError: If no character sets are selected
        """
        char_sets = []
        
        if self.include_lowercase:
            char_sets.append(self.LOWERCASE)
        if self.include_uppercase:
            char_sets.append(self.UPPERCASE)
        if self.include_digits:
            char_sets.append(self.DIGITS)
        if self.include_special:
            char_sets.append(self.SPECIAL)
        if self.custom_chars:
            char_sets.append(self.custom_chars)
        
        if not char_sets:
            raise ValueError("At least one character set must be selected")
        
        return ''.join(char_sets)
    
    def _has_required_chars(self, password: str, char_set: str) -> bool:
        """Check if password contains at least one character from each required set."""
        required_sets = []
        
        if self.include_lowercase:
            required_sets.append(set(self.LOWERCASE))
        if self.include_uppercase:
            required_sets.append(set(self.UPPERCASE))
        if self.include_digits:
            required_sets.append(set(self.DIGITS))
        if self.include_special:
            required_sets.append(set(self.SPECIAL))
        
        password_chars = set(password)
        
        for req_set in required_sets:
            if not req_set.intersection(password_chars):
                return False
        
        return True
    
    def _calculate_entropy(self, char_set_size: int) -> float:
        """Calculate password entropy in bits."""
        import math
        return self.length * math.log2(char_set_size)
    
    def generate(self) -> str:
        """
        Generate a single cryptographically secure password.
        
        Returns:
            Generated password string
            
        Raises:
            ValueError: If generated password doesn't meet requirements
        """
        char_set = self._get_character_set()
        
        # Ensure minimum entropy of 64 bits
        entropy = self._calculate_entropy(len(char_set))
        if entropy < 64:
            raise ValueError(
                f"Configuration provides only {entropy:.1f} bits of entropy. "
                f"Minimum required is 64 bits. Consider increasing length or "
                f"using more character sets."
            )
        
        # Generate password with required character types
        max_attempts = 100
        for attempt in range(max_attempts):
            password = ''.join(self._random.choice(char_set) for _ in range(self.length))
            
            # Check if password meets all requirements
            if self._has_required_chars(password, char_set):
                return password
        
        raise ValueError(
            "Failed to generate password meeting all requirements after "
            f"{max_attempts} attempts. Try relaxing some constraints."
        )
    
    def generate_batch(self, count: int) -> List[str]:
        """
        Generate multiple passwords with the same configuration.
        
        Args:
            count: Number of passwords to generate
            
        Returns:
            List of generated passwords
            
        Raises:
            ValueError: If count is not positive
        """
        if count <= 0:
            raise ValueError("Count must be a positive integer")
        
        return [self.generate() for _ in range(count)]
    
    def generate_memorable(
        self,
        word_count: int = 4,
        separator: str = "-",
        capitalize_words: bool = True,
        add_numbers: bool = True
    ) -> str:
        """
        Generate a memorable password using words.
        
        Args:
            word_count: Number of words to use (3-6 recommended)
            separator: Character to separate words
            capitalize_words: Capitalize each word
            add_numbers: Add random numbers between words
            
        Returns:
            Memorable password string
        """
        # Common word list for memorable passwords
        words = [
            "apple", "banana", "carrot", "dolphin", "elephant", "flamingo",
            "giraffe", "honey", "iguana", "jaguar", "koala", "lemon", "mango",
            "night", "orange", "panda", "quail", "rabbit", "sunset", "tiger",
            "umbrella", "violet", "water", "xray", "yellow", "zebra"
        ]
        
        selected_words = self._random.sample(words, word_count)
        
        if capitalize_words:
            selected_words = [word.capitalize() for word in selected_words]
        
        if add_numbers:
            # Add random numbers between words
            result = []
            for i, word in enumerate(selected_words):
                result.append(word)
                if i < len(selected_words) - 1:
                    result.append(str(self._random.randint(0, 99)))
        else:
            result = selected_words
        
        return separator.join(result)
    
    def get_configuration(self) -> dict:
        """
        Get current generator configuration.
        
        Returns:
            Dictionary with current configuration
        """
        return {
            "length": self.length,
            "include_uppercase": self.include_uppercase,
            "include_lowercase": self.include_lowercase,
            "include_digits": self.include_digits,
            "include_special": self.include_special,
            "custom_chars": self.custom_chars
        }