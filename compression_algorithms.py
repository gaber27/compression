import math
from utils import (
    run_length_encode,
    build_huffman_tree,
    huffman_encode,
    arithmetic_encode,
    encode_integer_with_golomb,
    lzw_encode
)

# Function to calculate compression metrics for a given algorithm
def all_algo_metric(text=None, algorithm_name=None, n=None, m=None):

    if algorithm_name == "RLE":
        # Run-Length Encoding
        encoded_text = run_length_encode(text)
        
        # Calculate bits before encoding
        if isinstance(text, str):
            bits_before = len(text) * 8
        if all(char.isdigit() for char in text):
            bits_before = len(text) * 1

        # Calculate bits after encoding
        max_length_encoded = max([count for _, count in encoded_text])
        if isinstance(text, str):
            bits_after = len(encoded_text) * (
                8 + math.ceil(math.log(max_length_encoded + 1, 2))
            )
        if all(char.isdigit() for char in text):
            bits_after = len(encoded_text) * (
                1 + math.ceil(math.log(max_length_encoded + 1, 2))
            )

        # Calculate compression ratio
        compression_ratio = bits_before / bits_after
        
        # Calculate character probabilities
        character_probabilities = {
            char: text.count(char) / len(text) for char in set(text)
        }
        
        # Calculate entropy
        entropy = -sum(
            prob * math.log2(prob) for prob in character_probabilities.values()
        )
        
        # Calculate average length
        average_length = sum(
            character_probabilities[char] * count for char, count in encoded_text
        )
        
        # Calculate efficiency
        efficiency = (entropy / average_length) * 100

        # Store results in dictionary
        results = {
            "Encoded text ": encoded_text,
            "Bits before encoding ": bits_before,
            "Bits after encoding ": bits_after,
            "Compression Ratio": compression_ratio,
            "Character Probabilities": character_probabilities,
            "Entropy": entropy,
            "Average Length": average_length,
            "Efficiency": efficiency,
        }
        return results

    elif algorithm_name == "Huffman":
        # Huffman Encoding
        huffman_tree = build_huffman_tree(text)
        encoded_text, encoding_dict = huffman_encode(text, huffman_tree)
        
        # Calculate bits before encoding
        bits_before = len(text) * 8  # Assuming 8 bits per character
        
        # Calculate bits after encoding
        bits_after = len(encoded_text)
        
        # Calculate compression ratio
        compression_ratio = bits_before / bits_after
        
        # Calculate character probabilities
        character_probabilities = {
            char: text.count(char) / len(text) for char in set(text)
        }
        
        # Calculate entropy
        entropy = -sum(
            prob * math.log2(prob) for prob in character_probabilities.values()
        )
        
        # Calculate average length
        average_length = sum(
            len(encoding_dict[char]) * prob
            for char, prob in character_probabilities.items()
        )
        
        # Calculate efficiency
        efficiency = (entropy / average_length) * 100

        # Store results in dictionary
        results = {
            "Encoded text ": encoded_text,
            "Encoded Dict": encoding_dict,
            "Bits before encoding ": bits_before,
            "Bits after encoding ": bits_after,
            "Compression Ratio": compression_ratio,
            "Character Probabilities": character_probabilities,
            "Entropy": entropy,
            "Average Length": average_length,
            "Efficiency": efficiency,
        }

        return results

    elif algorithm_name == "Arithmetic":
        # Arithmetic Encoding
        encoded_value, symbol_probs = arithmetic_encode(text)
        
        # Calculate bits before encoding
        bits_before = len(text) * 8
        
        # Calculate bits after encoding
        bits_after = int(math.ceil(math.log2(1 / min(symbol_probs.values())))) * len(text)
        
        # Calculate compression ratio
        compression_ratio = bits_before / bits_after
        
        # Calculate entropy
        entropy = -sum(prob * math.log2(prob) for prob in symbol_probs.values())
        
        # Calculate average length
        average_length = bits_after / len(text)
        
        # Calculate efficiency
        efficiency = (entropy / average_length) * 100

        # Store results in dictionary
        results = {
            "Encoded value ": encoded_value,
            "Bits before encoding ": bits_before,
            "Bits after encoding ": bits_after,
            "Compression Ratio": compression_ratio,
            "Character Probabilities": symbol_probs,
            "Entropy": entropy,
            "Average Length": average_length,
            "Efficiency": efficiency,
        }

        return results

    if algorithm_name == 'Golomb':
        # Golomb Encoding
        if n is not None and m is not None:  
            encoded_value = encode_integer_with_golomb(n, m)
            bits_before = n.bit_length()
            bits_after = len(encoded_value)
            compression_ratio = bits_before / bits_after if bits_after != 0 else float('inf')
            
            # Store results in dictionary
            results = {
                "Encoded Value": encoded_value,
                "Bits before encoding": bits_before,
                "Bits after encoding": bits_after,
                "Compression Ratio": compression_ratio
            }
            return results
        else:
            return "Error: Missing parameters for Golomb encoding."
    elif algorithm_name == "LZW":
        # LZW Encoding
        encoded_sequence = lzw_encode(text)
        bits_before = len(text) * 8
        bits_after = len(encoded_sequence) * 8
        compression_ratio = bits_before / bits_after
        character_probabilities = {
            char: text.count(char) / len(text) for char in set(text)
        }
        entropy = -sum(
            prob * math.log2(prob) for prob in character_probabilities.values()
        )
        # Calculate Average Length (L)
        average_length = bits_after / len(text)

        efficiency = (entropy / average_length) * 100
        results = {
            "Encoded Sequence ": encoded_sequence,
            "Bits before encoding ": bits_before,
            "Bits after encoding ": bits_after,
            "Compression Ratio": compression_ratio,
            "Character Probabilities": character_probabilities,
            "Entropy": entropy,
            "Average Length": average_length,
            "Efficiency": efficiency,
        }
        return results


def find_best_compression(text, n=None, m=None):
    results = {}

    # Huffman Encoding
    results["Huffman"] = all_algo_metric(text, "Huffman")

    # Run-Length Encoding
    results["RLE"] = all_algo_metric(text, "RLE")

    # Arithmetic Encoding
    results["Arithmetic"] = all_algo_metric(text, "Arithmetic")

    # Golomb Encoding
    results['Golomb'] = all_algo_metric(text, "Golomb", n, m)

    # LZW Encoding
    results["LZW"] = all_algo_metric(text, "LZW")

    # Determine the best based on compression ratio
    best_method = max(results, key=lambda k: results[k]["Compression Ratio"] if "Compression Ratio" in results[k] else 0)

    return best_method, results[best_method]

def compress_and_show(text, algorithm_name, n=None, m=None):
    results = all_algo_metric(text, algorithm_name, n, m)
    return results

def test_all_and_show_best(text, n=None, m=None):
    best_method, best_results = find_best_compression(text, n, m)

    display_text = f"Best Method: {best_method}\n" + "\n".join(
        f"{k}: {v}" for k, v in best_results.items()
    )

    return display_text
