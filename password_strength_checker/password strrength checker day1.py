# input =input("enter your number")
# special_characters=["!","@","#","$","%","^","&","*","(",")","_","+","-","=","{","}","[","]",":",";","'","\"","<",">",",",".","?","/"]
# if len(str(input))>8:
#      for i in special_characters:
#              if i in str(input):
#                     for i in str(input):
#                             if any(char.isupper() for char in str(input)):
#                                     print("strong password")
#                             else:
#                                    print("at least one upper case letter required")
                                     
#              else:
#                     print("at least one special character required")
# else: 
#     print("password must be at least 8 characters long")
# print("password is strong")


# password = input("Enter your password: ")

# special_characters = ["!","@","#","$","%","^","&","*","(",")","_","+","-","=",
#                       "{","}","[","]",":",";","'","\"","<",">",",",".","?","/"]

# # Length check
# if len(password) < 8:
#     print("Password must be at least 8 characters long")

# # Uppercase check
# elif not any(char.isupper() for char in password):
#     print("At least one uppercase letter required")

# # Special character check
# elif not any(char in special_characters for char in password):
#     print("At least one special character required")

# else:
#     print("Strong password")
# import re


    
import re
import tkinter as tk
from tkinter import messagebox

# ------------------ Password Check Function ------------------
def check_password():
    password = entry.get()

    if len(password) < 8:
        result_label.config(text="❌ Weak: Password too short", fg="red")

    elif not re.search("[A-Z]", password):
        result_label.config(text="❌ Weak: No uppercase letter", fg="red")

    elif not re.search("[0-9]", password):
        result_label.config(text="❌ Weak: No number", fg="red")

    elif not re.search(r"[!@#$%^&*()\[\]{}]", password):
        result_label.config(text="❌ Weak: No special character", fg="red")

    else:
        result_label.config(text="✅ Strong Password", fg="green")
        messagebox.showinfo("Success", "Your password is strong and secure!")

# ------------------ GUI Window ------------------
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("520x450")
root.config(bg="#0f172a")  # Dark blue (Cyber theme)

# ------------------ Heading ------------------
title = tk.Label(
    root,
    text="🔐 Password Strength Checker",
    font=("Arial", 18, "bold"),
    bg="#0f172a",
    fg="white"
)
title.pack(pady=15)

# ------------------ Guidelines ------------------
guidelines = tk.Label(
    root,
    text=(
        "Password Guidelines:\n"
        "✔ Minimum 8 characters\n"
        "✔ At least ONE uppercase letter (A-Z)\n"
        "✔ At least ONE number (0-9)\n"
        "✔ At least ONE special character (!@#$%^&*)\n\n"
        "This tool follows SOC & Security+ standards"
    ),
    justify="left",
    font=("Arial", 11),
    bg="#0f172a",
    fg="#cbd5e1"
)
guidelines.pack(pady=10)

# ------------------ Input Field ------------------
entry = tk.Entry(
    root,
    show="*",
    font=("Arial", 14),
    width=28,
    justify="center"
)
entry.pack(pady=15)

# ------------------ Button ------------------
check_btn = tk.Button(
    root,
    text="Check Password",
    font=("Arial", 13, "bold"),
    bg="#22c55e",
    fg="black",
    width=20,
    command=check_password
)
check_btn.pack(pady=10)

# ------------------ Result Label ------------------
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold"),
    bg="#0f172a"
)
result_label.pack(pady=20)

# ------------------ Footer ------------------
footer = tk.Label(
    root,
    text="Python • Cybersecurity • SOC Automation",
    font=("Arial", 10),
    bg="#0f172a",
    fg="#94a3b8"
)
footer.pack(side="bottom", pady=10)

# ------------------ Run App ------------------
root.mainloop()
