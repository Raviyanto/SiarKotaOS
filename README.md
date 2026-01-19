# 🚀 SiarKotaOS

SiarKotaOS adalah sistem operasi ringan berbasis antarmuka Web (GUI) yang berjalan secara minimalis di atas distribusi Debian Linux. Proyek ini dirancang untuk mengubah Debian menjadi lingkungan desktop modern menggunakan teknologi HTML, CSS, dan JavaScript yang dijembatani oleh Python.

---

## ✨ Fitur Unggulan

* **SiarKota Explorer**: File Manager fungsional untuk menjelajahi sistem file Debian Anda secara visual.
* **System Monitor**: Pemantauan penggunaan CPU dan RAM secara real-time pada desktop.
* **Kiosk Mode**: Memuat langsung ke antarmuka web saat booting tanpa desktop environment berat seperti GNOME atau KDE.
* **App Package Manager**: Sistem instalasi aplikasi otomatis melalui repositori GitHub.
* **Power Control**: Fitur shutdown sistem langsung dari antarmuka web.

---

## 🛠️ Persyaratan Sistem

* **Sistem Operasi**: Debian 12/13 (Rekomendasi: Minimal/Netinstall).
* **Perangkat Lunak**:
    * Python 3.x
    * Chromium Browser
    * XServer (xinit)
    * Git

---

## 🚀 Cara Instalasi Cepat

Cukup jalankan perintah berikut pada terminal Debian Anda setelah instalasi minimal:

1. **Clone Repositori:**
   ```bash
   git clone https://github.com/Raviyanto/SiarKotaOS.git
   cd SiarKotaOS
   ```
2. **Jalankan Skrip Instalasi**
   ```bash
   chmod +x install.sh
   ./install.sh
    ```

3. Reboot: Setelah selesai, silakan nyalakan ulang sistem Anda. SiarKotaOS akan otomatis terbuka.

## Cara Silent Boot & Splash Screen
1. Edit /etc/default/grub: GRUB_TIMEOUT=0, quiet splash.
2. Ganti logo di /usr/share/plymouth/themes/spinner/watermark.png.
3. Jalankan sudo update-grub && sudo update-initramfs -u.


📂 Struktur Proyek

main.py: Backend Python yang mengontrol sistem dan jembatan Eel.

web/: Folder berisi aset antarmuka (HTML, CSS, JS).

install.sh: Skrip otomatisasi setup sistem dan dependensi.

apps/: Direktori tempat aplikasi tambahan dari App Store akan terpasang.

🤝 Kontribusi

Proyek ini bersifat open-source. Jika Anda ingin menambahkan fitur atau memperbaiki bug, silakan buat Pull Request atau ajukan Issue.
