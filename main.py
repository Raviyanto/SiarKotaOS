import eel
import os
import psutil
import platform
import shutil
import subprocess
import json

# --- 1. INISIALISASI PATH ---
# Mengambil lokasi folder utama agar path file selalu akurat
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web')
APPS_DIR = os.path.join(BASE_DIR, 'apps') # Folder untuk aplikasi terinstall

# [Catatan: Fitur Dipertahankan] Memastikan folder apps tersedia saat OS mulai
if not os.path.exists(APPS_DIR):
    os.makedirs(APPS_DIR)

eel.init(WEB_DIR)

# --- 2. FUNGSI FILE MANAGER (FITUR BARU) ---
# Keterangan: Fungsi ini memungkinkan navigasi file murni lewat web tanpa aplikasi luar.
@eel.expose
def get_file_list(current_path="/home/sartika"):
    """Mengambil daftar file dan folder untuk ditampilkan di UI Explorer"""
    try:
        items = []
        # Membaca isi direktori yang ditentukan
        for item in os.listdir(current_path):
            full_path = os.path.join(current_path, item)
            is_dir = os.path.isdir(full_path)
            items.append({
                "name": item,
                "path": full_path,
                "is_dir": is_dir,
                "size": f"{os.path.getsize(full_path) // 1024} KB" if not is_dir else "--"
            })
        # Mengembalikan data: Folder dikelompokkan di atas, File di bawah
        return sorted(items, key=lambda x: not x['is_dir'])
    except Exception as e:
        return {"error": str(e)}

# --- 3. FUNGSI PACKAGE MANAGER (FITUR DIPERTAHANKAN & DIRAPIKAN) ---
# Keterangan: Semua logika instalasi aplikasi dari GitHub tetap utuh.
@eel.expose
def get_installed_apps():
    """Memindai folder apps dan mengambil daftar aplikasi"""
    apps = []
    if os.path.exists(APPS_DIR):
        for app_id in os.listdir(APPS_DIR):
            manifest_path = os.path.join(APPS_DIR, app_id, 'manifest.json')
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r') as f:
                        apps.append(json.load(f))
                except:
                    continue
    return apps

@eel.expose
def install_app(repo_url):
    """Mengunduh aplikasi dari GitHub"""
    try:
        app_id = repo_url.split('/')[-1].replace('.git', '')
        target_path = os.path.join(APPS_DIR, app_id)

        if os.path.exists(target_path):
            return {"status": "error", "msg": "Aplikasi sudah ada!"}

        # Clone repository menggunakan perintah git sistem
        subprocess.run(['git', 'clone', repo_url, target_path], check=True)
        return {"status": "success", "msg": f"Berhasil menginstal {app_id}"}
    except Exception as e:
        return {"status": "error", "msg": str(e)}

@eel.expose
def uninstall_app(app_id):
    """Menghapus aplikasi dari sistem folder apps"""
    try:
        target_path = os.path.join(APPS_DIR, app_id)
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
            return {"status": "success", "msg": "Aplikasi dihapus"}
        return {"status": "error", "msg": "Aplikasi tidak ditemukan"}
    except Exception as e:
        return {"status": "error", "msg": str(e)}

# --- 4. FUNGSI SISTEM CORE (DIPERTAHANKAN) ---
@eel.expose
def get_sys_info():
    try:
        return {
            "cpu": f"{psutil.cpu_percent()}%",
            "ram": f"{psutil.virtual_memory().percent}%",
            "os": f"{platform.system()} {platform.release()}"
        }
    except:
        return {"cpu": "0%", "ram": "0%", "os": "Linux"}

@eel.expose
def shutdown_pc():
    # Menggunakan systemctl untuk keamanan mematikan Debian
    print("Mematikan sistem via UI...")
    os.system("sudo /usr/bin/systemctl poweroff")

# --- 5. KONFIGURASI BROWSER (DIPERTAHANKAN) ---
WIDTH = 1366
HEIGHT = 768
browser_options = [
    '--kiosk',
    '--start-fullscreen',
    f'--window-size={WIDTH},{HEIGHT}',
    '--window-position=0,0',
    '--no-sandbox',
    '--disable-translate',
    '--disable-features=Translate',
    '--lang=id',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-infobars',
    '--password-store=basic',
    '--user-data-dir=/tmp/siarkota_profile'
]

# --- 6. EKSEKUSI UTAMA & PERBAIKAN STABILITAS ---
if __name__ == '__main__':
    # [Keterangan Perbaikan]: 
    # Kode 'shutil.rmtree' lama di sini sering menyebabkan error 'mount failed' 
    # karena Chromium terkadang masih mengunci file saat perintah dijalankan.
    # Diganti dengan subprocess 'rm -rf' yang lebih tahan terhadap file locking di Linux.
    profile_dir = '/tmp/siarkota_profile'
    if os.path.exists(profile_dir):
        try:
            # Menggunakan perintah sistem langsung untuk menghindari konflik Python
            subprocess.run(['rm', '-rf', profile_dir], check=False)
        except:
            pass

    try:
        print(f"SiarKotaOS Aktif. Memindai aplikasi...")
        # [Keterangan Dipertahankan]: 
        # port=0 memastikan aplikasi tetap jalan meski port 8000 masih 'nyangkut'.
        eel.start(
            'index.html',
            mode='chrome',
            size=(WIDTH, HEIGHT),
            port=0,
            cmdline_args=browser_options
        )
    except (SystemExit, KeyboardInterrupt):
        print("SiarKotaOS dihentikan.")
    except Exception as e:
        print(f"Error fatal: {e}")
