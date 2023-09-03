from enum import Enum
import os
from binascii import hexlify, unhexlify
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib


class Cipher(Enum):
    """Adds the option of choosing the type of cipher, which would \
be chosen by the encrypter."""

    Ceaser = 1
    Transposition = 2
    Subsitution = 3
    Vigenere = 4
    Playfair = 5
    Hill_Cipher = 6


def encrypt_ceaser(text: str, password: int) -> str:
    """Encrypts message using ceaser cipher"""
    password = password % 26
    cipher = ""
    for letter in text:
        unicode_letter = ord(letter)
        if unicode_letter >= 65 and unicode_letter <= 90:  # Capital Letters
            unicode_letter += password
            if unicode_letter > 90:
                unicode_letter -= 26
        elif unicode_letter >= 97 and unicode_letter <= 122:  # Small Letters
            unicode_letter += password
            if unicode_letter > 122:
                unicode_letter -= 26
        cipher = cipher + chr(unicode_letter)
    return (cipher)


def decrypt_ceaser(cipher: str, password: int) -> str:
    """Decrypts message using ceaser cipher"""
    password = password % 26
    text = ""
    # A would be 3 = D
    for letter in cipher:
        unicode_letter = ord(letter)
        if unicode_letter >= 65 and unicode_letter <= 90:  # Capital Letters
            unicode_letter -= password
            if unicode_letter < 65:
                unicode_letter += 26
        elif unicode_letter >= 97 and unicode_letter <= 122:  # Small Letters
            unicode_letter -= password
            if unicode_letter < 97:
                unicode_letter += 26
        text = text + chr(unicode_letter)
    return (text)


def encrypt_transposition(text: str, password: str) -> str:
    """Encrypts message using transposition cipher"""
    try:
        int(password)
    except ValueError:
        # get the order for the string coverage
        password = (list(password))
    else:
        # get the order for the number coverage
        password = list(set(int(digits) for digits in str(password)))
        print(password)


def decrypt_transposition(cipher: str, password: str) -> str:
    """Decrypts message using transposition cipher"""


def deriveKey_aes(password: str, salt: bytes = None) -> [str, bytes]:
    """Derives key for AES"""
    if salt is None:
        salt = os.urandom(8)
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf8"), salt, 1000), salt


def encrypt_aes(text: str, password: str) -> str:
    """Encrypts message using AES cipher"""
    key, salt = deriveKey_aes(password)
    aes = AESGCM(key)
    iv = os.urandom(12)
    text = text.encode("utf8")
    ciphertext = aes.encrypt(iv, text, None)
    return "%s-%s-%s" % (hexlify(salt).decode("utf8"),
                         hexlify(iv).decode("utf8"),
                         hexlify(ciphertext).decode("utf8"))


def decrypt_aes(cipher: str, password: str) -> str:
    """Decrypts message using AES cipher"""
    salt, iv, cipher = map(unhexlify, cipher.split("-"))
    key, _ = deriveKey_aes(password, salt)
    aes = AESGCM(key)
    plaintext = aes.decrypt(iv, cipher, None)
    # aes.decrypt()
    return plaintext.decode("utf8")


if __name__ == "__main__":
    cipher = encrypt_aes("duniya", "hello")
    print(cipher)
    print(decrypt_aes(cipher, "hello"))
