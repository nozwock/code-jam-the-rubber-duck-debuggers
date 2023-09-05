import base64
import hashlib
import os
from enum import Enum
from typing import Protocol
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Cipher(Enum):
    """Adds the option of choosing the type of cipher, which would \
be chosen by the encrypter."""

    AES_PBKDF = 1
    AES_Argon = 2
    Chacha_PBKDF = 3
    Chacha_Argon = 4


class KDF(Protocol):
    salt: bytes

    def hash(self, secret: bytes) -> bytes:
        ...


def deriveKey_aes(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """Derives key for AES"""
    if salt is None:
        salt = os.urandom(16)
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf8"), salt, 600_000), salt


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


if __name__ == "__main__":
    cipher = encrypt_aes("duniya", "hello")
    print(cipher)
    print(decrypt_aes(cipher, "hello"))
