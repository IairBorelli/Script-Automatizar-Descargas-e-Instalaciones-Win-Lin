import os
import subprocess
import sys
import requests

# Función para verificar si se ejecuta como root
def is_root():
    return os.getuid() == 0

# Función para pedir privilegios de root si no los tiene
def run_as_root():
    if not is_root():
        os.execvp('sudo', ['sudo', 'python3'] + sys.argv)

# Verificar y pedir privilegios de root
if not is_root():
    print("Este script requiere privilegios de root para ejecutarse.")
    run_as_root()
    sys.exit(0)

# URLs de descarga para Linux
download_urls = {
    "Steam": "https://steamcdn-a.akamaihd.net/client/installer/steam.deb",
    "Brave Browser": "https://brave-browser-apt-release.s3.brave.com/pool/main/b/brave-browser/brave-browser_1.40.113_amd64.deb",
    "Discord": "https://discord.com/api/download?platform=linux&format=deb",
    "Telegram": "https://updates.tdesktop.com/tlinux/tsetup.3.7.3.tar.xz",
    "Audacity": "https://github.com/audacity/audacity/releases/download/Audacity-3.1.3/audacity-linux-3.1.3.tar.xz",
    "Visual Studio Code": "https://update.code.visualstudio.com/latest/linux-deb-x64/stable",
    "Git": "https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.36.1.tar.gz",
    "GitHub Desktop": "https://github.com/shiftkey/desktop/releases/download/release-2.9.4-linux1/GitHubDesktop-linux-2.9.4-linux1.deb",
    "Free Download Manager": "https://dn3.freedownloadmanager.org/6/latest/freedownloadmanager.deb",
    "Spotify": "https://repository-origin.spotify.com/pool/non-free/s/spotify-client/spotify-client_1.1.84.716-2_amd64.deb"
}

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

# Función para instalar un archivo .deb
def install_deb(file_path):
    try:
        subprocess.run(['sudo', 'dpkg', '-i', file_path], check=True)
        subprocess.run(['sudo', 'apt-get', '-f', 'install', '-y'], check=True)
        print(f"Installed: {os.path.basename(file_path)}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install: {os.path.basename(file_path)}")

# Descargar e instalar cada programa
for program, url in download_urls.items():
    print(f"Downloading and installing: {program}")
    file_name = url.split("/")[-1]
    installer_path = download_file(url, file_name)
    if installer_path:
        install_deb(installer_path)

# Nota: Algunos programas pueden requerir otros métodos de instalación
