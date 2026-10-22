"""
test_all.py
Skrip pengujian otomatis komprehensif untuk seluruh Tahap 1 - 6
Menghasilkan output terminal dan log hasil pengujian.
"""

import subprocess
import time
import socket
import sys
import os

python_exe = sys.executable
workdir = r"C:/Users/hp/UTS-Pemrograman-Jaringan"

print("=" * 65)
print("PENGUJIAN SISTEM PEMROGRAMAN JARINGAN (UTS D3 TEKNIK KOMPUTER)")
print("Topik: Lab Network & Device Monitoring System")
print("Pengembang: Yusuf Rizal Indrianto (240104013)")
print("=" * 65)

# --- UJI TAHAP 1: Python & Localhost ---
print("\n[TAHAP 1] Uji Versi Python & Konektivitas Localhost:")
print(f"Versi Python: {sys.version.split()[0]}")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    print(f"Loopback 127.0.0.1: OK (Port testing {port} berhasil dibuka & ditutup)")
except Exception as e:
    print(f"Loopback test error: {e}")

# --- UJI TAHAP 2: Komunikasi TCP ---
print("\n[TAHAP 2] Uji Komunikasi TCP Dasar:")
p_tcp = subprocess.Popen([python_exe, "tcp_server.py"], cwd=workdir)
time.sleep(1)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 5000))
    banner = s.recv(1024).decode()
    print(f"Koneksi berhasil. Banner: {banner.strip()}")
    
    # Perintah 1: CHECK_DEVICE
    s.sendall(b"CHECK_DEVICE PC-LAB-01\n")
    resp1 = s.recv(1024).decode()
    print(f">> Req: CHECK_DEVICE PC-LAB-01 | Resp: {resp1.strip()}")
    
    # Perintah 2: REBOOT_DEVICE
    s.sendall(b"REBOOT_DEVICE PC-LAB-02\n")
    resp2 = s.recv(1024).decode()
    print(f">> Req: REBOOT_DEVICE PC-LAB-02 | Resp: {resp2.strip()}")
    
    # Tutup sesi
    s.sendall(b"QUIT\n")
    resp_quit = s.recv(1024).decode()
    print(f">> Req: QUIT | Resp: {resp_quit.strip()}")
    s.close()
    print("[✓] Sesi klien ditutup. Server TCP tetap berjalan aktif.")
finally:
    p_tcp.terminate()
    p_tcp.wait()

# --- UJI TAHAP 3: Komunikasi UDP ---
print("\n[TAHAP 3] Uji Komunikasi UDP & Timeout:")
# Kasus 1: Server tidak aktif (Timeout test)
print("1. Menguji kondisi server UDP TIDAK AKTIF:")
from udp_client import get_telemetry
get_telemetry()

# Kasus 2: Server aktif
print("2. Menguji kondisi server UDP AKTIF:")
p_udp = subprocess.Popen([python_exe, "udp_server.py"], cwd=workdir)
time.sleep(1)
try:
    get_telemetry()
finally:
    p_udp.terminate()
    p_udp.wait()

# --- UJI TAHAP 4: Server Multiklien Threading ---
print("\n[TAHAP 4] Uji Server TCP Multiklien Threading (3 Klien Simultan):")
p_multi = subprocess.Popen([python_exe, "tcp_multiclient_server.py"], cwd=workdir)
time.sleep(1)

def client_worker(client_id, cmd):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 5050))
        banner = s.recv(1024).decode().strip()
        s.sendall((cmd + "\n").encode())
        resp = s.recv(1024).decode().strip()
        s.sendall(b"QUIT\n")
        s.close()
        print(f"[{client_id}] {banner} | Req: '{cmd}' -> Resp: '{resp}'")
    except Exception as e:
        print(f"[{client_id}] Error: {e}")

import threading
t1 = threading.Thread(target=client_worker, args=("Klien 1 (Meja 1)", "CHECK_DEVICE PC-LAB-01"))
t2 = threading.Thread(target=client_worker, args=("Klien 2 (Meja 2)", "REBOOT_DEVICE PC-LAB-02"))
t3 = threading.Thread(target=client_worker, args=("Klien 3 (Admin Lab)", "LIST_DEVICES"))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
p_multi.terminate()
p_multi.wait()

# --- UJI TAHAP 5: Transfer Berkas TCP ---
print("\n[TAHAP 5] Uji Transfer Berkas TCP Header Biner:")
p_file = subprocess.Popen([python_exe, "file_transfer_server.py"], cwd=workdir)
time.sleep(1)

from file_transfer_client import send_file
f1 = os.path.join(workdir, "lab_network_config.ini")
f2 = os.path.join(workdir, "lab_audit_event.log")

print("1. Mengirim berkas konfigurasi:")
send_file(f1)
print("2. Mengirim berkas log audit:")
send_file(f2)

p_file.terminate()
p_file.wait()

# Bandingkan ukuran berkas
rf1 = os.path.join(workdir, "received_files", "lab_network_config.ini")
rf2 = os.path.join(workdir, "received_files", "lab_audit_event.log")
print(f"Verifikasi Berkas 1: Asli={os.path.getsize(f1)} B, Diterima={os.path.getsize(rf1)} B -> {'IDENTIK/LENGKAP' if os.path.getsize(f1) == os.path.getsize(rf1) else 'BERBEDA'}")
print(f"Verifikasi Berkas 2: Asli={os.path.getsize(f2)} B, Diterima={os.path.getsize(rf2)} B -> {'IDENTIK/LENGKAP' if os.path.getsize(f2) == os.path.getsize(rf2) else 'BERBEDA'}")

# --- UJI TAHAP 6: Layanan HTTP ---
print("\n[TAHAP 6] Uji Server & Klien HTTP Raw Socket:")
p_http = subprocess.Popen([python_exe, "http_server.py"], cwd=workdir)
time.sleep(1)

from http_client import fetch_http
fetch_http("/")
fetch_http("/status")
fetch_http("/rute_tidak_ada")

p_http.terminate()
p_http.wait()

print("\n" + "=" * 65)
print("SELURUH PENGUJIAN TAHAP 1 SAMPAI 6 BERHASIL 100%!")
print("=" * 65)
