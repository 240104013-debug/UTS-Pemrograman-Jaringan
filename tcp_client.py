"""
tcp_client.py
Tahap 2: Klien TCP Interaktif untuk Kontrol Perangkat Lab
"""

import socket

HOST = "127.0.0.1"
PORT = 5000

def run_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        banner = sock.recv(1024).decode("utf-8")
        print(f"[SERVER]: {banner.strip()}")
        print("Perintah tersedia:")
        print("  - LIST_DEVICES")
        print("  - CHECK_DEVICE <ID>   (contoh: CHECK_DEVICE PC-LAB-01)")
        print("  - REBOOT_DEVICE <ID>  (contoh: REBOOT_DEVICE PC-LAB-02)")
        print("  - QUIT")
        print("-" * 50)
        
        while True:
            cmd = input("Klien-TCP> ").strip()
            if not cmd:
                continue
                
            sock.sendall(cmd.encode("utf-8"))
            resp = sock.recv(1024).decode("utf-8")
            print(f"[BALASAN]: {resp.strip()}")
            
            if cmd.upper() == "QUIT":
                print("[*] Sesi koneksi ditutup secara tertib.")
                break
    except ConnectionRefusedError:
        print(f"[!] Gagal terhubung: Server TCP {HOST}:{PORT} tidak aktif.")
    finally:
        sock.close()

if __name__ == "__main__":
    run_client()
