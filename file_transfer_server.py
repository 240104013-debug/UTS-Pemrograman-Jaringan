"""
file_transfer_server.py
Tahap 5: Server Penerima Berkas TCP
Protokol Header Biner:
1. 2 byte: Panjang nama berkas (Big Endian)
2. N byte: Nama berkas (UTF-8)
3. 8 byte: Ukuran berkas (Big Endian)
4. M byte: Isi berkas
Port: 7000
"""

import socket
import struct
import os

HOST = "127.0.0.1"
PORT = 7000
STORAGE_DIR = "received_files"

def recv_exact(sock, n_bytes):
    """Membaca data dari socket secara berulang sampai genap n_bytes."""
    data = bytearray()
    while len(data) < n_bytes:
        packet = sock.recv(n_bytes - len(data))
        if not packet:
            return None
        data.extend(packet)
    return bytes(data)

def run_file_server():
    os.makedirs(STORAGE_DIR, exist_ok=True)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"[*] Server Transfer Berkas TCP aktif pada {HOST}:{PORT}")
    print(f"[*] Berkas yang diterima akan disimpan di: {os.path.abspath(STORAGE_DIR)}")

    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            print(f"[+] Klien terhubung dari: {client_addr}")
            
            # 1. Baca 2 byte panjang nama berkas
            raw_name_len = recv_exact(client_sock, 2)
            if not raw_name_len:
                client_sock.close()
                continue
            name_len = struct.unpack("!H", raw_name_len)[0]
            
            # 2. Baca nama berkas
            raw_filename = recv_exact(client_sock, name_len)
            filename = raw_filename.decode("utf-8")
            
            # 3. Baca 8 byte ukuran berkas
            raw_filesize = recv_exact(client_sock, 8)
            filesize = struct.unpack("!Q", raw_filesize)[0]
            
            print(f"[*] Header Diterima:")
            print(f"    - Nama Berkas   : {filename} (Panjang: {name_len} byte)")
            print(f"    - Ukuran Berkas : {filesize} byte")
            
            # 4. Baca isi berkas secara berulang
            save_path = os.path.join(STORAGE_DIR, filename)
            received_bytes = 0
            with open(save_path, "wb") as f:
                while received_bytes < filesize:
                    chunk_to_read = min(4096, filesize - received_bytes)
                    chunk = client_sock.recv(chunk_to_read)
                    if not chunk:
                        break
                    f.write(chunk)
                    received_bytes += len(chunk)
            
            if received_bytes == filesize:
                print(f"[✓] Berkas '{filename}' BERHASIL diterima utuh ({received_bytes}/{filesize} byte).")
                client_sock.sendall(b"OK: Berkas berhasil diterima dan disimpan utuh.")
            else:
                print(f"[!] GAGAL: Berkas terputus di tengah jalan ({received_bytes}/{filesize} byte).")
                client_sock.sendall(b"ERR: Ukuran berkas tidak sesuai.")
                
            client_sock.close()
    except KeyboardInterrupt:
        print("\n[!] Menghentikan server transfer berkas...")
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_file_server()
