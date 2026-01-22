import eel
import os
import psutil
import platform
import shutil
import subprocess
import json
import time
import tkinter as tk  # Ditambahkan untuk Splash Screen

# --- 1. INISIALISASI PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web')
APPS_DIR = os.path.join(BASE_DIR, 'apps')
SYMLINK_PATH = os.path.join(WEB_DIR, 'apps')

if not os.path.exists(APPS_DIR):
    os.makedirs(APPS_DIR)

# --- FUNGSI SPLASH SCREEN (ZARATHUSTRA) ---
def show_splash():
    """Menampilkan jendela splash screen ala Android sebelum masuk ke GUI utama"""
    splash = tk.Tk()
    splash.title("SiarKotaOS Booting")
    
    # Buat layar penuh dan warna hitam
    splash.attributes('-fullscreen', True)
    splash.configure(bg='black')
    
    # Logo ASCII Zarathustra
    ascii_art = """
 ____  _             _  __     _             ____  ____ 
/ ___|(_) __ _ _ __ | |/ /___ | |_ __ _     / __ \/ ___|
\___ \| |/ _` | '__|| ' // _ \| __/ _` |   / / / /\___ \ 
 ___) | | (_| | |   | . \ (_) | || (_| |  | /_/ / ___) |
|____/|_|\__,_|_|   |_|\_\___/ \__\__,_|   \____/|____/ 
    """
    
    label = tk.Label(
        splash, 
        text=ascii_art, 
        fg="#00ff41", 
        bg="black", 
        font=("Courier", 12, "bold"),
        justify=tk.LEFT
    )
    label.pack(expand=True)

    # Tambahkan teks status di bawah
    status = tk.Label(splash, text="INITIALIZING ZARATHUSTRA SYSTEM...", fg="#00ff41", bg="black", font=("Courier", 10))
    status.pack(side=tk.BOTTOM, pady=50)

    # Tutup otomatis setelah 3 detik
    splash.after(3000, splash.destroy)
    splash.mainloop()

# --- FUNGSI OTOMATIS SYMLINK ---
def setup_symlink():
    try:
        if os.path.exists(SYMLINK_PATH) and not os.path.islink(SYMLINK_PATH):
            if os.path.isdir(SYMLINK_PATH):
                shutil.rmtree(SYMLINK_PATH)
            else:
                os.remove(SYMLINK_PATH)
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
    os.system("pkill -f chromium")
    time.sleep(1)
    os.system("sudo /usr/bin/systemctl poweroff")

@eel.expose
def reboot_pc():
    os.system("pkill -f chromium")
    time.sleep(1)
    os.system("sudo /usr/bin/systemctl reboot")

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
    # 1. Tampilkan Splash Screen Terlebih Dahulu (Seperti Android)
    show_splash()

    # 2. Bersihkan sesi lama
    os.system("pkill -f chromium")
    profile_dir = '/tmp/siarkota_profile'
    if os.path.exists(profile_dir):
        shutil.rmtree(profile_dir, ignore_errors=True)

    # 3. Jalankan Setup Symlink
    setup_symlink()

    # 4. Mulai Aplikasi Utama
    try:
        print(f"SiarKotaOS Aktif. Transisi Splash Selesai.")
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
