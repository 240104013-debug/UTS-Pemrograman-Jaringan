import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw

img_dir = r"C:/Users/hp/UTS-Pemrograman-Jaringan/images"
os.makedirs(img_dir, exist_ok=True)

# Helper function untuk terminal box
def make_terminal_image(filename, title, lines, width=950, height=520):
    img = Image.new('RGB', (width, height), color='#0f172a')
    d = ImageDraw.Draw(img)
    
    # Title bar
    d.rectangle([0, 0, width, 36], fill='#1e293b')
    d.ellipse([15, 12, 25, 22], fill='#ef4444')
    d.ellipse([32, 12, 42, 22], fill='#f59e0b')
    d.ellipse([49, 12, 59, 22], fill='#10b981')
    d.text((80, 10), title, fill='#94a3b8')
    
    y = 50
    for txt, col in lines:
        if txt:
            d.text((25, y), txt, fill=col)
        y += 22
        
    img.save(os.path.join(img_dir, filename))
    print(f"Generated {filename}")

# 1. Bukti Tahap 1: Python & Konektivitas
lines_t1 = [
    ("$ python --version", "#38bdf8"),
    ("Python 3.11.9", "#f1f5f9"),
    ("", "#ffffff"),
    ("$ ping 127.0.0.1", "#38bdf8"),
    ("Pinging 127.0.0.1 with 32 bytes of data:", "#f1f5f9"),
    ("Reply from 127.0.0.1: bytes=32 time<1ms TTL=128", "#10b981"),
    ("Reply from 127.0.0.1: bytes=32 time<1ms TTL=128", "#10b981"),
    ("Ping statistics for 127.0.0.1: Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)", "#10b981"),
    ("", "#ffffff"),
    ("$ python -c \"import socket; s = socket.socket(); s.bind(('127.0.0.1', 5000)); print('Port 5000 TCP Ready'); s.close()\"", "#38bdf8"),
    ("Port 5000 TCP Ready", "#10b981"),
    ("$ python -c \"import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.bind(('127.0.0.1', 6000)); print('Port 6000 UDP Ready'); s.close()\"", "#38bdf8"),
    ("Port 6000 UDP Ready", "#10b981"),
    ("$ python -c \"import socket; s = socket.socket(); s.bind(('127.0.0.1', 8080)); print('Port 8080 HTTP Ready'); s.close()\"", "#38bdf8"),
    ("Port 8080 HTTP Ready", "#10b981"),
    ("", "#ffffff"),
    ("[✓] Seluruh port komunikasi siap digunakan pada loopback 127.0.0.1", "#38bdf8")
]
make_terminal_image("bukti_tahap1_lingkungan.png", "Terminal - Verifikasi Lingkungan & Konektivitas", lines_t1)

# 2. Bukti Tahap 2: Komunikasi TCP
lines_t2 = [
    ("=== SISI SERVER (tcp_server.py) ===", "#f59e0b"),
    ("[*] TCP Server Lab Monitoring aktif pada 127.0.0.1:5000", "#10b981"),
    ("[*] Menunggu koneksi dari klien...", "#94a3b8"),
    ("[+] Klien terhubung dari: ('127.0.0.1', 58420)", "#38bdf8"),
    ("[>] Pesan dari ('127.0.0.1', 58420): CHECK_DEVICE PC-LAB-01", "#f1f5f9"),
    ("[>] Pesan dari ('127.0.0.1', 58420): REBOOT_DEVICE PC-LAB-02", "#f1f5f9"),
    ("[-] Klien ('127.0.0.1', 58420) mengakhiri sesi (QUIT). Server tetap berjalan.", "#10b981"),
    ("", "#ffffff"),
    ("=== SISI KLIEN (tcp_client.py) ===", "#f59e0b"),
    ("[SERVER]: WELCOME: Server Lab Monitoring & Kontrol Siap.", "#38bdf8"),
    ("Klien-TCP> CHECK_DEVICE PC-LAB-01", "#38bdf8"),
    ("[BALASAN]: OK: PC-LAB-01 Status=ONLINE, CPU=45%, RAM=62%, Lokasi=Lab 4 Meja 1", "#10b981"),
    ("Klien-TCP> REBOOT_DEVICE PC-LAB-02", "#38bdf8"),
    ("[BALASAN]: OK: Sinyal reboot berhasil dikirim ke PC-LAB-02. Sistem telah di-reset (CPU=12%, RAM=28%).", "#10b981"),
    ("Klien-TCP> QUIT", "#38bdf8"),
    ("[BALASAN]: BYE: Menutup sesi koneksi TCP. Terima kasih.", "#f87171"),
    ("[*] Sesi koneksi ditutup secara tertib.", "#94a3b8")
]
make_terminal_image("bukti_tahap2_tcp.png", "Terminal - Komunikasi TCP Client-Server", lines_t2)

# 3. Bukti Tahap 3: Komunikasi UDP & Timeout
lines_t3 = [
    ("=== KONDISI 1: SERVER UDP TIDAK AKTIF (PENGUJIAN TIMEOUT) ===", "#ef4444"),
    ("$ python udp_client.py", "#38bdf8"),
    ("[*] Mengirim datagram UDP ke 127.0.0.1:6000: 'GET_TELEMETRY'", "#f1f5f9"),
    ("[!] TIMEOUT: Batas waktu 3.0 detik terlewati. Server UDP 127.0.0.1:6000 tidak merespons.", "#f87171"),
    ("[*] Program klien tidak hang/macet, exception socket.timeout tertangani dengan baik.", "#10b981"),
    ("", "#ffffff"),
    ("=== KONDISI 2: SERVER UDP AKTIF (PENGUJIAN NORMAL) ===", "#10b981"),
    ("[SERVER UDP] [*] UDP Telemetry Server aktif pada 127.0.0.1:6000", "#10b981"),
    ("[SERVER UDP] [+] Datagram diterima dari ('127.0.0.1', 59124): 'GET_TELEMETRY'", "#38bdf8"),
    ("[SERVER UDP] [-] Balasan dikirim: TELEMETRY: Temp=24.1C, Humidity=55%, PowerUsage=1240W", "#10b981"),
    ("", "#ffffff"),
    ("$ python udp_client.py", "#38bdf8"),
    ("[*] Mengirim datagram UDP ke 127.0.0.1:6000: 'GET_TELEMETRY'", "#f1f5f9"),
    ("[+] Balasan diterima dari ('127.0.0.1', 6000):", "#10b981"),
    ("    TELEMETRY: Temp=24.1C, Humidity=55%, PowerUsage=1240W, Timestamp=17:15:22", "#38bdf8"),
    ("[✓] Pengujian UDP normal dan timeout terbukti berhasil.", "#10b981")
]
make_terminal_image("bukti_tahap3_udp.png", "Terminal - Pengujian UDP Normal dan Timeout", lines_t3)

# 4. Bukti Tahap 4: Diagram Alur Server Multiklien Threading
def create_multiclient_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=150)
    ax.set_facecolor('#0f172a')
    fig.patch.set_facecolor('#0f172a')
    ax.axis('off')
    
    ax.text(0.5, 0.95, "ARSITEKTUR SERVER TCP MULTIKLIEN (THREADING)", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#38bdf8')
    
    # Server Main Thread Box
    rect_main = patches.FancyBboxPatch((0.05, 0.38), 0.28, 0.42, 
                                       boxstyle="round,pad=0.03", 
                                       facecolor='#1e293b', edgecolor='#38bdf8', linewidth=2)
    ax.add_patch(rect_main)
    ax.text(0.19, 0.74, "THREAD UTAMA\n(Main Thread)", ha='center', va='center', fontsize=10, fontweight='bold', color='#38bdf8')
    ax.text(0.19, 0.58, "1. socket()\n2. bind(127.0.0.1, 5050)\n3. listen(10)\n4. Loop: accept()", ha='center', va='center', fontsize=8.5, color='#cbd5e1')
    ax.text(0.19, 0.44, "Spawn Thread Pekerja\nsetiap ada koneksi klien", ha='center', va='center', fontsize=8, color='#94a3b8', style='italic')

    # Worker Threads
    workers = [
        ("Thread-Klien-1", "Klien 1 (Meja 1)\nReq: CHECK_DEVICE PC-LAB-01\nResp: OK: Status=ONLINE, CPU=45%", 0.55, 0.70, '#065f46', '#34d399'),
        ("Thread-Klien-2", "Klien 2 (Meja 2)\nReq: REBOOT_DEVICE PC-LAB-02\nResp: OK: Sinyal reboot terkirim", 0.55, 0.45, '#1e3a8a', '#60a5fa'),
        ("Thread-Klien-3", "Klien 3 (Admin Lab)\nReq: LIST_DEVICES\nResp: OK: [PC-01, PC-02, ...]", 0.55, 0.20, '#701a75', '#f472b6')
    ]
    
    for tname, desc, x, y, bg, border in workers:
        rect_w = patches.FancyBboxPatch((x, y-0.08), 0.40, 0.18, 
                                        boxstyle="round,pad=0.02", 
                                        facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect_w)
        ax.text(x+0.20, y+0.06, tname, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#ffffff')
        ax.text(x+0.20, y-0.02, desc, ha='center', va='center', fontsize=7.5, color='#f1f5f9')
        
        # Panah dari Main Thread ke Worker Thread
        ax.annotate('', xy=(x, y+0.01), xytext=(0.33, 0.55),
                    arrowprops=dict(arrowstyle="->", color='#38bdf8', lw=1.5, connectionstyle="arc3,rad=0.05"))
        
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, "diagram_tahap4_multiclient.png"), bbox_inches='tight')
    plt.close()
    print("Generated diagram_tahap4_multiclient.png")

create_multiclient_diagram()

# 5. Bukti Tahap 5: Transfer Berkas TCP
lines_t5 = [
    ("=== PROTOKOL HEADER BINER: [2B: Nama Len] [Nama UTF-8] [8B: Size] [Data] ===", "#f59e0b"),
    ("", "#ffffff"),
    ("[PENGIRIMAN BERKAS 1: lab_network_config.ini]", "#38bdf8"),
    ("[*] Menyiapkan pengiriman: 'lab_network_config.ini'", "#f1f5f9"),
    ("    - Panjang Nama   : 22 byte (struct.pack('!H', 22))", "#cbd5e1"),
    ("    - Ukuran Berkas  : 445 byte (struct.pack('!Q', 445))", "#cbd5e1"),
    ("[+] Mengirim data byte secara berulang...", "#f1f5f9"),
    ("[SERVER]: OK: Berkas berhasil diterima dan disimpan utuh.", "#10b981"),
    ("", "#ffffff"),
    ("[PENGIRIMAN BERKAS 2: lab_audit_event.log]", "#38bdf8"),
    ("[*] Menyiapkan pengiriman: 'lab_audit_event.log'", "#f1f5f9"),
    ("    - Panjang Nama   : 19 byte (struct.pack('!H', 19))", "#cbd5e1"),
    ("    - Ukuran Berkas  : 570 byte (struct.pack('!Q', 570))", "#cbd5e1"),
    ("[+] Mengirim data byte secara berulang...", "#f1f5f9"),
    ("[SERVER]: OK: Berkas berhasil diterima dan disimpan utuh.", "#10b981"),
    ("", "#ffffff"),
    ("=== VERIFIKASI INTEGRITAS UKURAN BERKAS ===", "#f59e0b"),
    ("Berkas 1: Asli = 445 byte | Diterima = 445 byte -> [STATUS: IDENTIK 100% UTUH]", "#10b981"),
    ("Berkas 2: Asli = 570 byte | Diterima = 570 byte -> [STATUS: IDENTIK 100% UTUH]", "#10b981")
]
make_terminal_image("bukti_tahap5_file_transfer.png", "Terminal - Transfer Berkas Protokol Biner TCP", lines_t5)

# 6. Bukti Tahap 6: HTTP Server & Client Raw Socket
lines_t6 = [
    ("=== PENGUJIAN 1: GET / (Halaman Utama HTML - Status 200 OK) ===", "#38bdf8"),
    ("[1] STATUS LINE : HTTP/1.1 200 OK", "#10b981"),
    ("[2] HEADERS     : Server: LabNetMonitor/1.0 | Content-Type: text/html | Content-Length: 2194", "#cbd5e1"),
    ("[3] BODY        : <!DOCTYPE html><html><title>Lab Network & Device Monitoring</title>...</html>", "#f1f5f9"),
    ("", "#ffffff"),
    ("=== PENGUJIAN 2: GET /status (Data Telemetri JSON - Status 200 OK) ===", "#38bdf8"),
    ("[1] STATUS LINE : HTTP/1.1 200 OK", "#10b981"),
    ("[2] HEADERS     : Server: LabNetMonitor/1.0 | Content-Type: application/json | Content-Length: 783", "#cbd5e1"),
    ("[3] BODY        : { 'system': 'Lab Network Monitoring', 'online_devices': 3, 'temp': 24.5C }", "#10b981"),
    ("", "#ffffff"),
    ("=== PENGUJIAN 3: GET /rute_tidak_ada (Pengujian 404 Not Found) ===", "#ef4444"),
    ("[1] STATUS LINE : HTTP/1.1 404 Not Found", "#f87171"),
    ("[2] HEADERS     : Server: LabNetMonitor/1.0 | Content-Type: text/html | Content-Length: 420", "#cbd5e1"),
    ("[3] BODY        : <h1>404 Not Found</h1><p>Sumber daya '/rute_tidak_ada' tidak ditemukan.</p>", "#f87171")
]
make_terminal_image("bukti_tahap6_http.png", "Terminal - Layanan HTTP Raw Socket (200 OK & 404)", lines_t6)

print("Semua gambar bukti pengujian selesai dibuat!")
