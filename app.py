import streamlit as st
from pathlib import Path
from golom.My_golomb import golomb_encode, golomb_decode
from huffman.My_huffman import my_huffman_encode, my_huffman_decode
from LZW.My_LZW import lzw_encode, lzw_decode
from quantizer.quantizer_photos import *
from RLE.my_RLE import rle_encoder
from arthimatic.My_arthritic import make_interval
from io import BytesIO
from PIL import Image
import numpy as np


TEXT_METHODS = {
    "LZW": lzw_encode,
    "RLE": rle_encoder.encoder,
    "Arithmetic": make_interval,
    "Golomb": golomb_encode,
    "Huffman": my_huffman_encode
}

IMAGE_METHODS = {
    "Uniform_Quantizer": quantize_image,
    "NonUniform_Quantizer": quantize_image_nonuniform
}


# App
st.title("File Compression Tool")

uploaded_file = st.file_uploader(
    "Upload an Image or Text File",
    type=["txt", "png", "jpg", "jpeg"]
)

if uploaded_file:
    file_extension = Path(uploaded_file.name).suffix.lower()

    # ---------------------------------------------------
    #                 TEXT COMPRESSION
    # ---------------------------------------------------
    if file_extension == ".txt":
        st.subheader("Text Compression")

        technique = st.selectbox("Choose Compression Technique", list(TEXT_METHODS.keys()))

        text_data = uploaded_file.read().decode("utf-8")
        original_size = len(text_data.encode("utf-8"))

        st.write(f" **Original Size:** {original_size} bytes")

        if st.button("Compress"):
            compress_func = TEXT_METHODS[technique]
            encoded_text = compress_func(text_data)

            # encoded size in bytes
            encoded_size = len(str(encoded_text).encode("utf-8"))
            ratio = original_size / encoded_size if encoded_size != 0 else 0

            st.success(f"{technique} compression completed!")

            st.write("### Encoded Output:")
            st.code(encoded_text)

            # ---- Sizes ----
            st.write(f" **Compressed Size:** {encoded_size} bytes")
            st.write(f" **Compression Ratio:** {ratio:.2f}x smaller")

            # ---- Download Encoded Text ----
            st.download_button(
                label="Download Encoded File",
                data=str(encoded_text),
                file_name=f"compressed_{technique}.txt",
                mime="text/plain"
            )

    # ---------------------------------------------------
    #               IMAGE COMPRESSION
    # ---------------------------------------------------
    elif file_extension in [".png", ".jpg", ".jpeg"]:
        st.subheader("Image Compression")

        technique = st.selectbox("Choose Compression Technique", list(IMAGE_METHODS.keys()))

        # Load using your function
        image_matrix, pil_image = load_image_as_matrix(uploaded_file)

        st.image(pil_image, caption="Uploaded Image", use_container_width=True)

        # original file size
        uploaded_file.seek(0)
        original_image_bytes = uploaded_file.read()
        original_size = len(original_image_bytes)

        st.write(f" **Original Image Size:** {original_size} bytes")

        if st.button("Compress"):
            compress_func = IMAGE_METHODS[technique]
            encoded, decoded = compress_func(image_matrix)

            # Estimate encoded size
            if isinstance(encoded, np.ndarray):
                encoded_size = encoded.nbytes
            else:
                encoded_size = len(str(encoded).encode("utf-8"))

            ratio = original_size / encoded_size if encoded_size != 0 else 0

            st.success(f"{technique} compression completed!")

            # ---------------------------
            #       Show Encoded Data
            # ---------------------------
            st.write("### Encoded Representation:")
            st.code(str(encoded))

            # size info
            st.write(f" **Compressed Size:** {encoded_size} bytes")
            st.write(f" **Compression Ratio:** {ratio:.2f}x smaller")

            # ---------------------------
            #       Show Decoded Image
            # ---------------------------
            decoded_image_uint8 = decoded.astype("uint8")
            st.image(decoded_image_uint8, caption="Decoded / Compressed Image", use_container_width=True)

            # ---------------------------
            #    Download Decoded Image
            # ---------------------------
            img_buffer = BytesIO()
            Image.fromarray(decoded_image_uint8).save(img_buffer, format="PNG")
            img_buffer.seek(0)

            st.download_button(
                label="Download Compressed Image",
                data=img_buffer,
                file_name=f"compressed_{technique}.png",
                mime="image/png"
            )

    else:
        st.error("Unsupported file format!")
