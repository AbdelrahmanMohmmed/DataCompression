def lzw_encode(text):
    # Initialize dictionary with single characters
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256

    current = ""
    result = []

    for c in text:
        combined = current + c
        if combined in dictionary:
            current = combined
        else:
            result.append(dictionary[current])
            dictionary[combined] = next_code
            next_code += 1
            current = c

    if current:
        result.append(dictionary[current])

    return result


def lzw_decode(code):
    # Initialize dictionary with single characters
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256

    prev = code[0]
    result = dictionary[prev]

    for cur in code[1:]:
        if cur in dictionary:
            entry = dictionary[cur]
        else:
            # Special case for codes not yet in the dictionary
            entry = dictionary[prev] + dictionary[prev][0]

        result += entry
        dictionary[next_code] = dictionary[prev] + entry[0]
        next_code += 1

        prev = cur

    return result
