from enum import Enum

class Cipher(Enum):
    '''
    Adds the option of choosing the type of cipher
    '''
    AES = 1
    Ceaser = 2
    Transposition = 3
    Subsitution = 4
    Vigenere = 5
    Playfair = 6
    Hill_Cipher = 7
