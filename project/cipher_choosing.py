import base64
import hashlib
import os
import argon2
from enum import Enum
from typing import Protocol
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


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


def deriveKey_pbkdf(password: str,
                    salt: bytes | None = None) -> tuple[bytes, bytes]:
    """Derives key for AES pbkdf"""
    if salt is None:
        salt = os.urandom(16)
    return hashlib.pbkdf2_hmac("sha256",
                               password.encode("utf8"),
                               salt, 600_000), salt


def deriveKey_Argon(password: str,
                    salt: bytes | None = None) -> tuple[bytes, bytes]:
    """Derives key for Argon"""
    if salt is None:
        salt = os.urandom(16)
    key = argon2.low_level.hash_secret_raw(
        secret=bytes(password, "utf-8"),
        salt=salt,
        time_cost=argon2.DEFAULT_TIME_COST,
        memory_cost=argon2.DEFAULT_MEMORY_COST,
        parallelism=argon2.DEFAULT_PARALLELISM,
        hash_len=argon2.DEFAULT_HASH_LENGTH,
        type=argon2.Type.ID,
    )
    return key, salt


def encrypt_aes_pbkdf(text: str, password: str) -> str:
    """Encrypts message using AES cipher"""
    key, salt = deriveKey_pbkdf(password)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    data = text.encode()
    ciphertext = aes.encrypt(nonce, data, None)
    return "{}${}${}".format(
        base64.b64encode(salt).decode(),
        base64.b64encode(nonce).decode(),
        base64.b64encode(ciphertext).decode(),
    )


def encrypt_aes_argon(text: str, password: str) -> bytes:
    """Encrypts message using AES cipher"""
    key, salt = deriveKey_Argon(password)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    data = text.encode()
    ciphertext = aes.encrypt(nonce, data, None)
    return "{}${}${}".format(
        base64.b64encode(salt).decode(),
        base64.b64encode(nonce).decode(),
        base64.b64encode(ciphertext).decode(),
    )


def encrypt_chacha_pbkdf(text: str, password: str) -> bytes:
    """Encrypts message using chacha cipher"""
    key, salt = deriveKey_pbkdf(password)
    text = bytes(text, "utf-8")
    password = bytes(password, "utf-8")
    chacha = ChaCha20Poly1305(key)
    nonce = os.urandom(12)
    ciphertext = chacha.encrypt(nonce, text, password)
    return "{}${}${}".format(
        base64.b64encode(salt).decode(),
        base64.b64encode(nonce).decode(),
        base64.b64encode(ciphertext).decode(),
    )


def encrypt_chacha_argon(text: str, password: str) -> bytes:
    """Encrypts message using chacha cipher"""
    key, salt = deriveKey_Argon(password)
    text = bytes(text, "utf-8")
    password = bytes(password, "utf-8")
    chacha = ChaCha20Poly1305(key)
    nonce = os.urandom(12)
    ciphertext = chacha.encrypt(nonce, text, password)
    return "{}${}${}".format(
        base64.b64encode(salt).decode(),
        base64.b64encode(nonce).decode(),
        base64.b64encode(ciphertext).decode(),
    )


def decrypt_aes_pbkdf(cipher: str, password: str) -> str:
    """Decrypts message using AES cipher"""
    salt, nonce, cipher_data = map(base64.b64decode, cipher.split("$"))
    key, _ = deriveKey_pbkdf(password, salt)
    aes = AESGCM(key)
    decrypted = aes.decrypt(nonce, cipher_data, None)
    return decrypted.decode()


def decrypt_aes_argon(cipher: str, password: str) -> str:
    """Decrypts message using AES argon encryption"""
    salt, nonce, cipher_data = map(base64.b64decode, cipher.split("$"))
    key, _ = deriveKey_Argon(password, salt)
    aes = AESGCM(key)
    decrypted = aes.decrypt(nonce, cipher_data, None)
    return decrypted.decode()


def decrypt_chacha_pbkdf(cipher: str, password: str) -> str:
    """Decrypts message using AES argon encryption"""
    salt, nonce, cipher_data = map(base64.b64decode, cipher.split("$"))
    key, _ = deriveKey_pbkdf(password, salt)
    password = bytes(password, "utf-8")
    chacha = ChaCha20Poly1305(key)
    decrypted = chacha.decrypt(nonce, cipher_data, password)
    return decrypted.decode()


def decrypt_chacha_argon(cipher: str, password: str) -> str:
    """Decrypts message using AES argon encryption"""
    salt, nonce, cipher_data = map(base64.b64decode, cipher.split("$"))
    key, _ = deriveKey_Argon(password, salt)
    password = bytes(password, "utf-8")
    chacha = ChaCha20Poly1305(key)
    decrypted = chacha.decrypt(nonce, cipher_data, password)
    return decrypted.decode()


if __name__ == "__main__":
    cipher = encrypt_chacha_argon("duniya", "hello")
    print(cipher)
    print(decrypt_chacha_argon(cipher, "hello"))
