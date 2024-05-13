# utils.py

import heapq
import math
from collections import Counter

# Running length encoding
def run_length_encode(text):
    encoded = []
    i = 0
    while i < len(text):
        # Count occurrences of a character
        count = 1
        while i + 1 < len(text) and text[i] == text[i + 1]:
            i += 1
            count += 1
        encoded.append((text[i], count))
        i += 1
    return encoded

# Huffman Tree
def build_huffman_tree(text):
    if not text:
        raise ValueError("Input text cannot be empty")
    frequency = Counter(text)
    heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = "1" + pair[1]
        for pair in hi[1:]:
            pair[1] = "0" + pair[1]

        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

# Huffman Encoding
def huffman_encode(text, huffman_tree):
    encoding_dict = {symbol: code[::-1] for symbol, code in huffman_tree}
    encoded_text = "".join(encoding_dict[char] for char in text)
    encoded_text = encoded_text[::-1]

    return encoded_text, encoding_dict

# Arithmetic encoding
def arithmetic_encode(text):
    symbols = sorted(set(text))
    symbol_probs = {symbol: 1 / len(symbols) for symbol in symbols}
    start, width = 0.0, 1.0

    for symbol in text:
        symbol_index = symbols.index(symbol)
        # Update the range
        start += sum(symbol_probs[s] for s in symbols[:symbol_index]) * width
        width *= symbol_probs[symbol]

    # Return the start of the final interval as the encoded value
    return start + width / 2, symbol_probs

# Golomb encoding
def golomb_encode(n, m):
    quotient = n // m
    remainder = n % m
    unary_code = '1' * quotient + '0'
    remainder_bits = int(math.ceil(math.log2(m)))
    binary_code = format(remainder, f'0{remainder_bits}b')
    return unary_code + binary_code

def encode_integer_with_golomb(n, m):
    return golomb_encode(n, m)

# LZW encoding
def lzw_encode(input_string):
    dictionary = {chr(i): i for i in range(128)}
    dict_size = 128

    p = ""  # Initialize current sequence
    encoded_output = []
    for c in input_string:
        pc = p + c
        if pc in dictionary:
            p = pc
        else:
            # Output the code for p
            encoded_output.append(dictionary[p])
            # Add pc to the dictionary
            dictionary[pc] = dict_size
            dict_size += 1
            p = c
    # Output code for p, if p is not empty
    if p:
        encoded_output.append(dictionary[p])
    return encoded_output
