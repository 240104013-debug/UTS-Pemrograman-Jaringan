"""
file_transfer_client.py
Tahap 5: Klien Pengirim Berkas TCP dengan Format Header Biner
Format Header:
1. 2 byte: Panjang nama berkas (struct '!H')
2. N byte: Nama berkas encoded (UTF-8)
3. 8 byte: Ukuran berkas (struct '!Q')
4. M byte: Isi berkas
"""

import socket
import struct
import os
import sys

HOST = "127.0.0.1"
PORT = 7000

def send_file(filepath):
    if not os.path.exists(filepath):
        print(f"[!] Berkas '{filepath}' tidak ditemukan.")
        return False
        
    filename = os.path.basename(filepath)
    name_bytes = filename.encode("utf-8")
    name_len = len(name_bytes)
    file_size = os.path.getsize(filepath)
    
    print(f"[*] Menyiapkan pengiriman: '{filename}'")
    print(f"    - Panjang Nama   : {name_len} byte")
    print(f"    - Ukuran Berkas  : {file_size} byte")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        
        # 1. Kirim 2 byte panjang nama berkas (Big Endian unsigned short)
        sock.sendall(struct.pack("!H", name_len))
        
        # 2. Kirim nama berkas
        sock.sendall(name_bytes)
        
        # 3. Kirim 8 byte ukuran berkas (Big Endian unsigned long long)
        sock.sendall(struct.pack("!Q", file_size))
        
        # 4. Kirim isi berkas
        sent_bytes = 0
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                sock.sendall(chunk)
                sent_bytes += len(chunk)
                
        print(f"[+] Isi berkas terkirim ({sent_bytes}/{file_size} byte).")
        
        # Terima konfirmasi
        ack = sock.recv(1024).decode("utf-8")
        print(f"[SERVER]: {ack}")
        return True
    except ConnectionRefusedError:
        print(f"[!] Server {HOST}:{PORT} tidak aktif.")
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_file(sys.argv[1])
    else:
        print("Penggunaan: python file_transfer_client.py <path_berkas>")
