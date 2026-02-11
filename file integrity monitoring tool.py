# import os
# print("hello")
# print(os.getcwd())
# print("abc")
# print(os.listdir())
# print(os.makedirs("test1lab"))
# print(os.listdir())
# import os
# import sys
# import hashlib

# print(sys.version)
# print(sys.platform)

# # Move to script directory
# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# print("hello")
# print(os.getcwd())
# print("abc")

# print(os.listdir())

# os.makedirs("test1lab", exist_ok=True)

# print(os.listdir())
# print(__file__)
# import os
# import stat

# file_path = "example.txt"
# permissions = os.stat("d:\AI Automation for cyber security\AI_Automation_in Cyber Security_Labs\file integrity monitoring tool.py")

# print(stat.filemode(permissions.st_mode))
#  def checksum(file):
#    hash=hashlib.sha256(filepath)
#    with open("filepath",rb) as f
#      while true:
#        data=f.read(4096)
#        if not data:
#           break
#        sha256.update(data)
#     return sha256.hexdigest()
import os
import sys
import hashlib
import stat

# ---------------- SYSTEM INFO ----------------
print("Python Version:", sys.version)
print("Operating System:", sys.platform)

# ---------------- MOVE TO SCRIPT DIRECTORY ----------------
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("\nCurrent Working Directory:")
print(os.getcwd())

print("\nDirectory Contents:")
print(os.listdir())

# ---------------- CREATE FOLDER SAFELY ----------------
os.makedirs("test1lab", exist_ok=True)

print("\nDirectory After Creating test1lab:")
print(os.listdir())

# ---------------- FILE PATH INFO ----------------
print("\nScript File Path:")
print(__file__)

# ---------------- FILE PERMISSIONS ----------------
permissions = os.stat(__file__)
print("\nFile Permissions:")
print(stat.filemode(permissions.st_mode))

# ---------------- FILE HASH / CHECKSUM ----------------
def checksum(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()

# ---------------- HASH OUTPUT ----------------
hash_value = checksum(__file__)
print("\nSHA256 Checksum of Script:")
print(hash_value)

# import os
# import hashlib
# import sys

# # ---------------- STEP 1: HASH FUNCTION (DEFINITION) ----------------
# def calculate_hash(file_path):
#     """
#     This function calculates SHA-256 hash of a file
#     """
#     sha256 = hashlib.sha256()   # Create SHA-256 hash object

#     with open(file_path, "rb") as file:   # Open file in binary mode
#         while True:
#             data = file.read(4096)        # Read file in chunks
#             if not data:
#                 break
#             sha256.update(data)           # Update hash with data chunk

#     return sha256.hexdigest()              # Return final hash value


# # ================= MAIN PROGRAM STARTS HERE =================

# # ---------------- STEP 2: FILE TO MONITOR ----------------
# file_to_monitor = __file__

# # ---------------- STEP 3: CHECK IF FILE EXISTS ----------------
# if not os.path.exists(file_to_monitor):
#     print("❌ File not found!")
#     sys.exit()

# # ---------------- STEP 4: FUNCTION CALL (FIRST TIME) ----------------
# # Calling calculate_hash() to get ORIGINAL hash
# original_hash = calculate_hash(file_to_monitor)

# print("🔐 Original Hash:", original_hash)

# # ---------------- STEP 5: WAIT FOR USER TO MODIFY FILE ----------------
# input("\n✏️ Modify the file and press Enter to continue...")

# # ---------------- STEP 6: FUNCTION CALL (SECOND TIME) ----------------
# # Calling calculate_hash() again to get NEW hash
# new_hash = calculate_hash(file_to_monitor)

# print("🔐 New Hash:", new_hash)

# # ---------------- STEP 7: COMPARE HASHES ----------------
# if original_hash == new_hash:
#     print("\n✅ File is SAFE. No changes detected.")
# else:
#     print("\n⚠️ WARNING! File has been modified.")
import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

# ---------------- HASH FUNCTION ----------------
def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


# ---------------- GLOBAL VARIABLES ----------------
selected_file = ""
original_hash = ""


# ---------------- BROWSE FILE ----------------
def browse_file():
    global selected_file, original_hash

    selected_file = filedialog.askopenfilename()
    if selected_file:
        file_label.config(text=selected_file)
        original_hash = calculate_hash(selected_file)
        hash_label.config(text=original_hash)
        status_label.config(text="Baseline hash generated", fg="blue")


# ---------------- CHECK INTEGRITY ----------------
def check_integrity():
    global selected_file, original_hash

    if not selected_file:
        messagebox.showerror("Error", "No file selected!")
        return

    new_hash = calculate_hash(selected_file)

    if new_hash == original_hash:
        status_label.config(text="✅ File is SAFE (No Change)", fg="green")
    else:
        status_label.config(text="⚠️ File MODIFIED!", fg="red")


# ---------------- GUI WINDOW ----------------
root = tk.Tk()
root.title("🔐 File Integrity Monitoring Tool")
root.geometry("600x350")
root.resizable(False, False)

# ---------------- UI ELEMENTS ----------------
title = tk.Label(root, text="File Integrity Monitoring Tool", font=("Arial", 16, "bold"))
title.pack(pady=10)

browse_btn = tk.Button(root, text="📂 Browse File", command=browse_file, width=20)
browse_btn.pack(pady=5)

file_label = tk.Label(root, text="No file selected", wraplength=550)
file_label.pack(pady=5)

hash_title = tk.Label(root, text="Original SHA-256 Hash:", font=("Arial", 10, "bold"))
hash_title.pack(pady=5)

hash_label = tk.Label(root, text="-----", wraplength=550)
hash_label.pack(pady=5)

check_btn = tk.Button(root, text="🔍 Check Integrity", command=check_integrity, width=20)
check_btn.pack(pady=15)

status_label = tk.Label(root, text="Status: Waiting...", font=("Arial", 12))
status_label.pack(pady=10)

# ---------------- RUN GUI ----------------
root.mainloop()




