#!/usr/bin/env python3
"""
Test script to verify EFF wordlist implementation in Pass-Gen library.

This script tests the new EFF large wordlist implementation for memorable passwords.
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pass_gen.pass_gen import PasswordGenerator

def test_eff_wordlist_loading():
    """Test that the EFF wordlist loads correctly."""
    print("Testing EFF wordlist loading...")
    
    generator = PasswordGenerator()
    
    # Load words from EFF wordlist
    words = generator._load_eff_wordlist()
    
    # Check that we have a substantial number of words
    print(f"Loaded {len(words)} words from EFF wordlist")
    
    if len(words) >= 7000:  # Should be close to 7776
        print("✓ EFF wordlist loaded successfully with substantial word count")
        return True
    else:
        print(f"✗ Expected at least 7000 words, got {len(words)}")
        return False

def test_memorable_password_generation():
    """Test memorable password generation with EFF wordlist."""
    print("\nTesting memorable password generation...")
    
    generator = PasswordGenerator()
    
    # Test different configurations
    configs = [
        (4, '-', False, False),  # 4 words, hyphen separator, no caps, no number
        (3, '.', True, False),   # 3 words, dot separator, capitalize, no number
        (5, ' ', False, True),   # 5 words, space separator, no caps, with number
        (2, '_', True, True),    # 2 words, underscore separator, capitalize, with number
    ]
    
    for i, (word_count, separator, capitalize, add_number) in enumerate(configs):
        print(f"\nTesting configuration {i+1}: {word_count} words, sep='{separator}', cap={capitalize}, num={add_number}")
        
        try:
            password = generator.generate_memorable(
                word_count=word_count,
                separator=separator,
                capitalize=capitalize,
                add_number=add_number
            )
            
            print(f"  Generated: {password}")
            
            # Basic validation
            parts = password.split(separator)
            if add_number:
                # Last part should be a number
                assert parts[-1].isdigit(), f"Last part should be a number: {password}"
                parts = parts[:-1]
            
            assert len(parts) == word_count, f"Expected {word_count} parts, got {len(parts)}: {password}"
            
            if capitalize:
                for part in parts:
                    assert part[0].isupper(), f"Word should be capitalized: {part}"
                    
            print(f"  ✓ Configuration {i+1} passed")
            
        except Exception as e:
            print(f"  ✗ Configuration {i+1} failed: {e}")
            return False
    
    print("✓ Memorable password generation works correctly")
    return True

def test_word_diversity():
    """Test that generated passwords use diverse words."""
    print("\nTesting word diversity...")
    
    gen = PasswordGenerator()
    
    # Generate multiple passwords and collect all words used
    all_words = []
    for _ in range(20):
        password = gen.generate_memorable(word_count=3)
        words = password.split('-')
        all_words.extend(words)
    
    # Count unique words
    unique_words = set(all_words)
    print(f"Used {len(unique_words)} unique words out of {len(all_words)} total")
    
    # Should have good diversity (at least 50% unique)
    diversity_ratio = len(unique_words) / len(all_words)
    assert diversity_ratio >= 0.5, f"Low word diversity: {diversity_ratio:.2f}"
    
    print("✓ Word diversity test passed!")
    return True

def test_character_exclusion():
    """Test character exclusion functionality with memorable passwords."""
    print("\nTesting character exclusion...")
    
    gen = PasswordGenerator(exclude_chars="aeiouAEIOU")
    
    for _ in range(5):
        password = gen.generate_memorable(word_count=3)
        print(f"Memorable with exclusion: {password}")
        
        # Verify no vowels are present
        assert not any(char in "aeiouAEIOU" for char in password), f"Vowels found in: {password}"
    
    print("✓ Character exclusion test passed!")
    return True

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
    
    print("✓ Pronounceable passwords test passed!")
    return True

def test_fallback_mechanism():
    """Test fallback mechanism when EFF wordlist is not available."""
    print("\nTesting fallback mechanism...")
    
    # Create a temporary directory and copy the wordlist
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a generator with a non-existent wordlist path
        gen = PasswordGenerator()
        
        # Mock the wordlist path to a non-existent file
        original_load = gen._load_eff_wordlist
        gen._load_eff_wordlist = lambda: []
        
        try:
            # Should fall back to basic words
            password = gen.generate_memorable(word_count=3)
            print(f"Fallback password: {password}")
            
            # Should contain basic words (not empty)
            assert password and '-' in password
            
        finally:
            # Restore original method
            gen._load_eff_wordlist = original_load
    
    print("✓ Fallback mechanism test passed!")
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("EFF Wordlist Implementation Tests")
    print("=" * 60)
    
    tests = [
        test_eff_wordlist_loading,
        test_memorable_password_generation,
        test_word_diversity,
        test_character_exclusion,
        test_pronounceable_passwords,
        test_fallback_mechanism,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, result in enumerate(results):
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"Test {i+1}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! EFF wordlist implementation is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())