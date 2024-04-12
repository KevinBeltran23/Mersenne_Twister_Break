import binascii
import base64
import re
from collections import Counter

ALPHABET_SIZE = 26


# convert a series of bytes into a hexadecimal ascii representation of those bytes
def bytes_to_hex_ascii(input_bytes):
    return binascii.hexlify(input_bytes).decode('ascii')


# convert a hexadecimal ascii representation into the series of bytes it represents
def hex_ascii_to_bytes(hex_ascii_string):
    return binascii.unhexlify(hex_ascii_string)


# convert an integer into a base 64 ascii representation of that integer
def int_to_base64_first_n_bits(input_int, n):
    return base64.b64encode(input_int.to_bytes(n // 8, byteorder='big'))


def int_to_bytes(num):
    # Convert the integer to bytes using the big-endian byte order and 4 bytes length
    return num.to_bytes(4, byteorder='big')

def bytes_to_int(byte_array):
    result = 0
    for byte in byte_array:
        result = (result << 8) + byte
    return result


# convert a series of bytes into a base 64 ascii representation of those bytes
def bytes_to_base64_ascii(input_bytes):
    return base64.b64encode(input_bytes).decode('ascii')


# convert a base 64 ascii representation into the series of bytes it represents
def base64_to_bytes(base64_string):
    return base64.b64decode(base64_string)


def bytes_to_ascii(byte_data):
    return [byte for byte in byte_data]


def score_english_text(text):
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    expected_frequencies = {
        'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015,
        'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749,
        'o': 7.507, 'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056, 'u': 2.758,
        'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074,
        'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 'F': 2.228, 'G': 2.015,
        'H': 6.094, 'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749,
        'O': 7.507, 'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056, 'U': 2.758,
        'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974, 'Z': 0.074
    }
    # Remove non-alphabetic characters and convert to lowercase
    cleaned_text = ''.join(char.lower() for char in text if char.isalpha())
    # Check if the cleaned text is empty or has only one character
    if len(cleaned_text) <= 0:
        return float('inf')

    counter = Counter(text)
    # get the frequency of each letter
    # get the sum of the difference in frequencies
    # normalize them
    return sum([abs(counter.get(letter, 0) * 100 / len(text) - expected_frequencies[letter]) for letter in ALPHABET]) / ALPHABET_SIZE


def score_english_text_top_n(text, top_n=26):
    expected_frequencies = {
        'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015,
        'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749,
        'o': 7.507, 'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056, 'u': 2.758,
        'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074,
        'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 'F': 2.228, 'G': 2.015,
        'H': 6.094, 'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749,
        'O': 7.507, 'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056, 'U': 2.758,
        'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974, 'Z': 0.074
    }
    # Remove non-alphabetic characters and convert to lowercase
    cleaned_text = ''.join(char.lower() for char in text if char.isalpha())
    # Check if there is any english at all
    if len(cleaned_text) <= 0:
        return float('inf')

    counter = Counter(text)
    # get the frequency of each letter
    # get the sum of the difference in frequencies
    # normalize them
    top_letters = [letter for letter, l in counter.most_common(top_n) if letter.isalpha()]
    return sum([abs(counter.get(letter, 0) * 100 / len(text) - expected_frequencies[letter]) for letter in top_letters]) / top_n


def xor_byte_string(input_bytes, key_bytes):
    # Ensure the key is repeated or truncated to match the length of the input string
    expanded_key = (key_bytes * (len(input_bytes) // len(key_bytes) + 1))[:len(input_bytes)]

    # Perform the XOR operation
    return bytes(x ^ k for x, k in zip(input_bytes, expanded_key))


def single_byte_xor_helper(byte_string, key):
    key_bytes = bytes([key])

    # XOR the bytes with the key
    decrypted_text = xor_byte_string(byte_string, key_bytes)

    # Convert it to an ASCII string for English scoring
    decrypted_text_str = decrypted_text.decode('utf-8', errors='ignore')

    # Score the decrypted text
    score = score_english_text(decrypted_text_str)

    return decrypted_text_str, score, bytes_to_ascii(key_bytes), key_bytes


def vigenere_single_byte_helper(byte_string, key):
    # XOR the bytes with the key
    decrypted_text = vigenere_decrypt(byte_string, key)

    # Score the decrypted text
    score = score_english_text_top_n(decrypted_text)

    return decrypted_text, score, bytes_to_ascii(key), key


def single_byte_xor_top_n_keys(block, b):
    results = []
    top_keys = []
    # Iterate through possible single-byte keys (0-255)
    for key in range(256):
        # XOR the block with the single-byte key
        results.append(single_byte_xor_helper(block, key))
    sorted_results = sorted(results, key=lambda l: l[1])[:b]
    # Extract the values from index 3, the keys
    for result in sorted_results:
        top_keys.append(result[3])
    return top_keys


def vigenere_single_byte_top_n_keys(block, b):
    results = []
    top_keys = []
    # Iterate through all possible single-byte keys (65-90)
    for key in range(65, 91):
        # shift the block with the single-byte key
        results.append(vigenere_single_byte_helper(block, chr(key)))
    sorted_results = sorted(results, key=lambda l: l[1])[:b]
    # Extract the values from index 3, the keys
    for result in sorted_results:
        top_keys.append(result[3])
    return top_keys


# tested - works fine
def vigenere_decrypt(ciphertext, key):
    decrypted_text = ''
    key = key.upper()
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            decrypted_text += shift_char(key, len(key), char, i)
        else:
            decrypted_text += char
    return decrypted_text


# tested - works fine
def shift_char(key, key_length, char, i):
    # get the ascii value of the current index of the key
    shift = ord(key[i % key_length].upper())
    # shift the current char of the message
    decrypted_char = chr((ord(char.upper()) - shift) % 26 + ord('A'))
    return decrypted_char.lower() if char.islower() else decrypted_char


def blocks_of_every_n_index(n, keyLength, message):
    letters = re.compile('[^A-Z]')
    message = letters.sub('', message)
    letters = []

    while n - 1 < len(message):
        letters.append(message[n - 1])
        n += keyLength
    return ''.join(letters)


def index_of_coincidence(text):
    text = text.lower()

    letter_counts = [text.count(chr(i)) for i in range(ord('a'), ord('z') + 1)]
    ic = sum(count * (count - 1) for count in letter_counts) / (len(text) * (len(text) - 1) / ALPHABET_SIZE)

    return ic


def vigenere_period(text, max_key_length=26):
    best_ic = 0
    smallest_key_length = 1

    for key_length in range(1, max_key_length + 1):
        chunks = [text[i::key_length] for i in range(key_length)]
        average_ic = sum(index_of_coincidence(chunk) for chunk in chunks) / key_length

        if average_ic > best_ic:
            best_ic = average_ic
            smallest_key_length = key_length

    return smallest_key_length
