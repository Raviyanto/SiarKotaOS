import eel
import os
import psutil
import platform
import shutil
import subprocess
import json
import time

# --- 1. INISIALISASI PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web')
APPS_DIR = os.path.join(BASE_DIR, 'apps')
# Path symlink di dalam folder web
SYMLINK_PATH = os.path.join(WEB_DIR, 'apps')

# Memastikan folder apps utama tersedia
if not os.path.exists(APPS_DIR):
    os.makedirs(APPS_DIR)

# --- FUNGSI OTOMATIS SYMLINK ---
def setup_symlink():
    """Membuat 'pintu ajaib' dari web/apps ke folder apps utama"""
    try:
        # Jika sudah ada folder/file di web/apps tapi bukan symlink, hapus dulu
        if os.path.exists(SYMLINK_PATH) and not os.path.islink(SYMLINK_PATH):
            if os.path.isdir(SYMLINK_PATH):
                shutil.rmtree(SYMLINK_PATH)
            else:
                os.remove(SYMLINK_PATH)
        
        # Buat symlink jika belum ada
        if not os.path.exists(SYMLINK_PATH):
            os.symlink(APPS_DIR, SYMLINK_PATH)
            print("✅ Symlink berhasil dibuat: web/apps -> apps")
    except Exception as e:
        print(f"❌ Gagal membuat symlink: {e}")

eel.init(WEB_DIR)

# --- 2. FUNGSI FILE MANAGER ---
@eel.expose
def get_file_list(current_path="/home/sartika"):
    try:
        items = []
        for item in os.listdir(current_path):
            full_path = os.path.join(current_path, item)
            is_dir = os.path.isdir(full_path)
            items.append({
                "name": item,
                "path": full_path,
                "is_dir": is_dir,
                "size": f"{os.path.getsize(full_path) // 1024} KB" if not is_dir else "--"
            })
        return sorted(items, key=lambda x: not x['is_dir'])
    except Exception as e:
        return {"error": str(e)}

# --- 3. FUNGSI PACKAGE MANAGER ---
@eel.expose
def get_installed_apps():
    apps = []
    if os.path.exists(APPS_DIR):
        for app_folder in os.listdir(APPS_DIR):
            manifest_path = os.path.join(APPS_DIR, app_folder, 'manifest.json')
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r') as f:
                        data = json.load(f)
                        data['id'] = app_folder
                        # Menggunakan path melalui symlink (apps/...) bukan (../apps/...)
                        data['path'] = f"apps/{app_folder}/{data['entry']}"
                        apps.append(data)
                except:
                    continue
    return apps

@eel.expose
def install_app(repo_url):
    try:
        app_id = repo_url.strip("/").split('/')[-1].replace('.git', '')
        target_path = os.path.join(APPS_DIR, app_id)
        if os.path.exists(target_path):
            return {"status": "error", "message": "Aplikasi sudah terpasang!"}
        
        result = subprocess.run(['git', 'clone', '--depth', '1', repo_url, target_path], 
                                capture_output=True, text=True)
        return {"status": "success"} if result.returncode == 0 else {"status": "error", "message": result.stderr}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def uninstall_app(app_id):
    try:
        target_path = os.path.join(APPS_DIR, app_id)
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
            return {"status": "success"}
        return {"status": "error", "message": "Aplikasi tidak ditemukan"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- 4. SISTEM CORE ---
@eel.expose
def get_sys_info():
    return {
        "cpu": f"{psutil.cpu_percent()}%",
        "ram": f"{psutil.virtual_memory().percent}%",
        "os": f"{platform.system()} {platform.release()}"
    }

@eel.expose
def shutdown_pc():
    print("Mematikan sistem via UI...")
    # FIX: Bunuh Chromium sebelum shutdown agar /tmp tidak terkunci
    os.system("pkill -f chromium")
    time.sleep(1)
    os.system("sudo /usr/bin/systemctl poweroff")

# --- 5. KONFIGURASI BROWSER ---
WIDTH, HEIGHT = 1366, 768
browser_options = [
    '--kiosk', 
    '--start-fullscreen', 
    f'--window-size={WIDTH},{HEIGHT}',
    '--window-position=0,0',
    '--no-sandbox',
    '--disable-translate',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-infobars',
    '--password-store=basic',
    '--user-data-dir=/tmp/siarkota_profile'
]

# --- 6. EKSEKUSI UTAMA ---
if __name__ == '__main__':
    # A. Bersihkan sesi lama yang mungkin masih mengunci /tmp
    os.system("pkill -f chromium")
    profile_dir = '/tmp/siarkota_profile'
    if os.path.exists(profile_dir):
        shutil.rmtree(profile_dir, ignore_errors=True)

    # B. Jalankan Setup Symlink otomatis
    setup_symlink()

    # C. Mulai Aplikasi
    try:
        print(f"SiarKotaOS Aktif. Symlink: OK. Port: Otomatis.")
        eel.start(
            'index.html',
            mode='chrome',
            size=(WIDTH, HEIGHT),
            cmdline_args=browser_options
        )
    except (SystemExit, KeyboardInterrupt):
        print("\nSiarKotaOS dihentikan.")
    except Exception as e:
        print(f"Error fatal: {e}")
