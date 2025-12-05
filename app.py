import streamlit as st
from pathlib import Path
from golom.My_golomb import golomb_encode, golomb_decode
from huffman.My_huffman import my_huffman_encode, my_huffman_decode
from LZW.My_LZW import lzw_encode, lzw_decode
from quantizer.quantizer_photos import *
from RLE.my_RLE import rle_encoder
from arthimatic.My_arthritic import  make_interval


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

    # text file
    if file_extension == ".txt":
        st.subheader("Text Compression")
        technique = st.selectbox("Choose Compression Technique", list(TEXT_METHODS.keys()))

        text_data = uploaded_file.read().decode("utf-8")

        if st.button("Compress"):
            compress_func = TEXT_METHODS[technique]
            result = compress_func(text_data)

            st.success(f"{technique} compression completed!")
            st.write("Compressed Output:")
            st.code(result)

    # image files
    elif file_extension in [".png", ".jpg", ".jpeg"]:
        st.subheader("Image Compression")

        technique = st.selectbox("Choose Compression Technique", list(IMAGE_METHODS.keys()))

        # Load using your function
        image_matrix, pil_image = load_image_as_matrix(uploaded_file)

        st.image(pil_image, caption="Uploaded Image", use_container_width=True)

        if st.button("Compress"):
            compress_func = IMAGE_METHODS[technique]
            encode, decode = compress_func(image_matrix)

            st.success(f"{technique} compression completed!")
            st.write("Decoded Image:")
            st.image(decode.astype("uint8"))

    else:
        st.error("Unsupported file format!")
