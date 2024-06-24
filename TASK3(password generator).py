import tkinter as tk
from tkinter import messagebox
import string
import random

def generate_password():
    try:
        length = int(length_entry.get())
        if length < 1:
            raise ValueError("Password length must be at least 1")
    except ValueError as e:
        messagebox.showerror("Invalid input", f"Error: {e}")
        return
    
    characters = ""
    if uppercase_var.get():
        characters += string.ascii_uppercase
    if lowercase_var.get():
        characters += string.ascii_lowercase
    if digits_var.get():
        characters += string.digits
    if punctuation_var.get():
        characters += string.punctuation
    
    if not characters:
        messagebox.showerror("Invalid input", "Please select at least one character set")
        return

    print(f"Selected characters: {characters}")
    
    password = ''.join(random.choice(characters) for _ in range(length))
    result_var.set(password)

root = tk.Tk()
root.title("Password Generator")
root.geometry("500x400")
root.configure(bg="#282c34")

title_font = ("Arial", 18, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")
result_font = ("Courier", 12, "bold")

title_label = tk.Label(root, text="Password Generator", font=title_font, bg="#61dafb", fg="#282c34", padx=20, pady=10)
title_label.pack(pady=20)

length_frame = tk.Frame(root, bg="#282c34")
length_frame.pack(pady=10)
length_label = tk.Label(length_frame, text="Enter password length:", font=label_font, bg="#282c34", fg="#ffffff")
length_label.pack(side=tk.LEFT, padx=10)
length_entry = tk.Entry(length_frame, font=label_font, width=5, bg="#ffffff", fg="#000000")
length_entry.pack(side=tk.LEFT)

options_frame = tk.Frame(root, bg="#282c34")
options_frame.pack(pady=10)
uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()
punctuation_var = tk.BooleanVar()

uppercase_check = tk.Checkbutton(options_frame, text="Include Uppercase Letters", variable=uppercase_var, font=label_font, bg="#282c34", fg="#ffffff", selectcolor="#00008b", activeforeground="#00008b")
lowercase_check = tk.Checkbutton(options_frame, text="Include Lowercase Letters", variable=lowercase_var, font=label_font, bg="#282c34", fg="#ffffff", selectcolor="#00008b", activeforeground="#00008b")
digits_check = tk.Checkbutton(options_frame, text="Include Digits", variable=digits_var, font=label_font, bg="#282c34", fg="#ffffff", selectcolor="#00008b", activeforeground="#00008b")
punctuation_check = tk.Checkbutton(options_frame, text="Include Punctuation", variable=punctuation_var, font=label_font, bg="#282c34", fg="#ffffff", selectcolor="#00008b", activeforeground="#00008b")

uppercase_check.pack(pady=2)
lowercase_check.pack(pady=2)
digits_check.pack(pady=2)
punctuation_check.pack(pady=2)

generate_button = tk.Button(root, text="Generate Password", command=generate_password, font=button_font, bg="#61dafb", fg="#282c34")
generate_button.pack(pady=20)

result_frame = tk.Frame(root, bg="#282c34")
result_frame.pack(pady=10)
result_label = tk.Label(result_frame, text="Generated Password:", font=label_font, bg="#282c34", fg="#ffffff")
result_label.pack(side=tk.LEFT, padx=10)
result_var = tk.StringVar()
result_display = tk.Entry(result_frame, textvariable=result_var, font=result_font, state="readonly", width=30, bg="#ffffff", fg="#000000")
result_display.pack(side=tk.LEFT)

root.mainloop()


