import socket
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread

scanning = False  # Global scan flag

# ------------------ SERVICE NAME FUNCTION ------------------
def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

# ------------------ BANNER GRABBING ------------------
def grab_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        return banner if banner else "No banner"
    except:
        return "No banner"

# ------------------ OS DETECTION ------------------
def detect_os(banner):
    banner = banner.lower()
    if "linux" in banner or "ubuntu" in banner:
        return "Linux"
    elif "windows" in banner or "microsoft" in banner:
        return "Windows"
    return "Unknown"

# ------------------ SCAN THREAD ------------------
def scan_ports(target):
    global scanning

    results.delete(*results.get_children())

    for port in range(1, 1025):
        if not scanning:
            break

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))

        if result == 0:
            service = get_service(port)
            banner = grab_banner(target, port)
            os_guess = detect_os(banner)

            results.insert("", "end",
                values=(port, service, "OPEN", banner, os_guess),
                tags=("open",)
            )
        else:
            results.insert("", "end",
                values=(port, "-", "CLOSED", "-", "-"),
                tags=("closed",)
            )

        s.close()
        root.update_idletasks()

    scanning = False
    start_btn.config(bg="green", text="Start Scan")
    stop_btn.config(state="disabled")

# ------------------ START SCAN ------------------
def start_scan():
    global scanning

    target = ip_entry.get()
    if not target:
        messagebox.showerror("Error", "Enter Target IP")
        return

    scanning = True
    start_btn.config(bg="red", text="Scanning...")
    stop_btn.config(state="normal")

    thread = Thread(target=scan_ports, args=(target,))
    thread.daemon = True
    thread.start()

# ------------------ STOP SCAN ------------------
def stop_scan():
    global scanning
    scanning = False

# ------------------ GUI SETUP ------------------
root = tk.Tk()
root.title("Advanced GUI Port Scanner")
root.geometry("1000x500")

# IP INPUT
tk.Label(root, text="Target IP:", font=("Arial", 11)).pack(pady=5)
ip_entry = tk.Entry(root, width=30)
ip_entry.pack()

# BUTTONS
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

start_btn = tk.Button(btn_frame, text="Start Scan", bg="green",
                      fg="white", width=15, command=start_scan)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(btn_frame, text="Stop Scan", bg="gray",
                     fg="white", width=15, state="disabled", command=stop_scan)
stop_btn.grid(row=0, column=1, padx=5)

# TABLE
columns = ("Port", "Service", "Status", "Banner", "OS Guess")
results = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    results.heading(col, text=col)
    results.column(col, width=180)

results.pack(expand=True, fill="both")

# COLOR TAGS
results.tag_configure("open", background="#b6ffb6")     # Green
results.tag_configure("closed", background="#ffd6d6")   # Light Red

root.mainloop()
