import os
import hashlib
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread

# ================= HASH FUNCTION =================
def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


# ================= GLOBAL STORAGE =================
files = {}
monitoring = False


# ================= LOG FUNCTION =================
def log_change(file_path):
    with open("integrity_log.txt", "a") as log:
        log.write(f"[ALERT] {file_path} modified at {time.ctime()}\n")


# ================= FILE BROWSER =================
def browse_files():
    selected = filedialog.askopenfilenames()
    for file in selected:
        files[file] = calculate_hash(file)
        listbox.insert(tk.END, file)


# ================= MONITOR FUNCTION =================
def monitor_files():
    global monitoring
    while monitoring:
        for file, old_hash in files.items():
            if not os.path.exists(file):
                continue

            new_hash = calculate_hash(file)
            if new_hash != old_hash:
                files[file] = new_hash
                log_change(file)
                messagebox.showwarning("⚠️ File Modified",
                    f"File modified:\n{file}")
        time.sleep(5)


# ================= START MONITOR =================
def start_monitoring():
    global monitoring
    monitoring = True
    Thread(target=monitor_files, daemon=True).start()
    status_label.config(text="Monitoring started...", fg="lime")


# ================= STOP MONITOR =================
def stop_monitoring():
    global monitoring
    monitoring = False
    status_label.config(text="Monitoring stopped", fg="orange")


# ================= MALWARE SIMULATION =================
def simulate_malware():
    if not files:
        messagebox.showerror("Error", "No file selected!")
        return

    file = list(files.keys())[0]
    with open(file, "a") as f:
        f.write("\n# MALWARE INJECTED")
    messagebox.showinfo("Simulation", "Malware simulation executed!")


# ================= DARK THEME GUI =================
root = tk.Tk()
root.title("🔐 Advanced File Integrity Monitor")
root.geometry("700x450")
root.configure(bg="#121212")

title = tk.Label(root, text="Advanced File Integrity Monitoring Tool",
                 bg="#121212", fg="cyan", font=("Consolas", 16, "bold"))
title.pack(pady=10)

browse_btn = tk.Button(root, text="📂 Add Files",
                       command=browse_files, width=20)
browse_btn.pack(pady=5)

listbox = tk.Listbox(root, width=90, height=8, bg="#1e1e1e", fg="white")
listbox.pack(pady=10)

start_btn = tk.Button(root, text="▶ Start Monitoring",
                      command=start_monitoring, width=20)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="⏹ Stop Monitoring",
                     command=stop_monitoring, width=20)
stop_btn.pack(pady=5)

simulate_btn = tk.Button(root, text="🧪 Malware Simulation",
                         command=simulate_malware, width=20)
simulate_btn.pack(pady=10)

status_label = tk.Label(root, text="Status: Idle",
                        bg="#121212", fg="white", font=("Arial", 12))
status_label.pack(pady=10)

root.mainloop()




.

# 🔐 Advanced File Integrity Monitoring Tool
# Python | Tkinter | Cybersecurity Automation
# 📌 Project Overview

# This project is a GUI-based File Integrity Monitoring (FIM) tool developed using Python and Tkinter.
# It detects unauthorized file modifications using SHA-256 cryptographic hashing.

# The tool is designed for cybersecurity learning, malware detection demonstration, and SOC-style monitoring.

# 🎯 Objectives

# Monitor files for unauthorized changes

# Detect tampering using cryptographic hashes

# Log integrity violations for forensic analysis

# Demonstrate malware behavior safely

# Provide a professional cybersecurity GUI

# 🚀 Features

# ✔ 🔁 Auto monitoring every 5 seconds
# ✔ 📂 Monitor multiple files simultaneously
# ✔ 🔐 Uses SHA-256 hashing
# ✔ 📄 Logs all modifications to integrity_log.txt
# ✔ 🔔 Popup alerts on file modification
# ✔ 🧪 Malware simulation for testing
# ✔ 🎨 Dark theme cybersecurity UI
# ✔ 🖥️ User-friendly GUI (Tkinter)

# 🛠️ Technologies Used

# Python 3

# Tkinter (GUI)

# hashlib (SHA-256 hashing)

# threading (background monitoring)

# os, time (file & time handling)

# 📂 Project Structure
# Advanced_File_Integrity_Monitor/
# │
# ├── file_integrity_monitor.py
# ├── integrity_log.txt
# ├── README.md

# ⚙️ How It Works

# User selects one or more files

# Tool generates baseline SHA-256 hashes

# Monitoring runs every 5 seconds

# If a file changes:

# Hash mismatch detected

# Alert popup shown

# Change logged in integrity_log.txt

# Malware simulation modifies a file intentionally

# ▶️ How to Run
# Step 1: Install Python

# Make sure Python 3 is installed:

# python --version

# Step 2: Run the Tool
# python file_integrity_monitor.py

# 🧪 Malware Simulation (Educational)

# The Malware Simulation button appends malicious text to a monitored file to demonstrate how integrity monitoring detects attacks.

# ⚠️ This is safe and for learning only.

# 📄 Log File Example
# [ALERT] C:\Users\...\important.txt modified at Tue Feb 11 12:45:22 2026


# Used for:

# Digital forensics

# Incident response

# Security audits

# 🧠 Cybersecurity Concepts Demonstrated

# File Integrity Monitoring (FIM)

# Cryptographic hashing

# Malware detection logic

# Endpoint security

# SOC alerting workflow

# 🎓 Viva / Exam Explanation (Short)

# “This tool uses SHA-256 hashing to ensure file integrity.
# Any modification changes the hash value, which triggers alerts and logging, similar to enterprise security tools like Wazuh and Tripwire.”

# 🔮 Future Enhancements

# Directory monitoring

# Email alerts

# Hash algorithm selector

# JSON-based SIEM logs

# Windows/Linux service mode

# 👩‍💻 Author

# Sumra Shahzadi
# BS Cybersecurity
# Python & Cybersecurity Automation Enthusiast

# 📜 License

# This project is for educational and academic use.