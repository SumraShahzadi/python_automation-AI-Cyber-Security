# 🔍 Advanced Port Scanner (Python GUI)

An **advanced TCP port scanner** built with **Python and Tkinter** that scans target systems for open and closed ports, detects common services, performs basic banner grabbing, and attempts **OS detection using TTL analysis**.

This project is designed for **learning networking fundamentals, cybersecurity labs, and ethical penetration testing practice**.

---

## 📌 Features

✅ Graphical User Interface (GUI) using Tkinter  
✅ Scan ports **1–1024**  
✅ Shows **OPEN / CLOSED** status of all ports  
✅ Highlights:
- 🟢 Open ports (green)
- 🔴 Closed ports (red)  
✅ Service name detection (HTTP, SSH, FTP, etc.)  
✅ Basic banner grabbing (HTTP services)  
✅ Operating System guessing using **TTL-based detection**  
✅ Start / Stop scan functionality  
✅ Responsive GUI using **multithreading**  

---

## 🧠 How It Works (Concept Overview)

### 🔹 Port Scanning
- Uses **TCP connect scanning**
- Attempts to establish a TCP connection to each port
- If connection succeeds → port is **OPEN**
- If it fails → port is **CLOSED**

### 🔹 Service Detection
- Uses Python’s built-in service database:
  - Example: `80 → HTTP`, `22 → SSH`
- This maps **port numbers to known services**

### 🔹 Banner Grabbing
- Sends safe protocol-specific requests (e.g. HTTP HEAD)
- Reads service response (if available)
- Many services do **not** expose banners (normal behavior)

### 🔹 OS Detection (TTL Method)
- Sends a single `ping` packet
- Extracts **TTL (Time To Live)** value
- Guesses OS based on common defaults:

| TTL Range | OS Guess |
|----------|---------|
| ≤ 64 | Linux / Unix |
| ≤ 128 | Windows |
| > 128 | Unknown |

⚠️ OS detection is **heuristic (guess-based)**, not 100% accurate.

---

## 🛠️ Technologies Used

- Python 3
- `socket` – Networking
- `tkinter` / `ttk` – GUI
- `threading` – Background scanning
- `subprocess` – System commands (ping)
- `re` – TTL extraction

---

## ▶️ How to Run

### 1️⃣ Clone the repository
