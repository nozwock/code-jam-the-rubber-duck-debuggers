import base64
import hashlib
import os
from enum import Enum
from typing import Protocol

import argon2
import cryptography.hazmat.primitives.ciphers.aead as cryptography_ciphers


class KDFInterface(Protocol):
    salt: bytes

    def hash(self, secret: bytes) -> bytes:
        ...


class PBKDF2(KDFInterface):
    def __init__(self, salt: bytes | None = None, iterations: int = 500_000):
        self.salt = os.urandom(16) if salt is None else salt
        self.iterations = iterations

    def hash(self, secret: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", secret, self.salt, self.iterations)


class Argon2(KDFInterface):
    def __init__(
        self,
        salt: bytes | None = None,
        time_cost: int = argon2.DEFAULT_TIME_COST,
        memory_cost: int = argon2.DEFAULT_MEMORY_COST,
        parallelism: int = argon2.DEFAULT_PARALLELISM,
        hash_len: int = argon2.DEFAULT_HASH_LENGTH,
        kind: argon2.Type = argon2.Type.ID,
    ):
        self.salt = os.urandom(16) if salt is None else salt
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_len = hash_len
        self.kind = kind

    def hash(self, secret: bytes) -> bytes:
        return argon2.low_level.hash_secret_raw(
            secret=secret,
            salt=self.salt,
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.hash_len,
            type=self.kind,
        )


class PBCipherInterface(Protocol):
    """Common interface for a password-based cipher."""

    def encrypt(
        self, data: bytes, secret: bytes, kdf: KDFInterface = Argon2()
    ) -> bytes:
        ...

    def decrypt(
        self, data: bytes, secret: bytes, kdf: KDFInterface = Argon2()
    ) -> bytes:
        ...


class PBAESGCM(PBCipherInterface):
    """Password-based AESGCM."""

    SEP = b"$"

    def encrypt(
        self, data: bytes, secret: bytes, kdf: KDFInterface = Argon2()
    ) -> bytes:
        salt = kdf.salt
        key = kdf.hash(secret)
        cipher = cryptography_ciphers.AESGCM(key)
        nonce = os.urandom(12)

        encrypted_data = cipher.encrypt(nonce, data, None)
        return (
            base64.b64encode(salt)
            + self.SEP
            + base64.b64encode(nonce)
            + self.SEP
            + base64.b64encode(encrypted_data)
        )

    def decrypt(
        self, data: bytes, secret: bytes, kdf: KDFInterface = Argon2()
    ) -> bytes:
        salt, nonce, data = map(base64.b64decode, data.split(self.SEP))
        assert len(nonce) == 12, "Corrupted encrypted data."

        kdf.salt = salt
        key = kdf.hash(secret)
        cipher = cryptography_ciphers.AESGCM(key)

        return cipher.decrypt(nonce, data, None)


class PBChaCha20(PBCipherInterface):
    """Password-based Chacha20."""

    SEP = b"$"

    def encrypt(
        self, data: bytes, secret: bytes, kdf: KDFInterface = Argon2()
    ) -> bytes:
        salt = kdf.salt
        key = kdf.hash(secret)
        cipher = cryptography_ciphers.ChaCha20Poly1305(key)
        nonce = os.urandom(12)

        encrypted_data = cipher.encrypt(nonce, data, None)
        return (
            base64.b64encode(salt)
            + self.SEP
            + base64.b64encode(nonce)
            + self.SEP
            + base64.b64encode(encrypted_data)
        )

    def decrypt(
        self, data: bytes, secret: bytes, kdf: KDFInterface = Argon2()
    ) -> bytes:
        salt, nonce, data = map(base64.b64decode, data.split(self.SEP))
        assert len(nonce) == 12, "Corrupted encrypted data."

        kdf.salt = salt
        key = kdf.hash(secret)
        cipher = cryptography_ciphers.ChaCha20Poly1305(key)

        return cipher.decrypt(nonce, data, None)


class Cipher(Enum):
    AESGCM = PBAESGCM
    ChaCha20 = PBChaCha20


class KDF(Enum):
    PBKDF2 = PBKDF2
    Argon2 = Argon2


if __name__ == "__main__":
    cipher = PBChaCha20()
    encrypted = cipher.encrypt(b"hello world", b"1234")
    decrypted = cipher.decrypt(encrypted, b"1234")
    print(f"{decrypted, encrypted=}")
