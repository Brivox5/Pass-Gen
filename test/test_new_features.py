#!/usr/bin/env python3
"""
Test script for new password generator features:
- Character exclusion
- Pronounceable passwords
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pass_gen.pass_gen import PasswordGenerator

def test_character_exclusion():
    """Test character exclusion functionality."""
    print("Testing character exclusion...")
    
    # Test excluding specific characters
    gen = PasswordGenerator(length=12, exclude_chars="aeiouAEIOU")
    
    for _ in range(10):
        password = gen.generate()
        print(f"Generated: {password}")
        
        # Verify no vowels are present
        assert not any(char in "aeiouAEIOU" for char in password), f"Vowels found in: {password}"
    
    print("✓ Character exclusion test passed!")

def test_pronounceable_passwords():
    """Test pronounceable password generation."""
    print("\nTesting pronounceable passwords...")
    
    gen = PasswordGenerator()
    
    # Test basic CVCV pattern
    password = gen.generate_pronounceable(length=4, pattern="CVCV")
    print(f"CVCV pattern: {password}")
    assert len(password.split('-')) == 4
    
    # Test with capitalization
    password = gen.generate_pronounceable(length=3, pattern="CVCV", capitalize=True)
    print(f"Capitalized: {password}")
    assert all(syllable[0].isupper() for syllable in password.split('-'))
    
    # Test different pattern
    password = gen.generate_pronounceable(length=2, pattern="CVCCV")
    print(f"CVCCV pattern: {password}")
    
    # Test without separator
    password = gen.generate_pronounceable(length=3, pattern="CVCV", separator="")
    print(f"No separator: {password}")
    assert len(password) >= 12  # 3 syllables * 4 chars each
    
    print("✓ Pronounceable passwords test passed!")

def test_combined_features():
    """Test using multiple features together."""
    print("\nTesting combined features...")
    
    # Test memorable passwords with character exclusion
    gen = PasswordGenerator(exclude_chars="l1I0O")
    
    for _ in range(3):
        password = gen.generate_memorable(word_count=3, add_number=True)
        print(f"Memorable with exclusion: {password}")
        
        # Verify excluded characters are not present
        assert not any(char in "l1I0O" for char in password), f"Excluded chars found in: {password}"
    
    print("✓ Combined features test passed!")

def main():
    """Run all tests."""
    try:
        test_character_exclusion()
        test_pronounceable_passwords()
        test_combined_features()
        
        print("\n🎉 All new feature tests passed!")
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())