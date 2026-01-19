#!/bin/bash
echo "=== Menginstal SiarKotaOS ==="
sudo apt update
sudo apt install -y python3-venv python3-pip xserver-xorg xinit chromium psutil git
python3 -m venv venv
source venv/bin/activate
pip install eel psutil
echo "Menyiapkan startup..."
cat <<EOF > ~/.xinitrc
#!/bin/bash
pkill -f chrome
pkill -f python3
cd ~/SiarKotaOS
exec ~/SiarKotaOS/venv/bin/python3 main.py
EOF
chmod +x ~/.xinitrc
echo "Instalasi Selesai. Silakan reboot."
