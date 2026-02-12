import os
import re
import platform
import subprocess
from threading import Thread
from collections import Counter
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Optional: Windows .evtx parsing
try:
    from Evtx.Evtx import Evtx
    from Evtx.Views import evtx_file_xml_view
    EVTX_AVAILABLE = True
except ImportError:
    EVTX_AVAILABLE = False

class BruteForceMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Brute-Force Log Monitor")
        self.root.state('zoomed')  # maximize GUI
        self.monitoring = False

        # OS detection
        self.os_name = platform.system()

        # --- GUI Setup ---
        self.setup_gui()

    def setup_gui(self):
        # Top frame for options
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, pady=5)

        tk.Label(top_frame, text="Select Log Source:").pack(side=tk.LEFT, padx=5)
        self.log_source = ttk.Combobox(top_frame, state="readonly", width=30)
        if self.os_name == "Linux":
            self.log_source['values'] = ["Linux auth.log", "Linux journalctl (SSH)"]
        elif self.os_name == "Windows":
            self.log_source['values'] = ["Windows Event Log (.evtx)"]
        self.log_source.current(0)
        self.log_source.pack(side=tk.LEFT, padx=5)

        self.file_button = tk.Button(top_frame, text="Select File (if needed)", command=self.select_file)
        self.file_button.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(top_frame, text="Start Monitoring", bg="green", fg="white", command=self.toggle_monitor)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Guidelines / info panel
        self.guidelines = tk.Text(self.root, height=6, bg="#f0f0f0", fg="black")
        self.guidelines.pack(fill=tk.X, padx=5, pady=5)
        self.guidelines.insert(tk.END, "Guidelines:\n"
                                       "- Monitor failed login attempts.\n"
                                       "- Red highlight = more than 5 failed attempts.\n"
                                       "- Supports live log monitoring.\n"
                                       "- Linux: auth.log or journalctl (SSH).\n"
                                       "- Windows: Event Log (.evtx).\n")
        self.guidelines.config(state=tk.DISABLED)

        # Live log feed
        self.log_feed = tk.Text(self.root, height=25, bg="black", fg="white")
        self.log_feed.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.log_feed, command=self.log_feed.yview)
        self.log_feed.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Internal variables
        self.selected_file = ""
        self.failed_ips = Counter()

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select Log File")
        if file_path:
            self.selected_file = file_path
            messagebox.showinfo("File Selected", f"File selected:\n{file_path}")

    def toggle_monitor(self):
        if not self.monitoring:
            self.monitoring = True
            self.start_button.config(text="Stop Monitoring", bg="red")
            Thread(target=self.start_monitoring, daemon=True).start()
        else:
            self.monitoring = False
            self.start_button.config(text="Start Monitoring", bg="green")

    def update_live_log(self, line):
        self.log_feed.insert(tk.END, line + "\n")
        self.log_feed.see(tk.END)

    def alert_ip(self, ip, attempts):
        msg = f"[ALERT] Possible brute-force from {ip} ({attempts} attempts)"
        self.update_live_log(msg)
        self.log_feed.tag_add("alert", "end-2l", "end-1l")
        self.log_feed.tag_config("alert", foreground="red", font=("Arial", 12, "bold"))
        messagebox.showwarning("Brute-Force Alert", msg)

    # ---------------- MONITORING LOGS ----------------
    def start_monitoring(self):
        source = self.log_source.get()

        if "journalctl" in source and self.os_name == "Linux":
            self.monitor_journalctl()
        elif "auth.log" in source and self.os_name == "Linux":
            self.monitor_file("/var/log/auth.log")
        elif "Windows" in source and self.os_name == "Windows":
            if not EVTX_AVAILABLE:
                messagebox.showerror("Error", "python-evtx not installed! Install with 'pip install python-evtx'")
                self.monitoring = False
                return
            if not self.selected_file:
                messagebox.showerror("Error", "Select an Event Log (.evtx) file!")
                self.monitoring = False
                return
            self.monitor_evtx(self.selected_file)
        else:
            messagebox.showerror("Error", "Unsupported OS or log source")
            self.monitoring = False

    # Linux: Live journalctl
    def monitor_journalctl(self):
        self.update_live_log("[INFO] Starting live journalctl monitoring...")
        proc = subprocess.Popen(
            ["journalctl", "-f", "-u", "ssh"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True
        )
        for line in iter(proc.stdout.readline, ""):
            if not self.monitoring:
                proc.terminate()
                break
            line = line.strip()
            self.update_live_log(line)
            self.check_failed_attempt(line)

    # Linux: File-based monitoring
    def monitor_file(self, file_path):
        self.update_live_log(f"[INFO] Monitoring file: {file_path}")
        with open(file_path, "r") as f:
            f.seek(0, os.SEEK_END)  # start at end
            while self.monitoring:
                line = f.readline()
                if not line:
                    continue
                line = line.strip()
                self.update_live_log(line)
                self.check_failed_attempt(line)

    # Windows: EVTX monitoring
    def monitor_evtx(self, file_path):
        self.update_live_log(f"[INFO] Parsing Windows Event Log: {file_path}")
        with Evtx(file_path) as log:
            for xml_str in evtx_file_xml_view(log):
                if not self.monitoring:
                    break
                if "Failed" in xml_str or "logon failure" in xml_str:
                    self.update_live_log(xml_str)
                    self.check_failed_attempt(xml_str)

    # ---------------- PATTERN CHECK ----------------
    def check_failed_attempt(self, line):
        # Only IPv4 for now
        failed_pattern = r"Failed password.*from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"
        match = re.search(failed_pattern, line)
        if match:
            ip = match.group(1)
            self.failed_ips[ip] += 1
            if self.failed_ips[ip] >= 5:
                self.alert_ip(ip, self.failed_ips[ip])

# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BruteForceMonitor(root)
    root.mainloop()










