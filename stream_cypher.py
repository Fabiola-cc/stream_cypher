from random import randint, seed

def keystream_random(key_seed, size):
    """
    Generate a random keystream of the given size.
    
    Use the provided seed to initialize the random number generator for reproducibility.
    """
    keystream = []
    seed(key_seed) # Initialize PRNG with given seed
    for _ in range(size):
        keystream.append(randint(0, 255)) # Generate a random byte (0-255)
    return bytes(keystream)


def encrypt(text, key_seed):
    """ Encrypt the given text using a generated keystream based on given seed"""
    keystream = keystream_random(key_seed, len(text))

    # ZIP combines iterables element-wise, and XOR is applied to each pair of text byte and keystream byte
    encrypted = bytes([t ^ k for t, k in zip(text.encode(), keystream)])
    return encrypted

# Example
og_message = "Hello, World!"
key_seed = 3

encrypted_message = encrypt(og_message, key_seed)
print(f"Original message: {og_message}")
print(f"Encrypted message: {encrypted_message}")