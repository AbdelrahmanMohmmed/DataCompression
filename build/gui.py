from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, OptionMenu, StringVar
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"K:\programing\python\compression\Project\build\assets\frame0")

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
    choices_3 = ["Huffman", "LZW", "Arithmetic Coding", "Golomb"]
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
        new_choices = ["Huffman", "LZW", "Arithmetic Coding", "Golomb"]
        is_four_choices = True

    # Create new dropdown
    dropdown3 = OptionMenu(window, choice3_var, *new_choices)
    dropdown3.place(x=137, y=139, width=133, height=36)


# -------------------------------------------------
# Function: When button_5 is clicked
# -------------------------------------------------
def upload_file():
    file_path = askopenfilename()
    if file_path:
        print("User selected:", file_path)
    else:
        print("No file selected")


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
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(x=137, y=437, width=133, height=36)

window.resizable(False, False)
window.mainloop()
