import eel
import os
import psutil
import platform
import shutil
import subprocess
import json

# --- 1. INISIALISASI PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web')
APPS_DIR = os.path.join(BASE_DIR, 'apps')

# Memastikan folder apps tersedia
if not os.path.exists(APPS_DIR):
    os.makedirs(APPS_DIR)

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

# --- 3. FUNGSI PACKAGE MANAGER & AUTO-DETECTION ---

@eel.expose
def get_installed_apps():
    """Memindai folder apps dan mengambil daftar aplikasi untuk ikon Desktop"""
    apps = []
    if os.path.exists(APPS_DIR):
        for app_folder in os.listdir(APPS_DIR):
            manifest_path = os.path.join(APPS_DIR, app_folder, 'manifest.json')
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r') as f:
                        data = json.load(f)
                        # Menambahkan path entry point relatif terhadap folder web
                        # Karena index.html ada di /web, maka apps ada di ../apps/
                        data['path'] = f"../apps/{app_folder}/{data['entry']}"
                        apps.append(data)
                except:
                    continue
    return apps

@eel.expose
def install_app(repo_url):
    """Mengunduh aplikasi dari GitHub dan mengekstraknya ke folder apps"""
    try:
        # Mengambil nama repo sebagai ID aplikasi
        app_id = repo_url.strip("/").split('/')[-1].replace('.git', '')
        target_path = os.path.join(APPS_DIR, app_id)

        if os.path.exists(target_path):
            return {"status": "error", "message": "Aplikasi sudah terpasang!"}

        # Melakukan git clone
        result = subprocess.run(['git', 'clone', '--depth', '1', repo_url, target_path], 
                                capture_output=True, text=True)
        
        if result.returncode == 0:
            return {"status": "success", "message": f"Berhasil memasang {app_id}"}
        else:
            return {"status": "error", "message": result.stderr}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def uninstall_app(app_id):
    try:
        target_path = os.path.join(APPS_DIR, app_id)
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
            return {"status": "success", "message": "Aplikasi berhasil dihapus"}
        return {"status": "error", "message": "Aplikasi tidak ditemukan"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- 4. FUNGSI SISTEM CORE ---
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
    print("Mematikan sistem via UI...")
    os.system("sudo /usr/bin/systemctl poweroff")

# --- 5. KONFIGURASI BROWSER ---
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

# --- 6. EKSEKUSI UTAMA ---
if __name__ == '__main__':
    profile_dir = '/tmp/siarkota_profile'
    if os.path.exists(profile_dir):
        try:
            subprocess.run(['rm', '-rf', profile_dir], check=False)
        except:
            pass

    try:
        print(f"SiarKotaOS Aktif. Menunggu UI...")
        eel.start(
            'index.html',
            mode='chrome',
            size=(WIDTH, HEIGHT),
            port=0,
            cmdline_args=browser_options
        )
    except (SystemExit, KeyboardInterrupt):
        print("\nSiarKotaOS dihentikan.")
    except Exception as e:
        print(f"Error fatal: {e}")
