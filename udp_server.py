"""
udp_server.py
Tahap 3: Layanan Pendukung UDP Telemetri Suhu & Daya Lab
Port: 6000
"""

import socket
import random
import time

HOST = "127.0.0.1"
PORT = 6000

def run_udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[*] UDP Telemetry Server aktif pada {HOST}:{PORT}")
    print("[*] Menunggu datagram permintaan sensor...")

    try:
        while True:
            data, client_addr = sock.recvfrom(1024)
            msg = data.decode("utf-8").strip()
            print(f"[+] Datagram diterima dari {client_addr}: '{msg}'")
            
            if msg.upper() == "GET_TELEMETRY":
                # Simulasi pembacaan sensor IoT Lab
                temp = round(random.uniform(22.5, 27.8), 1)
                humidity = random.randint(50, 68)
                power = random.randint(1100, 1450)
                resp = f"TELEMETRY: Temp={temp}C, Humidity={humidity}%, PowerUsage={power}W, Timestamp={time.strftime('%H:%M:%S')}"
            else:
                resp = f"ERR: Perintah UDP tidak valid. Gunakan 'GET_TELEMETRY'"
                
            sock.sendto(resp.encode("utf-8"), client_addr)
            print(f"[-] Balasan dikirim ke {client_addr}: {resp}")
    except KeyboardInterrupt:
        print("\n[!] Server UDP dihentikan.")
    finally:
        sock.close()

if __name__ == "__main__":
    run_udp_server()
