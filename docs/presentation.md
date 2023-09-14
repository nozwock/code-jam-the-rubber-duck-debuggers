Because the project remains unfinished, the reusable components have been consolidated into a CLI tool.

Here is an overview of the CLI features:
```
Usage: pic-crypt [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  decode        Decode text from an image.
  encode        Encode text within an image.
  hide-text     Generates an image with a hidden secret string by putting it...
  replace-text  Replace text from an image.
```

## Features
## Transcoding
The option to encrypt the data before performing transcoding is available.

There are two implementations available:
- **Direct Encoding:** Each channel of an image pixel stores a single byte of data.
    - **Encoding:**
        ```sh
        Usage: pic-crypt encode direct [OPTIONS]

        Encodes data into an image by utilizing the pixel channels to store each byte
        of the data.

        Input: [exactly 1 required]
        -t, --text TEXT
        -f, --file FILENAME

        Encryption:
        -e, --encrypt
        -k, --key TEXT
        --cipher [AESGCM|ChaCha20]
        --kdf [PBKDF2|Argon2]

        Other options:
        -o, --output FILE
        -w, --width-limit INTEGER
        -c, --channels INTEGER      [default: 3]
        -h, --help                  Show this message and exit.
        ```
        How to use-
        ```sh
        $ python -c 'import this' | pic-crypt encode direct -f - -o tests/direct.png -ek passw0rd
        Image saved to: tests/direct.png
        ```
        ![direct.png](https://github.com/nozwock/code-jam-the-rubber-duck-debuggers/assets/57829219/c54a5fa9-8a60-48a1-b1e6-ff60e2816bb7)
    - **Decoding:**
        ```sh
        $ pic-crypt decode direct tests/direct.png -dk passw0rd
        Decoded data:
        The Zen of Python, by Tim Peters

        Beautiful is better than ugly.
        Explicit is better than implicit.
        Simple is better than complex.
        Complex is better than complicated.
        ...
        ```
- **Steganography:** Utilizes LSB (Least Significant Bit) steganography to embed data by altering the LSB of each channel in the image.
    - **Encoding:**
        ```
        Usage: pic-crypt encode steganography [OPTIONS] IMG

        Encodes data into an image utilizing Steganography.

        Input: [exactly 1 required]
        -t, --text TEXT
        -f, --file FILENAME

        Encryption:
        -e, --encrypt
        -k, --key TEXT
        --cipher [AESGCM|ChaCha20]
        --kdf [PBKDF2|Argon2]

        Other options:
        -o, --output FILE
        -h, --help                  Show this message and exit.
        ```
        How to use-
        ```sh
        $ python -c 'import this' | pic-crypt encode steganography tests/stop.jpg -f - -o tests/stop-lsb.png -ek passw0rd
        Image saved to: tests/stop-lsb.png
        ```
        A side-by-side comparison between the original and encoded images:
        ![](https://github.com/nozwock/code-jam-the-rubber-duck-debuggers/assets/57829219/3d91414a-9a95-43c1-ad1d-f8ef8f6cbb14)
    - **Decoding:**
        ```sh
        $ pic-crypt decode steganography tests/stop-lsb.png -dk passw0rd
        Decoded data:
        The Zen of Python, by Tim Peters

        Beautiful is better than ugly.
        Explicit is better than implicit.
        Simple is better than complex.
        Complex is better than complicated.
        ...
        ```

> [!NOTE]
> These transcodings were achieved through the use of straightforward bit manipulation in conjunction with NumPy arrays.
