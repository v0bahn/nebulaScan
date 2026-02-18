# Nebula probe simple homemade port scanner 

import socket
import re
import sys
import signal
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Banner 

def banner():
  print("""
\033[0;35m=====================================
      ✨NEBULA PROBE✨
=====================================
  🐍 Python TCP Scanner
  👦 Author : v0ban
  🤔 Usage  : Scan open ports (1-8080)
=====================================\033[0m
""")

banner()

# Flag d'arrêt global

stop_event = threading.Event()

# Ctrl+C (SIGINT)

def handle_exit(sig, frame):
    stop_event.set() 
    sys.stdout.write("\n\n\033[0;31m⛔ Scan interrompu (Ctrl+C)\033[0m\n")
    sys.stdout.flush()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# Input target & validation syntax

testinput = input("🕵️ Set URL for Scanning (www.target.com): ")

def validHostname(testinput):
    pattern = r"^(?=.*[a-zA-Z])[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$"
    return re.match(pattern, testinput) is not None

if not validHostname(testinput):
    print("\033[0;31m❌ Invalid hostname format (www.example.com)\033[0m")
    exit()

try:
    target = socket.gethostbyname(testinput)
except socket.gaierror:
    print("\033[0;31m❌ Invalid hostname format (DNS error)\033[0m")
    exit()

print(f"\033[0;32m🔍 Scanning\033[0m {testinput} ({target})\n")

# Progress bar

progress_lock = threading.Lock()
scanned_count = 0

def progress_bar(current, total, bar_length=40):
    percent = current / total
    filled = int(bar_length * percent)
    bar = "█" * filled + "░" * (bar_length - filled)
    sys.stdout.write(f"\r\033[0;35m[{bar}]\033[0m {current}/{total} ({percent*100:.1f}%)")
    sys.stdout.flush()

# Scan port

TOTAL = 8079

def scan_port(port):
    global scanned_count

    # Ctrl+C stop process
    if stop_event.is_set():
        return port, False

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        result = s.connect_ex((target, port))
        return port, result == 0
    finally:
        s.close()
        with progress_lock:
            scanned_count += 1
            progress_bar(scanned_count, TOTAL)

# Scan process (multithread)

def portScan():
    open_ports = []

    with ThreadPoolExecutor(max_workers=200) as executor:
        futures = {executor.submit(scan_port, port): port for port in range(1, 8080)}
        for future in as_completed(futures):
            if stop_event.is_set():
                executor.shutdown(wait=False, cancel_futures=True)
                break
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)

    # Final result
    sys.stdout.write("\n\n")
    if open_ports:
        for port in sorted(open_ports):
            sys.stdout.write(f"\033[0;32m✅ FOUND\033[0m : PORT {port} is \033[0;32mOPEN\033[0m\n")
    else:
        sys.stdout.write("\033[0;33m⚠️  Aucun port ouvert trouvé.\033[0m\n")

    sys.stdout.write("\n\033[0;32m✅ Scan terminé !\033[0m\n")
    sys.stdout.flush()

portScan()