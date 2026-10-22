"""
http_server.py
Tahap 6: Server HTTP Berbasis Socket Murni (Raw Socket)
Rute:
- /       : Halaman HTML antarmuka dashboard monitoring Lab
- /status : Data JSON status telemetri dan perangkat
- Lainnya : Respons 404 Not Found
Port: 8080
"""

import socket
import json
import time

HOST = "127.0.0.1"
PORT = 8080

def build_http_response(status_code, status_text, content_type, body_bytes):
    header = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Server: LabNetMonitor/1.0 (Raw Socket Python)\r\n"
        f"Content-Type: {content_type}; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"Connection: close\r\n\r\n"
    )
    return header.encode("utf-8") + body_bytes

def run_http_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(10)
    print(f"[*] Server HTTP aktif pada http://{HOST}:{PORT}")
    print("    - Rute HTML : http://127.0.0.1:8080/")
    print("    - Rute JSON : http://127.0.0.1:8080/status")

    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            req_data = client_sock.recv(4096).decode("utf-8", errors="ignore")
            if not req_data:
                client_sock.close()
                continue
                
            first_line = req_data.split("\r\n")[0]
            print(f"[HTTP] Permintaan dari {client_addr}: {first_line}")
            
            parts = first_line.split()
            if len(parts) >= 2:
                method = parts[0]
                path = parts[1]
            else:
                method = "GET"
                path = "/"

            if path == "/":
                html_body = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Lab Network & Device Monitoring</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; }
        .card { background: #1e293b; border-radius: 12px; padding: 20px; max-width: 750px; margin: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        h1 { color: #38bdf8; margin-top: 0; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 12px; }
        .badge-online { background: #065f46; color: #34d399; }
        .badge-offline { background: #7f1d1d; color: #f87171; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #334155; }
        th { color: #94a3b8; }
        .api-link { color: #38bdf8; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Lab Network & Device Monitoring (SIP-LAB)</h1>
        <p>Sistem Pemantauan Terpadu Jaringan Laboratorium Komputer - D3 Teknik Komputer</p>
        <p><strong>Pengembang:</strong> Yusuf Rizal Indrianto (NIM: 240104013)</p>
        <hr style="border: 0; border-top: 1px solid #334155; margin: 20px 0;">
        <h3>Daftar Perangkat Lab:</h3>
        <table>
            <tr><th>Perangkat ID</th><th>Lokasi</th><th>Status</th><th>Beban CPU</th><th>RAM</th></tr>
            <tr><td>PC-LAB-01</td><td>Lab 4 Meja 1</td><td><span class="badge badge-online">ONLINE</span></td><td>45%</td><td>62%</td></tr>
            <tr><td>PC-LAB-02</td><td>Lab 4 Meja 2</td><td><span class="badge badge-online">ONLINE</span></td><td>78%</td><td>85%</td></tr>
            <tr><td>PC-LAB-03</td><td>Lab 4 Meja 3</td><td><span class="badge badge-offline">OFFLINE</span></td><td>0%</td><td>0%</td></tr>
            <tr><td>SW-CORE-01</td><td>Rack Server</td><td><span class="badge badge-online">ONLINE</span></td><td>22%</td><td>38%</td></tr>
        </table>
        <p style="margin-top: 20px;">Lihat data mentah JSON: <a class="api-link" href="/status">/status</a></p>
    </div>
</body>
</html>
"""
                resp = build_http_response(200, "OK", "text/html", html_body.encode("utf-8"))
                
            elif path == "/status":
                status_dict = {
                    "system": "Lab Network & Device Monitoring",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "server_port": PORT,
                    "total_devices": 4,
                    "online_devices": 3,
                    "offline_devices": 1,
                    "telemetry_sensors": {
                        "temperature_celsius": 24.5,
                        "humidity_percent": 58,
                        "power_usage_watts": 1280
                    },
                    "devices": [
                        {"id": "PC-LAB-01", "status": "ONLINE", "cpu_load": "45%", "memory_load": "62%"},
                        {"id": "PC-LAB-02", "status": "ONLINE", "cpu_load": "78%", "memory_load": "85%"},
                        {"id": "PC-LAB-03", "status": "OFFLINE", "cpu_load": "0%", "memory_load": "0%"},
                        {"id": "SW-CORE-01", "status": "ONLINE", "cpu_load": "22%", "memory_load": "38%"}
                    ]
                }
                body_bytes = json.dumps(status_dict, indent=2).encode("utf-8")
                resp = build_http_response(200, "OK", "application/json", body_bytes)
                
            else:
                error_html = f"""<!DOCTYPE html>
<html>
<head><title>404 Not Found</title></head>
<body style="font-family:sans-serif; text-align:center; padding-top:50px; background:#0f172a; color:#f8fafc;">
    <h1 style="color:#ef4444; font-size:48px;">404 Not Found</h1>
    <p>Sumber daya pada alamat '{path}' tidak ditemukan di server ini.</p>
    <p><a href="/" style="color:#38bdf8;">Kembali ke Halaman Utama (/)</a></p>
</body>
</html>"""
                resp = build_http_response(404, "Not Found", "text/html", error_html.encode("utf-8"))

            client_sock.sendall(resp)
            client_sock.close()
    except KeyboardInterrupt:
        print("\n[!] Menghentikan HTTP Server...")
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_http_server()
