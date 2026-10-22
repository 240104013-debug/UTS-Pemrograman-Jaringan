# Proyek UTS Pemrograman Jaringan — D3 Teknik Komputer

**Mata Kuliah:** Pemrograman Jaringan  
**Judul Proyek:** Sistem Monitoring & Kontrol Perangkat Jaringan Laboratorium Berbasis Multi-Protokol Socket Python (SIP-LAB)  
**Mahasiswa:** Yusuf Rizal Indrianto  
**NIM:** 240104013  
**Kelas / Semester:** TK24A1 / V  

---

## 📌 Daftar Berkas & Struktur Proyek
1. `tcp_server.py` & `tcp_client.py` : Layanan TCP dasar (Port 5000) dengan perintah khusus `CHECK_DEVICE` dan `REBOOT_DEVICE`.
2. `udp_server.py` & `udp_client.py` : Layanan UDP telemetri sensor lingkungan lab (Port 6000) dilengkapi timeout 3.0 detik.
3. `tcp_multiclient_server.py` : Server TCP multiklien berbasis threading (Port 5050) melayani banyak klien simultan.
4. `file_transfer_server.py` & `file_transfer_client.py` : Protokol transfer berkas biner TCP (Port 7000) dengan header [2B Nama][Nama][8B Size][Data].
5. `http_server.py` & `http_client.py` : Layanan HTTP server & client raw socket (Port 8080) melayani rute `/` (HTML) dan `/status` (JSON).
6. `test_all.py` : Skrip pengujian otomatis komprehensif untuk seluruh tahapan 1 sampai 6.
7. `lab_network_config.ini` & `lab_audit_event.log` : Berkas data uji transfer.

---

## 🚀 Cara Menjalankan Seluruh Pengujian:
```bash
python test_all.py
```
Seluruh pengujian Tahap 1 hingga Tahap 6 akan dieksekusi secara otomatis dengan output status terverifikasi 100%.
