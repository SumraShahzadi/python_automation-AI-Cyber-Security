Absolutely! Here's a detailed `README.md` tailored for your **Brute-Force Log Monitor GUI** project:

---

# Brute-Force Log Monitor (Cross-Platform GUI)

A **cross-platform Python application** to monitor failed login attempts on Linux and Windows systems in **real-time**, with an **interactive GUI**, live log feed, alerts, and guidelines. Designed for cybersecurity labs, system admins, and penetration testers to visualize brute-force attacks.

---

## Features ✅

* **Cross-Platform**: Works on Linux (auth.log, journalctl) and Windows (Event Logs `.evtx`)
* **Real-Time Monitoring**:

  * Linux: Live `auth.log` tail or `journalctl -f`
  * Windows: Parse `.evtx` Event Log files
* **Brute-Force Detection**: Alerts when an IP fails login ≥5 times
* **Interactive GUI**:

  * Maximizeable window
  * Live log feed
  * Color-coded highlights for alerts
  * Pop-up notifications for suspicious activity
  * Guidelines panel explaining monitoring instructions
* **Extensible**: Easily add new log patterns for other services (e.g., RDP, sudo)

---

## Installation 🛠️

### Requirements

* **Python 3.9+**
* Required packages:

```bash
pip install python-evtx
```

*(Windows only for `.evtx` parsing)*

* Linux: Access to `/var/log/auth.log` or `sudo` for `journalctl -u ssh`

---

### Clone the Project

```bash
git clone https://github.com/yourusername/bruteforce-monitor.git
cd bruteforce-monitor
```

---

## Usage 💻

1. **Run the application**:

```bash
python brute_force_gui.py
```

2. **Select Log Source**:

   * Linux: `auth.log` or `journalctl (SSH)`
   * Windows: `Event Log (.evtx)`

3. **If needed**, select a log file (Windows `.evtx`) via the **“Select File”** button.

4. Click **“Start Monitoring”**. The GUI will display:

   * Live log feed
   * Guidelines and instructions
   * Color-coded alerts for IPs with ≥5 failed login attempts

5. Click **“Stop Monitoring”** to halt monitoring.

---

## How It Works ⚙️

* **Linux**: Uses `tail -f` for `auth.log` or `journalctl -f -u ssh` to fetch live logs.
* **Windows**: Parses Event Logs using `python-evtx`.
* **Failed login detection**: Regex pattern identifies failed SSH or login attempts.
* Alerts are displayed both in GUI (red text) and as pop-up notifications.

---

## Example Screenshot 🖼️

```
+--------------------------------------------+
| Guidelines / Instructions                  |
|--------------------------------------------|
| - Monitor failed login attempts            |
| - Red highlight = >5 failed attempts       |
| - Linux: auth.log / journalctl (SSH)      |
| - Windows: Event Log (.evtx)              |
+--------------------------------------------+
| [Live Log Feed - Updates in real time]    |
|  Failed password from 192.168.0.10        |
|  Failed password from 192.168.0.10        |
|  [ALERT] Possible brute-force from ...    |
+--------------------------------------------+
```

---

## Security Notes ⚠️

* Must be run with appropriate permissions to access logs.
* Linux `journalctl` may require `sudo` to access SSH logs.
* Windows live monitoring is limited to `.evtx` files unless extended via Windows Event API.
* Designed for monitoring **your own systems** for learning and security purposes.

---

## Future Enhancements 🚀

* Live Windows monitoring without pre-exported `.evtx`
* Add more log patterns for other services (RDP, FTP, sudo, etc.)
* Export alerts to a CSV or database
* Integrate with Wazuh/ELK for centralized monitoring

---

## License 📄

MIT License — Free to use, modify, and share.

---

## Author ✨

**Sumra Shahzadi**

* Cybersecurity Student & Developer
* Projects: OS Simulation, Brute-Force Monitors, Security Tools

---

If you want, I can also **write a fully formatted version with badges, install instructions for Linux and Windows separately, and screenshots placeholders** — perfect for GitHub.

Do you want me to do that upgraded version too?
