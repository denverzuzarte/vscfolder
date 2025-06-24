import numpy as np

n = 10000000000
is_prime = np.ones(n, dtype=bool)  # Create a boolean array initialized to True
is_prime[0:2] = False  # 0 and 1 are not prime

# Use the Sieve of Eratosthenes algorithm for optimization
for i in range(2, int(np.sqrt(n)) + 1):
    if is_prime[i]:
        is_prime[i * i:n:i] = False  # Mark multiples of i as non-prime

# Extract the prime numbers
primes = np.nonzero(is_prime)[0]  # Get indices of True values, which are primes
print(primes)