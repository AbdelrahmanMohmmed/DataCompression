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

# 📘 Uniform Scalar Quantization in Python

## 🔍 Overview
This project implements **Uniform Scalar Quantization**, one of the simplest and most widely used quantization techniques in digital signal processing.  
It includes:

- Building a **uniform quantization table**  
- Encoding samples into **quantization indices**  
- Decoding indices back to **reconstructed values**  
- Computing **Compression Ratio (CR)**  
- Computing **Mean Squared Error (MSE)**  

This implementation uses Python and NumPy and is suitable for educational purposes, image processing exercises, and signal compression simulations.

---

## 🚀 Features
- Fully implemented **uniform quantizer**
- Straightforward encoding & decoding functions
- Compression Ratio calculation
- Mean Squared Error (MSE) computation
- Clear, well-commented code structure
- Pure Python + NumPy

---

### 🔹 Main Program Execution
```python
if __name__ == '__main__':
    bit_size = 2
    orig_bits = 8

    pixels = [6, 15, 17, 60, 100, 90, 66, 59, 18, 3, 5, 16, 14, 67, 63, 2, 98, 92]

    encoded = uniform_quantizer_encode(pixels, bit_size, 128)
    decoded = uniform_quantizer_decode(encoded, bit_size, 128)

    cr = compute_compression_ratio(len(pixels), bit_size, orig_bits)
    mse = mean_squared_error(pixels, decoded)

    print("Encoded:", encoded)
    print("Decoded:", decoded)
    print(f"Compression Ratio: {cr:.2f} : 1")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
```

---

## 🧪 Example Output

```
Encoded: [0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 0 1 1]
Decoded: [ 8  8  8  8 40 40 40  8  8  8  8  8  8 40 40  8 40 40]
Compression Ratio: 4.00 : 1
Mean Squared Error (MSE): 776.4444
```

*(Output may vary slightly depending on quantization settings.)*

---

## 🧠 How Uniform Quantization Works (Simplified)

1. Divide the full amplitude range into **equal-sized intervals**.  
2. Each interval is assigned a **quantization index**.  
3. During encoding, each sample is replaced with its corresponding index.  
4. During decoding, each index is replaced by the interval’s **midpoint**.  
5. Compression occurs because fewer bits are used per sample.  
6. Reconstruction introduces **quantization error**, measured using MSE.

---

## ⚠️ Notes & Limitations

- Uniform quantization may produce large distortion for **non-uniform distributions**.  
- Assumes input samples fall within `[0, full_scale)`.  
- No overload handling (clipping) is performed.  
- More accurate results may require **µ-law** or **A-law** companding.

---

## 📌 License
This project is free to use for learning, teaching, and research purposes.
