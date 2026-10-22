"""
tcp_multiclient_server.py
Tahap 4: Server TCP Multiklien Berbasis Threading
Melayani banyak klien secara bersamaan dan menampilkan ID thread & alamat klien
Port: 5050
"""

import socket
import threading

HOST = "127.0.0.1"
PORT = 5050

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
        return "BYE: Menutup sesi koneksi TCP."
        
    else:
        return f"ERR: Perintah '{cmd}' tidak dikenali. Tersedia: CHECK_DEVICE, REBOOT_DEVICE, LIST_DEVICES, QUIT."

def handle_client(client_sock, client_addr):
    thread_name = threading.current_thread().name
    print(f"[THREAD-START] {thread_name} melayani klien dari {client_addr}")
    
    try:
        client_sock.sendall(f"WELCOME: Terhubung ke Server Multiklien [{thread_name}]\n".encode("utf-8"))
        
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
                
            cmd_str = data.decode("utf-8").strip()
            print(f"[{thread_name}] Menerima dari {client_addr}: '{cmd_str}'")
            
            resp = process_command(cmd_str)
            client_sock.sendall((resp + "\n").encode("utf-8"))
            
            if cmd_str.upper() == "QUIT":
                break
    except Exception as e:
        print(f"[{thread_name}] Terjadi kesalahan: {e}")
    finally:
        client_sock.close()
        print(f"[THREAD-END] {thread_name} selesai melayani {client_addr}. Koneksi ditutup.")

def run_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(10)
    print(f"[*] Thread Utama: Server TCP Multiklien mendengarkan pada {HOST}:{PORT}")

    client_counter = 1
    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            # Buat thread pekerja baru untuk setiap klien
            t = threading.Thread(
                target=handle_client,
                args=(client_sock, client_addr),
                name=f"Thread-Klien-{client_counter}"
            )
            client_counter += 1
            t.daemon = True
            t.start()
            print(f"[*] Thread Utama: Menyerahkan koneksi {client_addr} ke {t.name} (Total Thread Aktif: {threading.active_count()})")
    except KeyboardInterrupt:
        print("\n[!] Server dimatikan oleh pengguna.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_server()
