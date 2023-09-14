## Installation
- Using `pipx`.
    1. Install `pipx`.
        ```sh
        python -m pip install --user pipx
        python -m pipx ensurepath
        ```
    2. Open a new terminal or re-login.
    3. Install the project.
        ```sh
        pipx install git+https://github.com/nozwock/code-jam-the-rubber-duck-debuggers.git
        ```
- Using `pip`.
    ```sh
    pip install --user git+https://github.com/nozwock/code-jam-the-rubber-duck-debuggers.git
    ```

- Run with `pic-crypt`

## About

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
### Transcoding
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

These transcodings were accomplished using simple bit manipulation techniques combined with NumPy arrays. They are tied to the 'secret codes' theme as they involve concealing information within an image, often without the user's awareness of its presence.

### Hidden Text

Conceal a "secret" string within an image by interleaving it between repetitions of a selected word, often rendering it challenging to detect.

```
Usage: pic-crypt hide-text [OPTIONS] SECRET REPEAT

  Generates an image with a hidden secret string by putting it in between
  repeations of some string.

Image:
  -w, --width INTEGER   [default: 720]
  -h, --height INTEGER  [default: 480]
  --img-color TEXT      [default: #000000]

Other options:
  -c, --color TEXT      [default: #ffffff]
  --font-size INTEGER   [default: 10]
  -p, --padding TEXT    [default: 0, 2]
  --trim-extra BOOLEAN  [default: True]
  -o, --output FILE
  --help                Show this message and exit.
```

How to use-
```sh
$ pic-crypt hide-text secret helloo
Image saved to: output.png
```
![hidden](https://github.com/nozwock/code-jam-the-rubber-duck-debuggers/assets/57829219/b7a9d769-4d22-469a-9112-8443e156e00c)

Pillow was utilized for rendering the text through repeated placement, employing basic calculations.

### Replace Text

Text replacement within an image is achieved by utilizing the EAST text detection model in conjunction with OpenCV. The process involves inpainting to remove the text and subsequently redrawing the desired text onto the image. These operations are facilitated using OpenCV features.

```
Usage: pic-crypt replace-text [OPTIONS] IMG TEXT

  Replace text from an image.

Pre-processing:
  -w, --width INTEGER      [default: 320]
  -h, --height INTEGER     [default: 320]

Text detection:
  --score-threshold FLOAT  [default: 0.5]
  --nms-threshold FLOAT    [default: 0.3]

Other options:
  -n, --count INTEGER      Number of times to replace image text.  [default: 1]
  -c, --color TEXT
  --font-scale FLOAT       [default: 1]
  --thickness INTEGER      [default: 1]
  -o, --output FILE
  --help                   Show this message and exit.
```

How to use-
```sh
$ pic-crypt replace-text tests/stop.jpg Hello --font-scale 1.6 --thickness 2
Image saved to: output.png
```
![replace-text](https://github.com/nozwock/code-jam-the-rubber-duck-debuggers/assets/57829219/3fb4826e-38bf-455b-890a-a2c5a3234134)

## Contibutors

Here is a summary of each contributor's key contributions:
- **realstealthninja:**
    - Implemented the decoder for the direct transcoder.
    - Implemented the initial version of the LSB steganography transcoder.
    - Added CLI commands for the transcoders.
    - Implemented the preliminary text replacement feature, using `pytesseract`.
    - Contributed to documentation tasks

- **Nhsdkk:**
    - Added an `Image` object and an `EncoderInterface`.
    - Worked on frontend development for the planned multiplayer game project.

- **SimonMeersschaut:**
    - Worked on the flask webserver backend development for the planned multiplayer game project.

- **Sapient44:**
    - Implemented password-based encryption using symmetric encryption and key derivation functions.
    - Added functionality for visually hiding text within images, disguising it as repeated text.

- **nozwock:**
    - Implemented the encoder for the direct transcoder.
    - Added additional CLI commands.
    - Assumed responsibility for codebase refactoring and review efforts.
