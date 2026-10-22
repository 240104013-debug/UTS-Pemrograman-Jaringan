"""
udp_client.py
Tahap 3: Klien UDP Telemetri dengan Batas Waktu (Timeout 3 Detik)
"""

import socket
import sys

HOST = "127.0.0.1"
PORT = 6000

def get_telemetry():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3.0)  # Batas waktu timeout 3 detik
    
    msg = "GET_TELEMETRY"
    print(f"[*] Mengirim datagram UDP ke {HOST}:{PORT}: '{msg}'")
    
    try:
        sock.sendto(msg.encode("utf-8"), (HOST, PORT))
        data, server_addr = sock.recvfrom(1024)
        print(f"[+] Balasan diterima dari {server_addr}:")
        print(f"    {data.decode('utf-8')}")
        return True
    except socket.timeout:
        print(f"[!] TIMEOUT: Batas waktu 3.0 detik terlewati. Server UDP {HOST}:{PORT} tidak merespons.")
        return False
    except Exception as e:
        print(f"[!] Terjadi kesalahan: {e}")
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    get_telemetry()
