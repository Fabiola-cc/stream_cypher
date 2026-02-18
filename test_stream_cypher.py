import unittest
from stream_cypher import encrypt, decrypt

class TestStreamCipher(unittest.TestCase):

    def setUp(self):
        """Datos base para las pruebas"""
        self.message = "Hello, World!"
        self.key1 = 3
        self.key2 = 10

    # 1. El descifrado recupera el mensaje original
    def test_decryption_recovers_original(self):
        encrypted = encrypt(self.message, self.key1)
        decrypted = decrypt(encrypted, self.key1)

        self.assertEqual(decrypted, self.message)

    # 2. Diferentes claves producen diferentes cifrados
    def test_different_keys_produce_different_ciphertext(self):
        encrypted1 = encrypt(self.message, self.key1)
        encrypted2 = encrypt(self.message, self.key2)

        self.assertNotEqual(encrypted1, encrypted2)

    # 3. Misma clave produce mismo cifrado (determinismo)
    def test_same_key_same_ciphertext(self):
        encrypted1 = encrypt(self.message, self.key1)
        encrypted2 = encrypt(self.message, self.key1)

        self.assertEqual(encrypted1, encrypted2)

    # 4. Manejo de diferentes longitudes
    def test_different_message_lengths(self):
        messages = [
            "",                         # vacío
            "A",                        # 1 caracter
            "Hola",                     # corto
            "Mensaje de mayor largo",
            "A" * 1000                  # muy largo
        ]

        for msg in messages:
            encrypted = encrypt(msg, self.key1)
            decrypted = decrypt(encrypted, self.key1)

            self.assertEqual(decrypted, msg)


# Ejecutar pruebas
if __name__ == "__main__":
    unittest.main()
