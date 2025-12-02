# 📘 LZW Compression & Decompression (Python)

## 🔍 Overview
This project provides a simple Python implementation of the **Lempel–Ziv–Welch (LZW)** compression algorithm.  
LZW is a **lossless data compression** method that builds a dynamic dictionary of repeated patterns found in the input text.  
It replaces repeated sequences with shorter numeric codes to reduce storage size.

The project includes:

- `lzw_encode(text)` — Compresses a string into a list of integer codes.  
- `lzw_decode(code_list)` — Decompresses the code list back to the original string.

---

## 🚀 Features
- **Pure Python implementation**
- No external dependencies
- Works on ASCII character range (0–255)
- Includes full example (encode + decode)
- Clean and readable code structure

---

## 📄 Code Implementation

### 🔹 Encoding Function
```python
def lzw_encode(text):
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
```

---

### 🔹 Decoding Function
```python
def lzw_decode(code):
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256

    prev = code[0]
    result = dictionary[prev]

    for cur in code[1:]:
        if cur in dictionary:
            entry = dictionary[cur]
        else:
            entry = dictionary[prev] + dictionary[prev][0]

        result += entry
        dictionary[next_code] = dictionary[prev] + entry[0]
        next_code += 1

        prev = cur

    return result
```

---

## 🧪 Example Usage
```python
text = 'ABAABABAAAAA'
print("code :", lzw_encode(text))
print("decoded :", lzw_decode([65, 66, 65, 256, 259, 258, 258]))
```

### ✔ Output
```
code : [65, 66, 65, 256, 259, 258, 258]
decoded : ABAABABAAAAA
```

---

## 🧠 How LZW Works (Simplified)
1. Initialize a dictionary with all ASCII characters (0–255).  
2. Read characters and find the longest pattern already in the dictionary.  
3. Output its code.  
4. Add a new extended pattern to the dictionary.  
5. Continue until the entire text is processed.  
6. During decoding, rebuild the dictionary in the same order to perfectly reconstruct the original text.

---

## ⚠️ Notes & Limitations
- This implementation works on **ASCII text only**.  
  For Unicode (Arabic, Emoji, etc.), you must extend the dictionary or process the text as bytes.  
- The decoder assumes the code list is **not empty**.  
- The dictionary grows dynamically without a size limit (can grow large for long inputs).

---

## 📌 License
This project is free to use for learning, teaching, and research purposes.
