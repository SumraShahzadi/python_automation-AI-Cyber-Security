import re
import tkinter as tk
from tkinter import messagebox

# ------------------ Password Validation Function ------------------
def check_password():
    try:
        password = entry.get()

        # ---------- SANITIZATION ----------
        password = password.strip()  # remove leading/trailing spaces

        # ---------- BASIC VALIDATION ----------
        if not password:
            raise ValueError("Password cannot be empty")

        if len(password) < 8 or len(password) > 100:
            raise ValueError("Password must be 8–100 characters long")

        # ---------- REGEX VALIDATION ----------
        if not re.search(r"[A-Z]", password):
            raise ValueError("Must contain at least ONE uppercase letter (A-Z)")

        if not re.search(r"[a-z]", password):
            raise ValueError("Must contain at least ONE lowercase letter (a-z)")

        if not re.search(r"[0-9]", password):
            raise ValueError("Must contain at least ONE number (0-9)")

        if not re.search(r"[!@#$%^&*()\[\]{}]", password):
            raise ValueError("Must contain at least ONE special character")

        if re.search(r"\s", password):
            raise ValueError("Password must not contain spaces")

        # ---------- FINAL STRONG PASSWORD ----------
        result_label.config(text="✅ Strong Password", fg="green")
        messagebox.showinfo(
            "Success",
            "Password accepted!\n\nThis password meets cybersecurity standards."
        )

    except ValueError as ve:
        result_label.config(text=f"❌ Weak: {ve}", fg="red")

    except Exception:
        result_label.config(text="❌ Error: Invalid input", fg="red")


# ------------------ GUI Window ------------------
root = tk.Tk()
root.title("🔐 Secure Password Strength Checker")
root.geometry("550x480")
root.config(bg="#0f172a")

# ------------------ Heading ------------------
title = tk.Label(
    root,
    text="🔐 Secure Password Strength Checker",
    font=("Arial", 18, "bold"),
    bg="#0f172a",
    fg="white"
)
title.pack(pady=15)

# ------------------ Guidelines ------------------
guidelines = tk.Label(
    root,
    text=(
        "Password Security Rules:\n"
        "✔ 8–100 characters\n"
        "✔ At least 1 uppercase letter\n"
        "✔ At least 1 lowercase letter\n"
        "✔ At least 1 number\n"
        "✔ At least 1 special character\n"
        "✔ No spaces allowed\n\n"
        "✔ Input Validation\n"
        "✔ Sanitization\n"
        "✔ Secure Logic (Day-2 Lab)"
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
    width=30,
    justify="center"
)
entry.pack(pady=15)

# ------------------ Button ------------------
check_btn = tk.Button(
    root,
    text="Check Password Security",
    font=("Arial", 13, "bold"),
    bg="#22c55e",
    fg="black",
    width=22,
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
    text="Python • Cybersecurity • Input Validation • Secure Logic",
    font=("Arial", 10),
    bg="#0f172a",
    fg="#94a3b8"
)
footer.pack(side="bottom", pady=10)

# ------------------ Run App ------------------
root.mainloop()


