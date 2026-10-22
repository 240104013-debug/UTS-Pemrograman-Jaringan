"""
http_client.py
Tahap 6: Klien HTTP Berbasis Socket Murni (Raw Socket)
Membaca dan memisahkan bagian:
- Baris Status (Status Line)
- Header HTTP
- Isi Pesan (Body)
"""

import socket
import sys

HOST = "127.0.0.1"
PORT = 8080

def fetch_http(path):
    print(f"\n=======================================================")
    print(f"[*] Melakukan permintaan HTTP GET ke: http://{HOST}:{PORT}{path}")
    print(f"=======================================================")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {HOST}:{PORT}\r\n"
            f"User-Agent: RawSocketPythonClient/1.0\r\n"
            f"Accept: */*\r\n"
            f"Connection: close\r\n\r\n"
        )
        sock.sendall(request.encode("utf-8"))
        
        response_bytes = bytearray()
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_bytes.extend(chunk)
            
        full_response = response_bytes.decode("utf-8", errors="replace")
        
        # Pisahkan Header dan Body
        if "\r\n\r\n" in full_response:
            header_part, body_part = full_response.split("\r\n\r\n", 1)
        else:
            header_part = full_response
            body_part = ""
            
        header_lines = header_part.split("\r\n")
        status_line = header_lines[0]
        headers = header_lines[1:]
        
        print(f"[1] STATUS LINE:")
        print(f"    {status_line}")
        print(f"\n[2] HEADERS:")
        for h in headers:
            print(f"    {h}")
        print(f"\n[3] ISI RESPONS (BODY):")
        print(f"{body_part.strip()}")
        print("-" * 55)
        
    except ConnectionRefusedError:
        print(f"[!] Server HTTP {HOST}:{PORT} tidak aktif.")
    finally:
        sock.close()

if __name__ == "__main__":
    paths = ["/", "/status", "/halaman_tidak_ada"]
    for p in paths:
        fetch_http(p)
