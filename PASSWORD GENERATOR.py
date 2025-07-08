import customtkinter
import random
import string
import pyperclip

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

def generate_password():
    length_text = length_entry.get()
    if not length_text.isdigit():
        result_label.configure(text="Enter a valid number")
        strength_label.configure(text="")
        return

    length = int(length_text)
    if length < 4:
        result_label.configure(text="Minimum length is 4")
        strength_label.configure(text="")
        return

    chars = ""
    if upper_var.get():
        chars += string.ascii_uppercase
    if lower_var.get():
        chars += string.ascii_lowercase
    if digit_var.get():
        chars += string.digits
    if symbol_var.get():
        chars += string.punctuation

    if not chars:
        result_label.configure(text="Select at least one option")
        strength_label.configure(text="")
        return

    excluded = exclude_entry.get()
    chars = ''.join(c for c in chars if c not in excluded)

    password = ''.join(random.choice(chars) for _ in range(length))
    result_label.configure(text=password)
    show_strength(password)

def copy_password():
    pyperclip.copy(result_label.cget("text"))

def update_length_display(event=None):
    text = length_entry.get()
    if text.isdigit():
        length_display.configure(text=f"Length: {text}")
    else:
        length_display.configure(text="")

def show_strength(password):
    length = len(password)
    types = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ])

    if length >= 12 and types >= 3:
        strength_label.configure(text="Strength: Strong", text_color="green")
    elif length >= 8 and types >= 2:
        strength_label.configure(text="Strength: Medium", text_color="yellow")
    else:
        strength_label.configure(text="Strength: Weak", text_color="red")

app = customtkinter.CTk()
app.title("Password Generator")
app.geometry("500x400")
app.resizable(False, False)


customtkinter.CTkLabel(app, text="🔐 Secure Password Generator", font=("Arial", 18, "bold")).pack(pady=10)


result_label = customtkinter.CTkLabel(app, text="", font=("Arial", 15, "bold"), text_color="lightgreen", wraplength=400)
result_label.pack(pady=5)

strength_label = customtkinter.CTkLabel(app, text="", font=("Arial", 13, "bold"))
strength_label.pack(pady=3)


main_frame = customtkinter.CTkFrame(app)
main_frame.pack(pady=10, padx=10, fill="x", expand=True)

left_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

customtkinter.CTkLabel(left_frame, text="Password Length:", font=("Arial", 13)).pack(anchor="w")
length_entry = customtkinter.CTkEntry(left_frame, width=100)
length_entry.insert(0, "16")
length_entry.pack(pady=3)
length_entry.bind("<KeyRelease>", update_length_display)

length_display = customtkinter.CTkLabel(left_frame, text="Length: 16", font=("Arial", 12))
length_display.pack(pady=2)

customtkinter.CTkLabel(left_frame, text="Exclude Characters:", font=("Arial", 13)).pack(anchor="w", pady=(10, 2))
exclude_entry = customtkinter.CTkEntry(left_frame, width=140)
exclude_entry.pack()

right_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

upper_var = customtkinter.BooleanVar(value=False)
lower_var = customtkinter.BooleanVar(value=False)  
digit_var = customtkinter.BooleanVar(value=False)
symbol_var = customtkinter.BooleanVar(value=False)  


customtkinter.CTkCheckBox(right_frame, text="Uppercase Letters", variable=upper_var).pack(anchor="w", pady=2)
customtkinter.CTkCheckBox(right_frame, text="Lowercase Letters", variable=lower_var).pack(anchor="w", pady=2)
customtkinter.CTkCheckBox(right_frame, text="Numbers", variable=digit_var).pack(anchor="w", pady=2)
customtkinter.CTkCheckBox(right_frame, text="Symbols (!@#)", variable=symbol_var).pack(anchor="w", pady=2)

button_row = customtkinter.CTkFrame(app, fg_color="transparent")
button_row.pack(pady=15)

customtkinter.CTkButton(button_row, text="Generate Password", command=generate_password, width=180).pack(side="left", padx=10)
customtkinter.CTkButton(button_row, text="Copy to Clipboard", command=copy_password, width=180).pack(side="left", padx=10)

app.mainloop()
