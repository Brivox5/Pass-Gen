"""
Benchmarking script to compare Pass-Gen with other password generation libraries.
This script tests security strength by calculating time to crack using entropy-based methods.
"""

import time
import math
import secrets
import random
import string
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from pass_gen import PasswordGenerator

# Try to import other password libraries
try:
    import passwordgenerator
    HAS_PASSWORDGENERATOR = True
except ImportError:
    HAS_PASSWORDGENERATOR = False

try:
    from passlib import pwd
    HAS_PASSLIB = True
except ImportError:
    HAS_PASSLIB = False

try:
    from faker import Faker
    HAS_FAKER = True
except ImportError:
    HAS_FAKER = False

# Custom simple password generators for comparison
def generate_simple_password(length=16, use_special=True):
    """Simple password generator using random module (not cryptographically secure)"""
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def generate_crypto_password(length=16, use_special=True):
    """Cryptographically secure password using secrets module"""
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# Functions for specific library comparisons
def generate_passlib_password(length=16):
    """Generate password using passlib library"""
    if HAS_PASSLIB:
        return pwd.genword(length=length)
    return ""

def generate_passwordgenerator_password():
    """Generate password using passwordgenerator library"""
    if HAS_PASSWORDGENERATOR:
        import subprocess
        try:
            result = subprocess.run(
                ["python", "-m", "passwordgenerator", "-e", "4"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass
    return ""

def generate_faker_password():
    """Generate password using faker library"""
    if HAS_FAKER:
        fake = Faker()
        return fake.password()
    return ""

class BenchmarkResults:
    """Store and analyze benchmark results"""
    
    def __init__(self):
        self.results = {}
        self.entropy_values = {}
        self.crack_times = {}
    
    def add_result(self, library_name: str, password: str, generation_time: float):
        """Add benchmark result for a library"""
        if library_name not in self.results:
            self.results[library_name] = []
            self.entropy_values[library_name] = []
            self.crack_times[library_name] = []
        
        self.results[library_name].append((password, generation_time))
        
        # Calculate entropy
        entropy = self.calculate_entropy(password)
        self.entropy_values[library_name].append(entropy)
        
        # Calculate estimated crack time
        crack_time = self.estimate_crack_time(entropy)
        self.crack_times[library_name].append(crack_time)
    
    def calculate_entropy(self, password: str) -> float:
        """Calculate password entropy in bits"""
        
        # Check if this is a memorable passphrase from Pass-Gen library
        # Pass-Gen memorable passwords follow pattern: word-word-word-word-number
        # or similar patterns with separators and optional capitalization
        
        # Common passphrase patterns
        separators = ['-', '_']
        
        # Try to detect Pass-Gen memorable pattern
        for separator in separators:
            if separator in password:
                parts = password.split(separator)
                
                # Check if this matches Pass-Gen memorable pattern (4 words + optional number)
                if (len(parts) >= 4 and 
                    all(3 <= len(part) <= 12 for part in parts[:-1]) and  # Words are 3-12 chars
                    (len(parts[-1]) in [0, 1, 2, 3, 4] or parts[-1].isdigit())):  # Last part might be a number
                    
                    # Count actual words (excluding any numbers at the end)
                    word_count = sum(1 for part in parts if part and not part.isdigit())
                    if word_count >= 3:  # At least 3 words to consider it a passphrase
                        # EFF large wordlist has 7776 words
                        wordlist_size = 7776
                        return word_count * math.log2(wordlist_size)
        
        # Additional check for passphrases with numbers mixed in
        # Pattern like: Word123-word456-word789-word0
        if '-' in password:
            parts = password.split('-')
            if len(parts) >= 3:
                # Check if parts look like words with optional numbers
                word_count = 0
                for part in parts:
                    # Remove digits from the end to check if the base looks like a word
                    base_word = part.rstrip('0123456789')
                    if 3 <= len(base_word) <= 12:  # Reasonable word length
                        word_count += 1
                
                if word_count >= 3:
                    wordlist_size = 7776
                    return word_count * math.log2(wordlist_size)
        
        # Standard character-based entropy calculation for random passwords
        char_set = set(password)
        char_pool_size = 0
        
        # Determine character pool size
        if any(c in string.ascii_lowercase for c in password):
            char_pool_size += 26
        if any(c in string.ascii_uppercase for c in password):
            char_pool_size += 26
        if any(c in string.digits for c in password):
            char_pool_size += 10
        if any(c in string.punctuation for c in password):
            char_pool_size += len(string.punctuation)
        
        if char_pool_size == 0:
            char_pool_size = 1  # Avoid division by zero
        
        return len(password) * math.log2(char_pool_size)
    
    def estimate_crack_time(self, entropy_bits: float) -> float:
        """
        Estimate time to crack password (in seconds)
        Based on NIST SP 800-63B and OWASP guidelines
        Assumes 10^12 guesses per second (modern GPU cracking)
        """
        guesses_needed = 2 ** entropy_bits
        guesses_per_second = 1e12  # 1 trillion guesses per second
        return guesses_needed / guesses_per_second
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics for all libraries"""
        stats = {}
        
        for library in self.results.keys():
            times = [t for _, t in self.results[library]]
            entropies = self.entropy_values[library]
            crack_times = self.crack_times[library]
            
            stats[library] = {
                'avg_generation_time': np.mean(times) if times else 0,
                'avg_entropy': np.mean(entropies) if entropies else 0,
                'avg_crack_time': np.mean(crack_times) if crack_times else 0,
                'min_entropy': np.min(entropies) if entropies else 0,
                'max_entropy': np.max(entropies) if entropies else 0,
                'sample_count': len(times)
            }
        
        return stats

def run_benchmark(num_samples: int = 100) -> BenchmarkResults:
    """Run comprehensive benchmark of password generation libraries"""
    results = BenchmarkResults()
    
    # Test configurations (must meet minimum entropy requirements)
    configs = [
        (16, True, True, True, True),   # Standard secure (high entropy)
        (20, True, True, True, False),   # No special chars but longer
        (24, True, True, True, True),   # Very long password
        (12, True, True, True, True),   # Shorter but with all char sets
    ]
    
    print("Running password generation benchmark...")
    print(f"Testing {num_samples} samples per configuration")
    
    for config in configs:
        length, upper, lower, digits, special = config
        
        print(f"\nTesting configuration: length={length}, upper={upper}, lower={lower}, digits={digits}, special={special}")
        
        # Test Pass-Gen library
        pass_gen = PasswordGenerator(
            length=length,
            include_uppercase=upper,
            include_lowercase=lower,
            include_digits=digits,
            include_special=special
        )
        
        for i in range(num_samples):
            start_time = time.time()
            password = pass_gen.generate()
            gen_time = time.time() - start_time
            results.add_result("Pass-Gen", password, gen_time)
        
        # Test simple random generator
        for i in range(num_samples):
            start_time = time.time()
            password = generate_simple_password(length, special)
            gen_time = time.time() - start_time
            results.add_result("Simple Random", password, gen_time)
        
        # Test crypto secure generator
        for i in range(num_samples):
            start_time = time.time()
            password = generate_crypto_password(length, special)
            gen_time = time.time() - start_time
            results.add_result("Crypto Secure", password, gen_time)
        
        # Test memorable passwords
        pass_gen_mem = PasswordGenerator()
        for i in range(num_samples):
            start_time = time.time()
            password = pass_gen_mem.generate_memorable(
                word_count=4,
                separator='-',
                capitalize=True,
                add_number=True
            )
            gen_time = time.time() - start_time
            results.add_result("Pass-Gen Memorable", password, gen_time)
        
        # Test passlib library
        if HAS_PASSLIB:
            for i in range(num_samples):
                start_time = time.time()
                password = generate_passlib_password(length)
                gen_time = time.time() - start_time
                results.add_result("Passlib", password, gen_time)
        
        # Test passwordgenerator library
        if HAS_PASSWORDGENERATOR:
            for i in range(num_samples):
                start_time = time.time()
                password = generate_passwordgenerator_password()
                gen_time = time.time() - start_time
                results.add_result("PasswordGenerator", password, gen_time)
        
        # Test faker library
        if HAS_FAKER:
            for i in range(num_samples):
                start_time = time.time()
                password = generate_faker_password()
                gen_time = time.time() - start_time
                results.add_result("Faker", password, gen_time)
    
    return results

def generate_plots(results: BenchmarkResults, output_path: str = "benchmark_results.png"):
    """Generate comparison plots"""
    stats = results.get_statistics()
    
    libraries = list(stats.keys())
    avg_entropy = [stats[lib]['avg_entropy'] for lib in libraries]
    avg_crack_time_years = [stats[lib]['avg_crack_time'] / (3600 * 24 * 365.25) for lib in libraries]
    
    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Entropy comparison
    bars1 = ax1.bar(libraries, avg_entropy, color=['blue', 'orange', 'green', 'red'])
    ax1.set_title('Average Password Entropy (bits)')
    ax1.set_ylabel('Entropy (bits)')
    ax1.tick_params(axis='x', rotation=45)
    
    # Crack time comparison (log scale)
    bars2 = ax2.bar(libraries, avg_crack_time_years, color=['blue', 'orange', 'green', 'red'])
    ax2.set_yscale('log')
    ax2.set_title('Average Time to Crack (years, log scale)')
    ax2.set_ylabel('Years (log scale)')
    ax2.tick_params(axis='x', rotation=45)
    
    # Generation time comparison
    gen_times = [stats[lib]['avg_generation_time'] * 1000 for lib in libraries]  # Convert to ms
    bars3 = ax3.bar(libraries, gen_times, color=['blue', 'orange', 'green', 'red'])
    ax3.set_title('Average Generation Time')
    ax3.set_ylabel('Time (milliseconds)')
    ax3.tick_params(axis='x', rotation=45)
    
    # Entropy distribution box plot
    entropy_data = [results.entropy_values[lib] for lib in libraries]
    ax4.boxplot(entropy_data, labels=libraries)
    ax4.set_title('Entropy Distribution Across Libraries')
    ax4.set_ylabel('Entropy (bits)')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Plots saved to {output_path}")

def print_detailed_report(results: BenchmarkResults):
    """Print comprehensive benchmark report"""
    stats = results.get_statistics()
    
    print("\n" + "="*80)
    print("PASSWORD GENERATION BENCHMARK REPORT")
    print("="*80)
    
    for library, data in stats.items():
        print(f"\n{library}:")
        print(f"  Samples: {data['sample_count']}")
        print(f"  Avg Generation Time: {data['avg_generation_time']*1000:.4f} ms")
        print(f"  Avg Entropy: {data['avg_entropy']:.2f} bits")
        print(f"  Min Entropy: {data['min_entropy']:.2f} bits")
        print(f"  Max Entropy: {data['max_entropy']:.2f} bits")
        
        # Convert crack time to human-readable format
        crack_time = data['avg_crack_time']
        if crack_time < 60:
            time_str = f"{crack_time:.2e} seconds"
        elif crack_time < 3600:
            time_str = f"{crack_time/60:.2e} minutes"
        elif crack_time < 86400:
            time_str = f"{crack_time/3600:.2e} hours"
        elif crack_time < 31536000:
            time_str = f"{crack_time/86400:.2e} days"
        else:
            time_str = f"{crack_time/31536000:.2e} years"
        
        print(f"  Avg Time to Crack: {time_str}")
    
    print("\n" + "="*80)
    print("RECOMMENDATIONS:")
    print("="*80)
    
    # Find best library based on entropy
    best_lib = max(stats.items(), key=lambda x: x[1]['avg_entropy'])
    print(f"✓ Best overall: {best_lib[0]} ({best_lib[1]['avg_entropy']:.2f} bits average entropy)")
    
    # Security recommendations
    print("✓ For high security: Use libraries with >80 bits entropy")
    print("✓ Avoid non-cryptographic random generators for sensitive applications")
    print("✓ Memorable passwords should still maintain high entropy through word count")

if __name__ == "__main__":
    # Run the benchmark
    benchmark_results = run_benchmark(num_samples=50)
    
    # Generate plots
    generate_plots(benchmark_results, "password_benchmark.png")
    
    # Print detailed report
    print_detailed_report(benchmark_results)
    
    # Save raw data for reference
    import json
    with open('benchmark_data.json', 'w') as f:
        json.dump(benchmark_results.get_statistics(), f, indent=2)
    
    print("\nBenchmark completed. Results saved to:")
    print("- password_benchmark.png (visual comparison)")
    print("- benchmark_data.json (raw statistics)")