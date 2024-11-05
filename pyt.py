import hashlib
import itertools
import string
import concurrent.futures
import time

# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to read password dictionary from a file
def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to apply rules to generate variations
def generate_variants(password):
    variants = set()
    # Original password
    variants.add(password)

    # Add numbers to the end
    for i in range(10):
        variants.add(f"{password}{i}")

    # Change case variations
    variants.add(password.lower())
    variants.add(password.upper())
    variants.add(password.capitalize())

    # More complex variations can be added here

    return variants

# Function to attempt cracking with dictionary attack
def dictionary_attack(hashed_password, dictionary):
    for password in dictionary:
        if hash_password(password) == hashed_password:
            return password
    return None

# Function for brute force cracking
def brute_force_crack(hashed_password, max_length=4):
    characters = string.ascii_letters + string.digits + string.punctuation
    for length in range(1, max_length + 1):
        for attempt in itertools.product(characters, repeat=length):
            attempt_password = ''.join(attempt)
            if hash_password(attempt_password) == hashed_password:
                return attempt_password
    return None

# Function to attempt cracking with rules
def rule_based_crack(hashed_password, dictionary):
    for password in dictionary:
        variants = generate_variants(password)
        for variant in variants:
            if hash_password(variant) == hashed_password:
                return variant
    return None

# Function to run multiple cracking methods
def run_cracker(hashed_password, dictionary):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(dictionary_attack, hashed_password, dictionary): 'Dictionary Attack',
            executor.submit(rule_based_crack, hashed_password, dictionary): 'Rule-Based Attack',
            executor.submit(brute_force_crack, hashed_password): 'Brute Force Attack'
        }
        for future in concurrent.futures.as_completed(futures):
            method = futures[future]
            try:
                result = future.result()
                if result:
                    print(f"Password found using {method}: {result}")
                    return result
            except Exception as e:
                print(f"{method} failed: {e}")
    print("Password not found.")
    return None

# Example usage
if __name__ == "__main__":
    # Input the hash of the password you want to crack
    target_hash = input("Enter the SHA-256 hash of the password to crack: ")

    # Load dictionary from a file
    dictionary_file = 'pass.txt'  # Change this to your dictionary file path
    dictionary = load_dictionary(dictionary_file)

    # Start the cracking process
    start_time = time.time()
    found_password = run_cracker(target_hash, dictionary)
    if found_password:
        print(f"Password found: {found_password}")
    else:
        print("Password not found.")
    print(f"Cracking completed in {time.time() - start_time:.2f} seconds.")

