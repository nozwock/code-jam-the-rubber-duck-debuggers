import base64
import hashlib
import os
from enum import Enum
from typing import Protocol

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Cipher(Enum):
    """Adds the option of choosing the type of cipher, which would \
be chosen by the encrypter."""

    Ceaser = 1
    Transposition = 2
    AES = 3
    Vigenere = 4
    Playfair = 5
    Hill_Cipher = 6


class KDF(Protocol):
    salt: bytes

    def hash(self, secret: bytes) -> bytes:
        ...


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
    return cipher


def decrypt_ceaser(cipher: str, password: int) -> str:
    """Decrypts message using ceaser cipher"""
    password = password % 26
    text = ""
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
    return text


def encrypt_transposition(text: str, password: str) -> str:
    """Encrypts message using transposition cipher"""
    try:
        int(password)
    except ValueError:
        # get the order for the string coverage
        password = list(password)
    else:
        # get the order for the number coverage
        password = list(set(int(digits) for digits in str(password)))
        print(password)


def decrypt_transposition(cipher: str, password: str) -> str:
    """Decrypts message using transposition cipher"""


def deriveKey_aes(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """Derives key for AES"""
    if salt is None:
        salt = os.urandom(16)
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf8"), salt, 500_000), salt


def encrypt_aes(text: str, password: str) -> str:
    """Encrypts message using AES cipher"""
    key, salt = deriveKey_aes(password)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    data = text.encode()
    ciphertext = aes.encrypt(nonce, data, None)
    return "{}${}${}".format(
        base64.b64encode(salt).decode(),
        base64.b64encode(nonce).decode(),
        base64.b64encode(ciphertext).decode(),
    )


def decrypt_aes(cipher: str, password: str) -> str:
    """Decrypts message using AES cipher"""
    salt, nonce, cipher_data = map(base64.b64decode, cipher.split("$"))
    key, _ = deriveKey_aes(password, salt)
    aes = AESGCM(key)
    decrypted = aes.decrypt(nonce, cipher_data, None)
    return decrypted.decode()


def encrypt_vigenere(text: str, password: str) -> str:
    """Encrypts message using vigenere cipher"""
    cipher = ""
    while len(password) < len(text):
        password += password
    for count, letter in enumerate(text, 0):
        unicode_letter = ord(letter)
        unicode_password = ord(password[count])
        if unicode_password >= 65 and unicode_password <= 90:
            unicode_password = unicode_password % 65
        if unicode_password >= 97 and unicode_password <= 122:
            unicode_password = unicode_password % 97
        if unicode_letter >= 65 and unicode_letter <= 90:  # Capital Letters
            unicode_letter += unicode_password
            if unicode_letter > 90:
                unicode_letter -= 26
        elif unicode_letter >= 97 and unicode_letter <= 122:  # Small Letters
            unicode_letter += unicode_password
            if unicode_letter > 122:
                unicode_letter -= 26
        cipher = cipher + chr(unicode_letter)
    return cipher


if __name__ == "__main__":
    cipher = encrypt_aes("duniya", "hello")
    print(cipher)
    print(decrypt_aes(cipher, "hello"))
    # print(encrypt_vigenere("ATTACKATDAWN", "LEMON"))
    # print(encrypt_vigenere("attaCKatdawn", "LeMon"))
