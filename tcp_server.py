"""
tcp_server.py
Tahap 2: Layanan Komunikasi TCP Dasar untuk Lab Monitoring & Kontrol Perangkat
Port: 5000
"""

import socket

HOST = "127.0.0.1"
PORT = 5000

# Basis data perangkat laboratorium
devices = {
    "PC-LAB-01": {"status": "ONLINE", "cpu": 45, "ram": 62, "location": "Lab 4 Meja 1"},
    "PC-LAB-02": {"status": "ONLINE", "cpu": 78, "ram": 85, "location": "Lab 4 Meja 2"},
    "PC-LAB-03": {"status": "OFFLINE", "cpu": 0, "ram": 0, "location": "Lab 4 Meja 3"},
    "SW-CORE-01": {"status": "ONLINE", "cpu": 22, "ram": 38, "location": "Rack Server Lab 4"}
}

def process_command(cmd_line):
    parts = cmd_line.strip().split()
    if not parts:
        return "ERR: Perintah kosong"
    
    cmd = parts[0].upper()
    
    if cmd == "CHECK_DEVICE":
        if len(parts) < 2:
            return "ERR: Format salah. Gunakan: CHECK_DEVICE <DEVICE_ID>"
        dev_id = parts[1].upper()
        if dev_id in devices:
            d = devices[dev_id]
            return f"OK: {dev_id} Status={d['status']}, CPU={d['cpu']}%, RAM={d['ram']}%, Lokasi={d['location']}"
        else:
            return f"ERR: Perangkat '{dev_id}' tidak ditemukan di database Lab."
            
    elif cmd == "REBOOT_DEVICE":
        if len(parts) < 2:
            return "ERR: Format salah. Gunakan: REBOOT_DEVICE <DEVICE_ID>"
        dev_id = parts[1].upper()
        if dev_id in devices:
            if devices[dev_id]["status"] == "OFFLINE":
                return f"ERR: Gagal reboot. {dev_id} sedang dalam kondisi OFFLINE."
            devices[dev_id]["cpu"] = 12
            devices[dev_id]["ram"] = 28
            return f"OK: Sinyal reboot berhasil dikirim ke {dev_id}. Sistem telah di-reset (CPU=12%, RAM=28%)."
        else:
            return f"ERR: Perangkat '{dev_id}' tidak terdaftar."
            
    elif cmd == "LIST_DEVICES":
        dev_list = ", ".join(devices.keys())
        return f"OK: Daftar Perangkat Lab: [{dev_list}]"
        
    elif cmd == "QUIT":
        return "BYE: Menutup sesi koneksi TCP. Terima kasih."
        
    else:
        return f"ERR: Perintah '{cmd}' tidak dikenali. Tersedia: CHECK_DEVICE, REBOOT_DEVICE, LIST_DEVICES, QUIT."

def run_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"[*] TCP Server Lab Monitoring aktif pada {HOST}:{PORT}")
    print("[*] Menunggu koneksi dari klien...")

    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            print(f"[+] Klien terhubung dari: {client_addr}")
            client_sock.sendall(b"WELCOME: Server Lab Monitoring & Kontrol Siap.\n")
            
            while True:
                data = client_sock.recv(1024)
                if not data:
                    print(f"[-] Klien {client_addr} terputus secara mendadak.")
                    break
                
                cmd_str = data.decode("utf-8").strip()
                print(f"[>] Pesan dari {client_addr}: {cmd_str}")
                
                response = process_command(cmd_str)
                client_sock.sendall((response + "\n").encode("utf-8"))
                
                if cmd_str.upper() == "QUIT":
                    print(f"[-] Klien {client_addr} mengakhiri sesi (QUIT). Server tetap berjalan.")
                    break
                    
            client_sock.close()
    except KeyboardInterrupt:
        print("\n[!] Menghentikan server...")
    finally:
        server_sock.close()
        print("[*] Server TCP ditutup.")

if __name__ == "__main__":
    run_server()
