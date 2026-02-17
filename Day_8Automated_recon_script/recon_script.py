import socket
import subprocess

# Target (SAFE: Localhost only)
target = "127.0.0.1"

print("Starting Reconnaissance Scan on:", target)
print("-" * 50)

# ---------------------------
# Step 1: Nmap Port Scan
# ---------------------------
print("[+] Running Nmap Scan...")

nmap_command = ["nmap", "-sV", target]
result = subprocess.run(nmap_command, capture_output=True, text=True)

print(result.stdout)

# ---------------------------
# Step 2: Banner Grabbing
# ---------------------------
print("[+] Banner Grabbing")

common_ports = [21, 22, 80, 443]

for port in common_ports:
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((target, port))
        banner = sock.recv(1024)
        print(f"Port {port} Banner:", banner.decode().strip())
        sock.close()
    except:
        print(f"Port {port}: No banner or closed")

print("\nReconnaissance Completed Successfully!")
