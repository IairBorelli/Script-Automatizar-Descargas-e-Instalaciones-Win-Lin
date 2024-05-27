import os
import subprocess
import sys
import ctypes
import requests

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        # Check for Windows
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

def run_as_admin():
    if sys.platform == 'win32':
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    else:
        os.execvp('sudo', ['sudo', 'python3'] + sys.argv)

if not is_admin():
    print("Este script requiere privilegios de administrador para ejecutarse.")
    run_as_admin()
    sys.exit(0)

# URLs de descarga
download_urls = {
    "Steam": "https://steamcdn-a.akamaihd.net/client/installer/SteamSetup.exe",
    "Brave Browser": "https://laptop-updates.brave.com/latest/winx64",
    "Discord": "https://discord.com/api/download?platform=win",
    "Telegram": "https://updates.tdesktop.com/tsetup/tsetup.exe",
    "Audacity": "https://fossies.org/windows/misc/audacity-win-3.1.3-x64.exe",
    "Visual Studio Code": "https://update.code.visualstudio.com/latest/win32-x64-user/stable",
    "Git": "https://github.com/git-for-windows/git/releases/latest/download/Git-2.36.1-64-bit.exe",
    "GitHub Desktop": "https://central.github.com/deployments/desktop/desktop/latest/win32",
    "Cougar Minos XC Driver": "https://cougargaming.com/fileadmin/downloads/minos_x2_1.08.zip",
    "TLauncher": "https://tlauncher.org/jar",
    "Free Download Manager": "https://dn3.freedownloadmanager.org/6/latest/fdm_x64_setup.exe",
    "WO Mic Client": "https://wolicheng.com/womic/files/WoMicClientSetup.exe",
    "Python": "https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe",
    "Readmin VPN": "https://download.radmin.com/download/files/RVServer_3.5.2.1_EN.msi",
    "Revo Uninstaller": "https://www.revouninstaller.com/download-professional-version.php",
    "Wise Memory Optimizer": "https://www.wisecleaner.com/soft/WiseMemoryOptimizer.exe"
}

# URL de descarga de Spotify
spotify_url = "https://download.scdn.co/SpotifySetup.exe"

# Directorio de descargas
download_dir = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_dir, exist_ok=True)

# Función para descargar un archivo
def download_file(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(download_dir, file_name)
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {file_name}")
        return file_path
    else:
        print(f"Failed to download: {file_name}")
        return None

# Función para ejecutar un archivo
def run_installer(file_path):
    try:
        subprocess.run(file_path, check=True)
        print(f"Installed: {os.path.basename(file_path)}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install: {os.path.basename(file_path)}")

# Descargar e instalar cada programa
for program, url in download_urls.items():
    print(f"Downloading and installing: {program}")
    file_name = url.split("/")[-1]
    installer_path = download_file(url, file_name)
    if installer_path:
        run_installer(installer_path)

# Descargar e instalar Spotify sin privilegios de administrador
print("Downloading and installing: Spotify")
spotify_installer = download_file(spotify_url, "SpotifySetup.exe")
if spotify_installer:
    try:
        subprocess.run(spotify_installer, check=True)
        print("Installed: Spotify")
    except subprocess.CalledProcessError as e:
        print("Failed to install: Spotify")
