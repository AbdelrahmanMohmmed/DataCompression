from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, OptionMenu, StringVar
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import sys
from tkinter.filedialog import asksaveasfilename

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from golom.My_golomb import golomb_encode_file, golomb_decode_file
from huffman.My_huffman import huffman_encode_with_tree, huffman_decode_with_tree
from LZW.My_LZW import lzw_encode, lzw_decode_file
from RLE.my_RLE import *
from quantizer.quantizer_photos import quantize_image, quantize_image_nonuniform


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"K:\programing\python\compression\Project\build\assets\frame0")
rle = RLE()


TEXT_METHODS = {
    "Huffman": (huffman_encode_with_tree, huffman_decode_with_tree),
    "LZW": (lzw_encode, lzw_decode_file),
    "Golomb": (golomb_encode_file, golomb_decode_file),
    "RLE":(rle.encoder,rle.decoder)
}

IMAGE_METHODS = {
    "Uniform Quantizer": quantize_image,
    "Nonuniform Quantizer": quantize_image_nonuniform
}

selected_file = None


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("408x487")
window.configure(bg="#CBCBCB")

canvas = Canvas(
    window,
    bg="#CBCBCB",
    height=487,
    width=408,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# --- Images ---
img_path = relative_to_assets("hacker.png")
hacker_image = Image.open(img_path)

hacker_image_raw = hacker_image.resize((352, 350), Image.LANCZOS)
hacker_img = ImageTk.PhotoImage(hacker_image_raw)

header_raw = hacker_image.resize((45, 36), Image.LANCZOS)
header_img = ImageTk.PhotoImage(header_raw)

# --- Background shapes ---
canvas.create_image(23, 69, anchor="nw", image=hacker_img)
canvas.create_rectangle(0, 9, 408, 69, fill="#5864B2", outline="")
canvas.create_text(50, 28, anchor="nw", text="Mega Compression", fill="#FFFFFF", font=("Inter", -12))

# ----------------------------
#       Dropdown variables
# ----------------------------
choice3_var = StringVar(value="Select method")
choice4_var = StringVar(value="Select mode")

dropdown3 = None
dropdown4 = None

# Toggle state for button 2
is_four_choices = True


# -------------------------------------------------
# Function: When button_1 is clicked
# -------------------------------------------------
def activate_dropdowns():
    global dropdown3, dropdown4

    # Hide original button_3
    button_3.place_forget()
    # Replace with OptionMenu (4 choices)
    choices_3 = ["Huffman", "LZW", "RLE", "Golomb"]
    dropdown3 = OptionMenu(window, choice3_var, *choices_3)
    dropdown3.place(x=137, y=139, width=133, height=36)

    # Hide original button_4
    button_4.place_forget()
    # Replace with OptionMenu (2 choices)
    choices_4 = ["Encode", "Decode"]
    dropdown4 = OptionMenu(window, choice4_var, *choices_4)
    dropdown4.place(x=137, y=204, width=133, height=36)


# -------------------------------------------------
# Function: Button 2 - Toggle dropdown3 choices
# -------------------------------------------------
def toggle_dropdown3():
    global is_four_choices, dropdown3

    # Make sure dropdown exists (user pressed button_1)
    if dropdown3 is None:
        print("Dropdown not active yet.")
        return

    # Remove old dropdown
    dropdown3.place_forget()

    # Toggle between 4 choices and 2 choices
    if is_four_choices:
        new_choices = ["Uniform Quantizer", "Nonuniform Quantizer"]
        is_four_choices = False
    else:
        new_choices = ["Huffman", "LZW", "RLE", "Golomb"]
        is_four_choices = True

    # Create new dropdown
    dropdown3 = OptionMenu(window, choice3_var, *new_choices)
    dropdown3.place(x=137, y=139, width=133, height=36)


# Function: When button_5 is clicked
def upload_file():
    global selected_file
    file_path = askopenfilename(filetypes=[("All files", "*.txt *.png *.jpg *.jpeg")])
    if file_path:
        selected_file = file_path
        print("User selected:", file_path)
    else:
        print("No file selected")

#save file
def save_output_file(data, default_name):
    file_path = asksaveasfilename(
        defaultextension=".txt",
        initialfile=default_name,
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(data))
        print("Saved to:", file_path)


#Compression
def run_compression():
    if selected_file is None:
        print("No file selected!")
        return

    method = choice3_var.get()
    mode = choice4_var.get()

    if method == "Select method" or mode == "Select mode":
        print("Please select method and mode")
        return

    file_ext = Path(selected_file).suffix.lower()

    # -------- TEXT FILE --------
    if file_ext == ".txt":
        if method not in TEXT_METHODS:
            print("Invalid method for text files")
            return

        encode_func, decode_func = TEXT_METHODS[method]

        with open(selected_file, "r", encoding="utf-8") as f:
            text = f.read()

        if mode == "Encode":
            result = encode_func(text)
            print("Encoded Text:\n", result)
            save_output_file(result, f"encoded_{method}.txt")


        elif mode == "Decode":
            result = decode_func(text)
            print("Decoded Text:\n", result)
            save_output_file(result, f"decoded_{method}.txt")

    # -------- IMAGE FILE --------
    elif file_ext in [".png", ".jpg", ".jpeg"]:
        if method not in IMAGE_METHODS:
            print("Invalid method for image files")
            return

        compress_func = IMAGE_METHODS[method]

        from PIL import Image
        import numpy as np

        img = Image.open(selected_file).convert("L")
        img_np = np.array(img)

        encoded, decoded = compress_func(img_np)
        print("Image compressed successfully")
        save_path = asksaveasfilename(
            defaultextension=".png",
            initialfile=f"compressed_{method}.png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )

        if save_path:
            Image.fromarray(decoded.astype("uint8")).save(save_path)
            print("Image saved to:", save_path)

    else:
        print("Unsupported file format!")


# -------------------------------------------------
# Buttons (keep your Figma assets)
# -------------------------------------------------

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=activate_dropdowns,
    relief="flat"
)
button_1.place(x=190, y=21, width=82, height=37)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=toggle_dropdown3,
    relief="flat"
)
button_2.place(x=295, y=21, width=77, height=37)

canvas.create_image(0, 17, anchor="nw", image=header_img)

# --- button_3 (will turn into list) ---
button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(x=137, y=139, width=133, height=36)

# --- button_4 (will turn into 2-choice list) ---
button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(x=137, y=204, width=133, height=36)

# --- button_5 (UPLOAD FILE) ---
button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=upload_file,
    relief="flat"
)
button_5.place(x=137, y=290, width=133, height=36)

# --- button_6 (normal) ---
button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=run_compression,
    relief="flat"
)
button_6.place(x=137, y=437, width=133, height=36)

window.resizable(False, False)
window.mainloop()
