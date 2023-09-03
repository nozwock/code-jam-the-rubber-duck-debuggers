from enum import Enum


class Cipher(Enum):
    """Adds the option of choosing the type of cipher, which would \
be chosen by the encrypter."""

    Ceaser = 1
    Transposition = 2
    Subsitution = 3
    Vigenere = 4
    Playfair = 5
    Hill_Cipher = 6
