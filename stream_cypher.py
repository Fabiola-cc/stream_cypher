from random import randint, seed

def keystream_random(given_seed, size):
    """
    Generate a random keystream of the given size.
    
    Use the provided seed to initialize the random number generator for reproducibility.
    """
    keystream = []
    seed(given_seed) # Initialize PRNG with given seed
    for _ in range(size):
        keystream.append(randint(0, 255)) # Generate a random byte (0-255)
    return keystream


# Example
og_message = "Hello, World!"
key = keystream_random(3, len(og_message))
print("key: ", key)