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


def encrypt_ceaser(text: str, password: int) -> str:
    """Encrypts message using ceaser cipher"""
    password = password % 26
    cipher = ""
    # A would be 3 = D
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


if __name__ == "__main__":
    print(decrypt_ceaser("ABCDE VWXYZ", 5))
    print(encrypt_ceaser("Hello World", 4))
