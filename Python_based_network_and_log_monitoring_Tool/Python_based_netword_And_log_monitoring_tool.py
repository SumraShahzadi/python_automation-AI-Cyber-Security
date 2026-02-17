import socket
import threading
import os
import re
import time
import csv
import datetime
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# -------- EVTX SUPPORT --------
try:
    from Evtx.Evtx import Evtx
    EVTX_AVAILABLE = True
except:
    EVTX_AVAILABLE = False

monitoring = False
CSV_FILE = "siem_alerts.csv"
open_ports = []

# -------- SOUND ALERT --------
def alert_sound():
    try:
        import winsound
        winsound.Beep(1200, 300)
    except:
        print('\a')

# -------- SAVE CSV --------
def save_csv(source, alert, details):
    exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["Time", "Source", "Alert", "Details"])
        writer.writerow([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source,
            alert,
            details.strip()
        ])

# -------- NETWORK SCANNING --------
def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex((target, port)) == 0:
            open_ports.append((port, get_service(port)))
        s.close()
    except:
        pass

def start_network_scan():
    open_ports.clear()
    target = ip_entry.get()

    if not target:
        messagebox.showerror("Error", "Enter Target IP")
        return

    output.insert(tk.END, f"\n🔍 Network Scan Started → {target}\n")

    ports = [21,22,23,25,53,80,110,139,143,443,445,3389]
    threads = []

    for p in ports:
        t = threading.Thread(target=scan_port, args=(target, p))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if open_ports:
        for port, service in open_ports:
            output.insert(tk.END, f"✅ Port {port} OPEN → {service}\n")
    else:
        output.insert(tk.END, "❌ No open ports found\n")

# -------- SYSTEM USER DETECTION --------
def detect_users():
    output.insert(tk.END, "\n👤 System User Information\n")
    os_name = platform.system()

    try:
        if os_name == "Windows":
            user = os.getlogin()
            output.insert(tk.END, f"Current User: {user}\n")
        else:
            users = subprocess.check_output("who", shell=True).decode()
            user_list = set(line.split()[0] for line in users.splitlines())
            output.insert(tk.END, f"Logged-in Users ({len(user_list)}): {', '.join(user_list)}\n")
    except:
        output.insert(tk.END, "Unable to detect users\n")

# -------- TEXT LOG MONITOR --------
def monitor_text_logs(path):
    global monitoring
    patterns = {
        "Failed Login": r"failed|invalid",
        "Unauthorized": r"unauthorized|denied",
        "Error": r"error|critical",
        "Warning": r"warning"
    }

    with open(path, "r", errors="ignore") as f:
        f.seek(0, os.SEEK_END)

        while monitoring:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            for alert, regex in patterns.items():
                if re.search(regex, line, re.IGNORECASE):
                    output.insert(tk.END, f"🚨 {alert} → {line}")
                    save_csv("TextLog", alert, line)
                    alert_sound()

# -------- EVTX ANALYSIS --------
def analyze_evtx(path):
    if not EVTX_AVAILABLE:
        messagebox.showerror("Error", "python-evtx not installed")
        return

    output.insert(tk.END, "\n🪟 Analyzing Windows EVTX\n")

    with Evtx(path) as log:
        for record in log.records():
            xml = record.xml()
            if "<EventID>4625</EventID>" in xml:
                alert = "Failed Login (4625)"
            elif "<EventID>4624</EventID>" in xml:
                alert = "Successful Login (4624)"
            elif "<EventID>4672</EventID>" in xml:
                alert = "Admin Privileges (4672)"
            else:
                continue

            output.insert(tk.END, f"🚨 {alert}\n")
            save_csv("Windows EVTX", alert, "Security Event")
            alert_sound()

# -------- FILE SELECTION --------
def select_log():
    global monitoring
    file = filedialog.askopenfilename(
        filetypes=[("Logs", "*.log *.txt *.evtx")]
    )

    if not file:
        return

    if file.endswith(".evtx"):
        analyze_evtx(file)
    else:
        monitoring = True
        status.config(text="🟢 Monitoring Active")
        threading.Thread(target=monitor_text_logs, args=(file,), daemon=True).start()

def stop_monitor():
    global monitoring
    monitoring = False
    status.config(text="🔴 Monitoring Stopped")

# -------- GUI (BLUE/GREY THEME) --------
root = tk.Tk()
root.title("Mini SIEM – Network & Log Monitoring")
root.geometry("950x600")
root.configure(bg="#2b3a42")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#2b3a42", foreground="#eaeaea")
style.configure("TButton", background="#3f5765", foreground="white")
style.configure("TLabelframe", background="#2b3a42", foreground="white")
style.configure("TLabelframe.Label", background="#2b3a42", foreground="white")

ttk.Label(root, text="🛡️ Mini SIEM – Cross Platform Tool",
          font=("Segoe UI", 18, "bold")).pack(pady=10)

# Network Frame
net = ttk.LabelFrame(root, text="Network Scanning", padding=10)
net.pack(fill="x", padx=15)

ttk.Label(net, text="Target IP:").grid(row=0, column=0)
ip_entry = ttk.Entry(net, width=25)
ip_entry.grid(row=0, column=1, padx=5)
ttk.Button(net, text="Start Scan", command=start_network_scan).grid(row=0, column=2, padx=10)
ttk.Button(net, text="Detect Users", command=detect_users).grid(row=0, column=3, padx=10)

# Log Frame
logf = ttk.LabelFrame(root, text="Log / SIEM Monitoring", padding=10)
logf.pack(fill="x", padx=15, pady=5)

ttk.Button(logf, text="Select Log / EVTX", command=select_log).grid(row=0, column=0, padx=10)
ttk.Button(logf, text="Stop Monitoring", command=stop_monitor).grid(row=0, column=1, padx=10)
status = ttk.Label(logf, text="🔴 Monitoring Stopped")
status.grid(row=0, column=2, padx=20)

# Output
frame = ttk.Frame(root)
frame.pack(padx=15, pady=10, fill="both", expand=True)

scroll = ttk.Scrollbar(frame)
scroll.pack(side="right", fill="y")

output = tk.Text(
    frame,
    bg="#1f2a30",
    fg="#9fd3c7",
    font=("Consolas", 10),
    yscrollcommand=scroll.set
)
output.pack(fill="both", expand=True)
scroll.config(command=output.yview)

ttk.Label(root, text="Alerts saved to siem_alerts.csv | Educational Use Only",
          font=("Segoe UI", 9)).pack(pady=5)

root.mainloop()







# import os, re, time, csv, socket, platform, subprocess, threading, datetime
# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# import matplotlib.pyplot as plt

# # -------- EVTX SUPPORT --------
# try:
#     from Evtx.Evtx import Evtx
#     EVTX = True
# except:
#     EVTX = False

# CSV_FILE = "siem_results.csv"
# monitoring = True
# alerts_count = {}

# # -------- MITRE MAP --------
# MITRE = {
#     "Failed Login": "T1110 – Brute Force",
#     "Successful Login": "T1078 – Valid Accounts",
#     "Admin Privilege": "T1068 – Privilege Escalation",
#     "Port Scan": "T1046 – Network Service Discovery"
# }

# # -------- SOUND --------
# def beep():
#     try:
#         import winsound
#         winsound.Beep(1200, 300)
#     except:
#         print('\a')

# # -------- CSV --------
# def save_csv(source, alert, detail):
#     exists = os.path.isfile(CSV_FILE)
#     with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
#         w = csv.writer(f)
#         if not exists:
#             w.writerow(["Time", "Source", "Alert", "MITRE", "Details"])
#         w.writerow([
#             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             source,
#             alert,
#             MITRE.get(alert, "N/A"),
#             detail
#         ])
#     alerts_count[alert] = alerts_count.get(alert, 0) + 1

# # -------- ARP LAN SCAN --------
# def lan_scan():
#     output.insert(tk.END, "\n🌐 LAN Device Detection\n")
#     try:
#         cmd = "arp -a" if platform.system() == "Windows" else "arp -n"
#         result = subprocess.check_output(cmd, shell=True).decode()
#         devices = set(re.findall(r"\d+\.\d+\.\d+\.\d+", result))
#         output.insert(tk.END, f"Devices Found: {len(devices)}\n")
#         for d in devices:
#             output.insert(tk.END, f"✔ {d}\n")
#         save_csv("LAN", "Network Discovery", f"{len(devices)} devices")
#     except:
#         output.insert(tk.END, "ARP scan failed\n")

# # -------- NETWORK SCAN --------
# def network_scan():
#     target = "127.0.0.1"
#     ports = [22, 80, 443, 3389]
#     output.insert(tk.END, "\n🔍 Auto Network Scan Started\n")

#     for p in ports:
#         try:
#             s = socket.socket()
#             s.settimeout(0.5)
#             if s.connect_ex((target, p)) == 0:
#                 output.insert(tk.END, f"OPEN {p}\n")
#                 save_csv("Network", "Port Scan", f"Port {p} open")
#             s.close()
#         except:
#             pass

# # -------- LOG MONITOR --------
# def auto_log_monitor():
#     log = "/var/log/auth.log" if platform.system() != "Windows" else None
#     if not log or not os.path.exists(log):
#         return

#     with open(log, "r", errors="ignore") as f:
#         f.seek(0, os.SEEK_END)
#         while monitoring:
#             line = f.readline()
#             if not line:
#                 time.sleep(1)
#                 continue

#             if "failed" in line.lower():
#                 alert("Failed Login", line)
#             elif "session opened" in line.lower():
#                 alert("Successful Login", line)

# def alert(name, detail):
#     output.insert(tk.END, f"🚨 {name} → {detail}")
#     save_csv("Log", name, detail.strip())
#     beep()

# # -------- EVTX --------
# def evtx_scan():
#     if not EVTX:
#         return
#     path = "Security.evtx"
#     if not os.path.exists(path):
#         return

#     with Evtx(path) as log:
#         for r in log.records():
#             x = r.xml()
#             if "4625" in x:
#                 alert("Failed Login", "EventID 4625")
#             elif "4624" in x:
#                 alert("Successful Login", "EventID 4624")
#             elif "4672" in x:
#                 alert("Admin Privilege", "EventID 4672")

# # -------- DASHBOARD --------
# def dashboard():
#     if not alerts_count:
#         messagebox.showinfo("Dashboard", "No data")
#         return
#     plt.bar(alerts_count.keys(), alerts_count.values())
#     plt.title("SIEM Alert Dashboard")
#     plt.xticks(rotation=30)
#     plt.show()

# # -------- AUTO START --------
# def auto_start():
#     threading.Thread(target=lan_scan, daemon=True).start()
#     threading.Thread(target=network_scan, daemon=True).start()
#     threading.Thread(target=auto_log_monitor, daemon=True).start()
#     threading.Thread(target=evtx_scan, daemon=True).start()

# # -------- GUI --------
# root = tk.Tk()
# root.title("Mini SIEM – Enterprise Edition")
# root.geometry("1000x620")
# root.configure(bg="#2b3a42")

# style = ttk.Style()
# style.theme_use("clam")
# style.configure("TLabel", background="#2b3a42", foreground="white")

# ttk.Label(root, text="🛡️ Mini SIEM – Network & Security Monitoring",
#           font=("Segoe UI", 18, "bold")).pack(pady=10)

# ttk.Button(root, text="📊 Dashboard", command=dashboard).pack(pady=5)

# frame = ttk.Frame(root)
# frame.pack(fill="both", expand=True, padx=10, pady=10)

# scroll = ttk.Scrollbar(frame)
# scroll.pack(side="right", fill="y")

# output = tk.Text(frame, bg="#1f2a30", fg="#9fd3c7",
#                  font=("Consolas", 10),
#                  yscrollcommand=scroll.set)
# output.pack(fill="both", expand=True)
# scroll.config(command=output.yview)

# ttk.Label(root, text="Auto Monitoring Enabled | Results saved to siem_results.csv").pack(pady=5)

# auto_start()
# root.mainloop()
