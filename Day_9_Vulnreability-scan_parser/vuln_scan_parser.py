# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk
# import os

# class VulnerabilityParserGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("🛡️ Vulnerability Scan Parser")
#         self.root.geometry("900x600")
#         self.root.configure(bg="#0f172a")

#         self.file_path = ""

#         self.create_widgets()

#     def create_widgets(self):
#         # Title
#         title = tk.Label(
#             self.root,
#             text="Vulnerability Scan Parser Tool",
#             font=("Segoe UI", 20, "bold"),
#             fg="#38bdf8",
#             bg="#0f172a"
#         )
#         title.pack(pady=10)

#         # File Selection Frame
#         frame = tk.Frame(self.root, bg="#020617")
#         frame.pack(fill="x", padx=20, pady=10)

#         self.file_label = tk.Label(
#             frame,
#             text="No file selected",
#             fg="white",
#             bg="#020617",
#             font=("Segoe UI", 10)
#         )
#         self.file_label.pack(side="left", padx=10)

#         browse_btn = ttk.Button(
#             frame,
#             text="Browse Scan File",
#             command=self.load_file
#         )
#         browse_btn.pack(side="right", padx=10)

#         # Output Area
#         output_frame = tk.Frame(self.root, bg="#020617")
#         output_frame.pack(fill="both", expand=True, padx=20, pady=10)

#         self.text_area = tk.Text(
#             output_frame,
#             bg="#020617",
#             fg="#e5e7eb",
#             insertbackground="white",
#             font=("Consolas", 11),
#             wrap="word"
#         )
#         self.text_area.pack(side="left", fill="both", expand=True)

#         scrollbar = ttk.Scrollbar(
#             output_frame,
#             orient="vertical",
#             command=self.text_area.yview
#         )
#         scrollbar.pack(side="right", fill="y")

#         self.text_area.config(yscrollcommand=scrollbar.set)

#         # Action Buttons
#         btn_frame = tk.Frame(self.root, bg="#0f172a")
#         btn_frame.pack(pady=10)

#         parse_btn = ttk.Button(
#             btn_frame,
#             text="Parse Scan",
#             command=self.parse_scan
#         )
#         parse_btn.grid(row=0, column=0, padx=10)

#         save_btn = ttk.Button(
#             btn_frame,
#             text="Save Result",
#             command=self.save_result
#         )
#         save_btn.grid(row=0, column=1, padx=10)

#         clear_btn = ttk.Button(
#             btn_frame,
#             text="Clear",
#             command=self.clear_output
#         )
#         clear_btn.grid(row=0, column=2, padx=10)

#     def load_file(self):
#         self.file_path = filedialog.askopenfilename(
#             title="Select Vulnerability Scan File",
#             filetypes=[("All Files", "*.*")]
#         )

#         if self.file_path:
#             self.file_label.config(text=os.path.basename(self.file_path))

#     def parse_scan(self):
#         if not self.file_path:
#             messagebox.showerror("Error", "Please select a scan file first")
#             return

#         try:
#             with open(self.file_path, "r", errors="ignore") as file:
#                 data = file.read()

#             self.text_area.delete(1.0, tk.END)
#             self.text_area.insert(tk.END, "🔍 Parsed Vulnerability Results\n\n")

#             entries = data.strip().split("\n\n")

#             for entry in entries:
#                 lines = entry.splitlines()
#                 for line in lines:
#                     self.text_area.insert(tk.END, line + "\n")
#                 self.text_area.insert(tk.END, "-" * 60 + "\n")

#         except Exception as e:
#             messagebox.showerror("Error", str(e))

#     def save_result(self):
#         save_path = filedialog.asksaveasfilename(
#             defaultextension=".txt",
#             filetypes=[
#                 ("Text File", "*.txt"),
#                 ("CSV File", "*.csv"),
#                 ("Log File", "*.log"),
#                 ("All Files", "*.*")
#             ]
#         )

#         if save_path:
#             content = self.text_area.get(1.0, tk.END)
#             with open(save_path, "w") as file:
#                 file.write(content)
#             messagebox.showinfo("Saved", "Parsed result saved successfully!")

#     def clear_output(self):
#         self.text_area.delete(1.0, tk.END)


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VulnerabilityParserGUI(root)
#     root.mainloop()




import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re, json, csv, os
import xml.etree.ElementTree as ET


class SOCVulnerabilityParser:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ SOC Vulnerability Scan Parser")
        self.root.geometry("1200x700")
        self.root.configure(bg="#020617")

        self.file_path = ""
        self.results = []

        self.build_gui()

    # ---------------- GUI ----------------
    def build_gui(self):
        title = tk.Label(
            self.root,
            text="SOC Vulnerability Scan Parser Dashboard",
            font=("Segoe UI", 22, "bold"),
            fg="#38bdf8",
            bg="#020617"
        )
        title.pack(pady=10)

        top = tk.Frame(self.root, bg="#020617")
        top.pack(fill="x", padx=20)

        self.file_label = tk.Label(
            top,
            text="No file selected",
            fg="white",
            bg="#020617"
        )
        self.file_label.pack(side="left")

        ttk.Button(
            top,
            text="Browse Scan File",
            command=self.load_file
        ).pack(side="right")

        # Status bar
        self.status = tk.Label(
            self.root,
            text="Status: Waiting for scan file...",
            fg="#facc15",
            bg="#020617",
            font=("Segoe UI", 10)
        )
        self.status.pack(pady=5)

        # Dashboard Table
        table_frame = tk.Frame(self.root, bg="#020617")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("CVE", "Severity", "CVSS", "Description")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=250, anchor="w")

        self.table.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.table.configure(yscrollcommand=scrollbar.set)

        # Buttons
        btns = tk.Frame(self.root, bg="#020617")
        btns.pack(pady=10)

        ttk.Button(btns, text="Parse Scan", command=self.parse_scan).grid(row=0, column=0, padx=5)
        ttk.Button(btns, text="Export CSV", command=self.export_csv).grid(row=0, column=1, padx=5)
        ttk.Button(btns, text="Export JSON", command=self.export_json).grid(row=0, column=2, padx=5)
        ttk.Button(btns, text="Clear", command=self.clear).grid(row=0, column=3, padx=5)

    # ---------------- FILE LOADER ----------------
    def load_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select Vulnerability Scan File",
            filetypes=[("All Files", "*.*")]
        )
        if self.file_path:
            self.file_label.config(text=os.path.basename(self.file_path))
            self.status.config(text="Status: File loaded, ready to parse")

    # ---------------- CVSS LOGIC ----------------
    def cvss_from_severity(self, sev):
        return {
            "Critical": 9.8,
            "High": 8.0,
            "Medium": 5.5,
            "Low": 2.5,
            "INFO": 0.0
        }.get(sev, 0.0)

    # ---------------- TEXT PARSER ----------------
    def parse_text(self, data):
        blocks = data.split("\n\n")
        for block in blocks:
            cves = re.findall(r"CVE-\d{4}-\d{4,7}", block)

            severity = "Low"
            if re.search(r"critical", block, re.I):
                severity = "Critical"
            elif re.search(r"high", block, re.I):
                severity = "High"
            elif re.search(r"medium", block, re.I):
                severity = "Medium"

            for cve in cves:
                self.results.append({
                    "CVE": cve,
                    "Severity": severity,
                    "CVSS": self.cvss_from_severity(severity),
                    "Description": block.replace("\n", " ")[:400]
                })

    # ---------------- XML PARSER ----------------
    def parse_xml(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        for elem in root.iter():
            cve = elem.attrib.get("cve")
            if cve:
                severity = elem.attrib.get("severity", "Low")
                self.results.append({
                    "CVE": cve,
                    "Severity": severity,
                    "CVSS": self.cvss_from_severity(severity),
                    "Description": "Parsed from XML vulnerability report"
                })

    # ---------------- MAIN PARSE (FIXED) ----------------
    def parse_scan(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a scan file first")
            return

        self.results.clear()
        self.table.delete(*self.table.get_children())
        self.status.config(text="Status: Parsing logs...")

        if self.file_path.endswith(".xml"):
            self.parse_xml()
        else:
            with open(self.file_path, "r", errors="ignore") as f:
                self.parse_text(f.read())

        # ✅ IF NO VULNERABILITIES FOUND
        if not self.results:
            info_entry = {
                "CVE": "N/A",
                "Severity": "INFO",
                "CVSS": 0.0,
                "Description": "Scan completed successfully. No vulnerabilities were detected in this report."
            }

            self.results.append(info_entry)

            self.table.insert(
                "",
                tk.END,
                values=(
                    info_entry["CVE"],
                    info_entry["Severity"],
                    info_entry["CVSS"],
                    info_entry["Description"]
                )
            )

            self.status.config(text="Status: Scan completed — No vulnerabilities found")

            messagebox.showinfo(
                "Scan Completed",
                "Log parsing completed successfully.\n\nNo vulnerabilities were found.\nYou can still export this report."
            )
            return

        # ✅ NORMAL CASE
        for r in self.results:
            self.table.insert(
                "",
                tk.END,
                values=(r["CVE"], r["Severity"], r["CVSS"], r["Description"])
            )

        self.status.config(text=f"Status: Parsing completed — {len(self.results)} findings")

        messagebox.showinfo(
            "Parsing Completed",
            f"Log parsing completed successfully!\n\nTotal Findings: {len(self.results)}"
        )

    # ---------------- EXPORT ----------------
    def export_csv(self):
        if not self.results:
            messagebox.showerror("Error", "No data to export")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["CVE", "Severity", "CVSS", "Description"]
                )
                writer.writeheader()
                writer.writerows(self.results)

            messagebox.showinfo("Exported", "CSV file exported successfully")

    def export_json(self):
        if not self.results:
            messagebox.showerror("Error", "No data to export")
            return

        path = filedialog.asksaveasfilename(defaultextension=".json")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=4)

            messagebox.showinfo("Exported", "JSON file exported successfully")

    # ---------------- CLEAR ----------------
    def clear(self):
        self.table.delete(*self.table.get_children())
        self.results.clear()
        self.status.config(text="Status: Cleared — waiting for new scan")


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    SOCVulnerabilityParser(root)
    root.mainloop()
