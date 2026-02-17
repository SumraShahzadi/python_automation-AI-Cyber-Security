import socket
from datetime import datetime

# ==============================
# SAFE TARGET (LOCALHOST ONLY)
# ==============================
target_ip = "127.0.0.1"

# Common ports for learning
ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445]

print("=" * 50)
print(" SAFE NETWORK SCANNING SIMULATION ")
print(" Target:", target_ip)
print(" Time:", datetime.now())
print("=" * 50)

for port in ports_to_scan:
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        # Try connecting
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            print(f"[OPEN ] Port {port} is OPEN")
        else:
            print(f"[CLOSED] Port {port} is CLOSED")

        sock.close()

    except KeyboardInterrupt:
        print("\nScan stopped by user.")
        break

    except socket.error:
        print("Connection error.")
        break

print("\nScan completed safely.")
